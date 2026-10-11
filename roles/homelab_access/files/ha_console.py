"""Small shared transport for the existing Home Assistant OS serial console."""

import base64
from contextlib import contextmanager
import re
import select
import socket
import time
import urllib.request
import uuid


def read_until(connection, pattern, timeout=30):
    output = b""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        readable, _, _ = select.select(
            [connection], [], [], max(0, deadline - time.monotonic())
        )
        if not readable:
            break
        chunk = connection.recv(65536)
        if not chunk:
            raise RuntimeError("Home Assistant serial console disconnected")
        output += chunk
        text = output.decode(errors="replace").replace("\r", "")
        text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            return match, text
    raise TimeoutError("Home Assistant serial console timed out")


def execute(connection, command, timeout=30):
    marker = "HA_DONE_" + uuid.uuid4().hex
    line = f"{command}; printf '\\n{marker}:%s\\n' \"$?\"\r".encode()
    if len(line) >= 1024:
        raise ValueError("Console command exceeds BusyBox line-editing limit")
    connection.sendall(line)
    status, text = read_until(connection, rf"^{marker}:(\d+)$", timeout)
    if status[1] != "0":
        error = re.search(r"(?m)^([A-Za-z]+Error:[^\n]*)$", text)
        detail = error[1] if error else "inspect Home Assistant console logs"
        raise RuntimeError(
            f"Home Assistant command failed (exit {status[1]}): {detail}"
        )
    return text


def wait_prompt(connection, timeout=30):
    prompt, _ = read_until(
        connection,
        r"(?P<root>^\s*#\s*\Z)|(?P<cli>ha >\s*\Z)|"
        r"(?P<login>^[A-Za-z0-9_.-]+ login:\s*\Z)|(?P<password>Password:\s*\Z)",
        timeout,
    )
    if prompt.lastgroup == "password":
        raise PermissionError(
            "Home Assistant serial console requires interactive authentication"
        )
    return prompt.lastgroup


@contextmanager
def console(vm):
    if not str(vm).isdecimal():
        raise ValueError("VM ID must be numeric")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.connect(f"/var/run/qemu-server/{vm}.serial0")
        connection.sendall(b"\r")
        prompt = wait_prompt(connection)
        if prompt == "login":
            connection.sendall(b"root\r")
            prompt = wait_prompt(connection)
        if prompt == "cli":
            connection.sendall(b"login\r")
            prompt = wait_prompt(connection)
        if prompt != "root":
            raise RuntimeError("HA OS did not enter its root console")
        execute(connection, "true", timeout=10)
        yield connection


def upload(connection, data, destination):
    payload = base64.b64encode(data).decode()
    execute(connection, f"(umask 077; : > {destination}.b64)")
    # ponytail: 256-byte chunks fit BusyBox's 1024-byte lines; use SSH for large configuration trees.
    for offset in range(0, len(payload), 256):
        execute(
            connection,
            f"printf %s {payload[offset : offset + 256]} >> {destination}.b64",
        )
    execute(
        connection,
        f"(umask 077; base64 -d < {destination}.b64 > {destination}) && rm -f {destination}.b64",
    )


def wait_http(address, forwarded=False):
    import ipaddress

    ipaddress.IPv4Address(address)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    request = urllib.request.Request(
        f"http://{address}:80/manifest.json",
        headers={"X-Forwarded-For": "198.51.100.1"} if forwarded else {},
    )
    for _ in range(60):
        try:
            with opener.open(request, timeout=3) as response:
                if response.status == 200:
                    return
        except OSError:
            pass
        time.sleep(2)
    raise RuntimeError("Home Assistant did not accept HTTP requests")
