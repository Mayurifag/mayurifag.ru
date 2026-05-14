(() => {
  const customPopover = {
    activeTarget: null,
    container: null,
    content: null,
    hideTimer: null,
  };

  function ensureCustomPopover() {
    if (customPopover.container) return;

    customPopover.container = document.createElement("div");
    customPopover.container.className = "popover-container position-below";
    customPopover.container.addEventListener("mouseenter", () =>
      clearTimeout(customPopover.hideTimer),
    );
    customPopover.container.addEventListener(
      "mouseleave",
      hideCustomPopoverSoon,
    );

    const frame = document.createElement("div");
    frame.className = "popover-frame";
    customPopover.content = document.createElement("div");
    customPopover.content.className = "popover-content";
    frame.append(customPopover.content);
    customPopover.container.append(frame);
    document.body.append(customPopover.container);
  }

  function setupCustomWidgetTitles(root = document) {
    const targets =
      root.querySelectorAll?.(
        ".widget-type-custom-api [title]:not([data-custom-popover-text])",
      ) || [];

    for (const target of targets) {
      const text = target.getAttribute("title");
      if (!text) continue;

      target.dataset.customPopoverText = text;
      if (!target.hasAttribute("aria-label"))
        target.setAttribute("aria-label", text);
      target.removeAttribute("title");
    }
  }

  function setupHiddenWidgets(root = document) {
    const widgets = new Set();

    if (root.matches?.(".widget")) widgets.add(root);
    root.querySelectorAll?.(".widget").forEach((widget) => widgets.add(widget));
    if (root.closest?.(".widget")) {
      widgets.add(root.closest(".widget"));
    }

    for (const widget of widgets) {
      widget.hidden = !!widget.querySelector("[data-hide-widget]");
    }
  }

  function showCustomPopover(target) {
    const text = target.dataset.customPopoverText;
    if (!text) return;

    ensureCustomPopover();
    clearTimeout(customPopover.hideTimer);
    customPopover.activeTarget = target;
    customPopover.content.textContent = text;
    customPopover.content.style.maxWidth =
      target.dataset.popoverMaxWidth || "300px";
    customPopover.container.style.display = "block";
    target.classList.add("popover-active");
    positionCustomPopover();
  }

  function positionCustomPopover() {
    if (!customPopover.activeTarget) return;

    const targetBounds = customPopover.activeTarget.getBoundingClientRect();
    const containerBounds = customPopover.container.getBoundingClientRect();
    const left = Math.max(
      0,
      Math.min(
        window.innerWidth - containerBounds.width,
        Math.round(
          targetBounds.left +
            targetBounds.width / 2 -
            containerBounds.width / 2,
        ),
      ),
    );
    const top = targetBounds.bottom + window.scrollY;

    customPopover.container.style.left = `${left}px`;
    customPopover.container.style.top = `${top}px`;
    customPopover.container.style.setProperty(
      "--triangle-offset",
      `${targetBounds.left - left + targetBounds.width / 2}px`,
    );
  }

  function hideCustomPopover() {
    if (!customPopover.activeTarget) return;

    customPopover.activeTarget.classList.remove("popover-active");
    customPopover.activeTarget = null;
    customPopover.container.style.display = "none";
  }

  function hideCustomPopoverSoon() {
    clearTimeout(customPopover.hideTimer);
    customPopover.hideTimer = setTimeout(hideCustomPopover, 500);
  }

  function exchangeZonedParts(date, timeZone) {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      weekday: "short",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    })
      .formatToParts(date)
      .reduce((acc, part) => {
        acc[part.type] = part.value;
        return acc;
      }, {});

    return {
      year: Number(parts.year),
      month: Number(parts.month),
      day: Number(parts.day),
      weekday: parts.weekday,
      hour: Number(parts.hour) % 24,
      minute: Number(parts.minute),
    };
  }

  function exchangeLocalMinute(parts) {
    return (
      Math.floor(Date.UTC(parts.year, parts.month - 1, parts.day) / 60000) +
      parts.hour * 60 +
      parts.minute
    );
  }

  function exchangeLocalDateToDate(timeZone, year, month, day, hour, minute) {
    const utc = new Date(Date.UTC(year, month - 1, day, hour, minute));
    const actualParts = exchangeZonedParts(utc, timeZone);
    const wantedParts = { year, month, day, hour, minute };
    return new Date(
      utc.getTime() -
        (exchangeLocalMinute(actualParts) - exchangeLocalMinute(wantedParts)) *
          60000,
    );
  }

  function exchangeDateKey(parts) {
    return `${parts.year}-${String(parts.month).padStart(2, "0")}-${String(parts.day).padStart(2, "0")}`;
  }

  function relativeFuture(date, now) {
    const minutes = Math.max(
      1,
      Math.ceil((date.getTime() - now.getTime()) / 60000),
    );
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 60) return `${minutes}m`;
    if (hours < 24) return `${hours}h ${minutes % 60}m`;
    return `${days}d ${hours % 24}h`;
  }

  function relativePast(date, now) {
    const minutes = Math.max(
      1,
      Math.floor((now.getTime() - date.getTime()) / 60000),
    );
    const hours = Math.floor(minutes / 60);

    if (minutes < 60) return `${minutes}m`;
    return `${hours}h ${minutes % 60}m`;
  }

  function nextOpenText(date, holidayName) {
    if (!date) return "";

    const nextOpen = `Next open: ${new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
      hour12: false,
    }).format(date)}`;

    if (holidayName) return `Holiday: ${holidayName}\n${nextOpen}`;
    return nextOpen;
  }

  const holidayCache = new Map();

  function fetchHolidays(countryCode, year) {
    const key = `${countryCode}-${year}`;
    if (!holidayCache.has(key)) {
      holidayCache.set(
        key,
        fetch(
          `https://date.nager.at/api/v3/PublicHolidays/${year}/${countryCode}`,
        )
          .then((response) => (response.ok ? response.json() : []))
          .then(
            (holidays) =>
              new Map(
                holidays.map((holiday) => [
                  holiday.date,
                  holiday.name || holiday.localName,
                ]),
              ),
          )
          .catch(() => new Map()),
      );
    }

    return holidayCache.get(key);
  }

  async function holidayName(exchange, parts) {
    const holidays = await fetchHolidays(exchange.countryCode, parts.year);
    const name = holidays.get(exchangeDateKey(parts)) || "";
    if (!name || (exchange.holidayNames && !exchange.holidayNames.has(name)))
      return "";
    return name;
  }

  async function scheduleForDay(exchange, parts) {
    const apiHolidayName = await holidayName(exchange, parts);
    const isWeekend = parts.weekday === "Sat" || parts.weekday === "Sun";

    if (isWeekend || apiHolidayName)
      return { holidayName: apiHolidayName || "Weekend" };

    return {
      open: exchangeLocalDateToDate(
        exchange.timeZone,
        parts.year,
        parts.month,
        parts.day,
        exchange.openHour,
        exchange.openMinute,
      ),
      close: exchangeLocalDateToDate(
        exchange.timeZone,
        parts.year,
        parts.month,
        parts.day,
        exchange.closeHour,
        exchange.closeMinute,
      ),
      holidayName: "",
    };
  }

  async function exchangeStatus(exchange, now) {
    const todayParts = exchangeZonedParts(now, exchange.timeZone);
    const today = await scheduleForDay(exchange, todayParts);

    if (today.open && now >= today.open && now < today.close) {
      return {
        isOpen: true,
        label: "Open",
        detail: relativeFuture(today.close, now),
        popoverText: `Opened ${relativePast(today.open, now)} ago`,
      };
    }

    let holiday = today.holidayName === "Weekend" ? "" : today.holidayName;

    for (let offset = 0; offset < 14; offset++) {
      const parts = exchangeZonedParts(
        new Date(now.getTime() + offset * 86400000),
        exchange.timeZone,
      );
      const schedule = await scheduleForDay(exchange, parts);
      if (schedule.holidayName && schedule.holidayName !== "Weekend")
        holiday = schedule.holidayName;
      if (!schedule.open || schedule.open <= now) continue;

      return {
        isOpen: false,
        label: today.holidayName || "Closed",
        detail:
          today.holidayName && offset === 0
            ? today.holidayName
            : `${offset === 0 ? "in" : parts.weekday} ${relativeFuture(schedule.open, now)}`,
        popoverText: nextOpenText(schedule.open, holiday),
      };
    }

    return {
      isOpen: false,
      label: "Closed",
      detail: "schedule unavailable",
      popoverText: "",
    };
  }

  const exchanges = {
    NASDAQ: {
      countryCode: "US",
      timeZone: "America/New_York",
      openHour: 9,
      openMinute: 30,
      closeHour: 16,
      closeMinute: 0,
      holidayNames: new Set([
        "New Year's Day",
        "Martin Luther King, Jr. Day",
        "Martin Luther King Jr. Day",
        "Presidents Day",
        "Washington's Birthday",
        "Good Friday",
        "Memorial Day",
        "Juneteenth National Independence Day",
        "Independence Day",
        "Labor Day",
        "Labour Day",
        "Thanksgiving Day",
        "Christmas Day",
      ]),
    },
    MOEX: {
      countryCode: "RU",
      timeZone: "Europe/Moscow",
      openHour: 9,
      openMinute: 50,
      closeHour: 18,
      closeMinute: 50,
    },
  };

  async function updateExchangeClocks() {
    const items = document.querySelectorAll("[data-exchange-clock]");
    const now = new Date();

    for (const item of items) {
      const exchange = exchanges[item.dataset.exchangeClock];
      if (!exchange) continue;

      const status = await exchangeStatus(exchange, now);
      const state = item.querySelector("[data-exchange-state]");
      const detail = item.querySelector("[data-exchange-detail]");

      item.classList.toggle("color-subdue", !status.isOpen);
      if (state) {
        state.textContent = status.label;
        state.classList.toggle("color-positive", status.isOpen);
      }
      if (detail && status.isOpen) {
        detail.innerHTML = `<span class="color-subdue">closes </span>${status.detail}`;
      } else if (detail) {
        detail.textContent = status.detail;
      }
      item.dataset.customPopoverText = status.popoverText;
      if (status.popoverText)
        item.setAttribute("aria-label", status.popoverText);
    }
  }

  function setup() {
    setupCustomWidgetTitles();
    setupHiddenWidgets();
    updateExchangeClocks();

    document.addEventListener(
      "mouseenter",
      (event) => {
        const target = event.target.closest?.("[data-custom-popover-text]");
        if (target) showCustomPopover(target);
      },
      true,
    );
    document.addEventListener(
      "mouseleave",
      (event) => {
        if (event.target.closest?.("[data-custom-popover-text]"))
          hideCustomPopoverSoon();
      },
      true,
    );
    window.addEventListener("scroll", positionCustomPopover);
    window.addEventListener("resize", positionCustomPopover);

    new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {
          if (node.nodeType !== Node.ELEMENT_NODE) continue;
          setupCustomWidgetTitles(node);
          setupHiddenWidgets(node);
          if (
            node.matches?.("[data-exchange-clock]") ||
            node.querySelector?.("[data-exchange-clock]")
          )
            updateExchangeClocks();
        }
      }
    }).observe(document.body, { childList: true, subtree: true });

    setInterval(updateExchangeClocks, 60000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup, { once: true });
  } else {
    setup();
  }
})();
