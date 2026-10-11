"""Configure Home Assistant's trusted proxy through its serial console and native API."""

import asyncio
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import sys
import uuid


def desired_config(current, proxy):
    network = str(ipaddress.ip_network(proxy))
    settings = {
        key: value
        for key, value in current.items()
        if key not in {"created_at", "error", "error_message"}
    }
    trusted = list(settings.get("trusted_proxies", []))
    if network not in {str(ipaddress.ip_network(value)) for value in trusted}:
        trusted.append(network)
    settings["use_x_forwarded_for"] = True
    settings["trusted_proxies"] = trusted
    return settings


async def manage_http(action, proxy):
    import aiohttp

    connector = aiohttp.UnixConnector(path=os.environ["SUPERVISOR_CORE_API_SOCKET"])
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.ws_connect("http://localhost/api/websocket") as websocket:
            auth = await asyncio.wait_for(websocket.receive_json(), 15)
            if auth.get("type") != "auth_ok":
                raise RuntimeError("Supervisor Unix socket did not authenticate")

            async def request(identifier, kind, **data):
                await websocket.send_json({"id": identifier, "type": kind, **data})
                result = await asyncio.wait_for(websocket.receive_json(), 15)
                if result.get("id") != identifier or not result.get("success"):
                    code = result.get("error", {}).get("code", "unexpected_response")
                    raise RuntimeError(
                        f"Home Assistant HTTP API rejected {kind}: {code}"
                    )
                return result.get("result")

            state = await request(1, "http/config")
            active = (
                state["pending"]
                if state["active_config_type"] == "pending"
                else state["stable"]
            )
            desired = desired_config(active, proxy)
            comparable = {key: active.get(key) for key in desired}
            if action == "--configure":
                if comparable == desired:
                    print("UNCHANGED")
                else:
                    result = await request(2, "http/config/configure", config=desired)
                    print("STAGED" if result["restart"] else "UNCHANGED")
            elif action == "--confirm":
                if comparable != desired:
                    raise RuntimeError(
                        "Active HTTP proxy settings do not match desired settings"
                    )
                if state["pending"] is not None:
                    if state["active_config_type"] != "pending":
                        raise RuntimeError(
                            "Pending HTTP settings did not become active"
                        )
                    await request(2, "http/config/promote")
                    print("PROMOTED")
                else:
                    print("UNCHANGED")
            else:
                raise ValueError("Unknown HTTP configuration action")


def configure(vm, proxy, address):
    from ha_console import console, execute, upload, wait_http

    ipaddress.ip_address(proxy)
    ipaddress.IPv4Address(address)
    temporary = "/tmp/homelab-proxy-" + uuid.uuid4().hex
    with console(vm) as connection:
        try:
            upload(connection, Path(__file__).read_bytes(), temporary + ".py")

            def invoke(action):
                return execute(
                    connection,
                    f"docker exec -i homeassistant python3 - {action} {shlex.quote(proxy)} < {temporary}.py",
                    timeout=90,
                )

            configured = invoke("--configure")
            wait_http(address, forwarded=True)
            confirmed = invoke("--confirm")
            changed = bool(
                re.search(r"(?m)^STAGED$", configured)
                or re.search(r"(?m)^PROMOTED$", confirmed)
            )
            print(json.dumps({"changed": changed}))
        finally:
            execute(connection, f"rm -f {temporary}.py.b64 {temporary}.py", timeout=10)


if __name__ == "__main__":
    if sys.argv[1] in {"--configure", "--confirm"}:
        action, proxy = sys.argv[1:]
        ipaddress.ip_address(proxy)
        asyncio.run(manage_http(action, proxy))
    else:
        configure(*sys.argv[1:])
