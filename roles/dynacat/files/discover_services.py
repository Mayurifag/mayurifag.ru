#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time


def discover_services(containers):
    services = {}
    for container in containers:
        name = container["name"].lstrip("/")
        labels = container.get("labels") or {}
        if labels.get("dynacat.hide") == "true":
            continue
        if labels.get("traefik.enable") != "true":
            continue

        display_name = name.replace("_", " ").replace("-", " ").title()
        state = container["state"]
        health = container.get("health")
        if state != "running" and container["oom_killed"]:
            state = "oom-killed"
        elif state != "running" and container["start_error"]:
            state = "failed"
        elif state == "running" and health:
            state = health
        elif state in ("exited", "created") and labels.get("sablier.enable") == "true":
            state = "sleeping"

        for key, rule in labels.items():
            if not key.startswith("traefik.http.routers.") or not key.endswith(".rule"):
                continue
            # API/subscription-only routes are not app entry points.
            if re.search(r"\bPath(?:Prefix|Regexp)?\s*\(", rule):
                continue
            path = (
                "/dashboard/"
                if labels.get(key.removesuffix(".rule") + ".service") == "api@internal"
                else "/"
            )
            for match in re.finditer(r"\bHost\s*\(([^)]*)\)", rule):
                for hostname in re.findall(r"`([^`]+)`", match[1]):
                    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname):
                        continue
                    url = "https://" + hostname.lower() + path
                    services[url] = {
                        "name": labels.get("dynacat.name") or display_name,
                        "url": url,
                        "status": state,
                    }
    return sorted(services.values(), key=lambda service: service["name"].casefold())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    # Request only routing metadata and state, never environment or health logs.
    fields = (
        '{"name":{{json .Name}},"labels":{{json .Config.Labels}},'
        '"state":{{json .State.Status}},"oom_killed":{{json .State.OOMKilled}},'
        '"start_error":{{if .State.Error}}true{{else}}false{{end}},'
        '"health":{{if .State.Health}}{{json .State.Health.Status}}{{else}}null{{end}}}'
    )
    containers = []
    for attempt in range(2):
        ids = subprocess.check_output(
            [
                "docker",
                "ps",
                "--all",
                "--quiet",
                "--filter",
                "label=traefik.enable=true",
            ],
            text=True,
            timeout=15,
        ).split()
        if not ids:
            break
        try:
            result = subprocess.check_output(
                ["docker", "inspect", "--format", fields, *ids],
                text=True,
                timeout=15,
            )
        except subprocess.CalledProcessError:
            # A container may disappear during recreation; enumerate once more.
            if attempt:
                raise
            continue
        containers = [json.loads(line) for line in result.splitlines()]
        break

    snapshot = {
        "updated_at": int(time.time()),
        "services": discover_services(containers),
    }
    with tempfile.NamedTemporaryFile(
        mode="w", dir=args.output.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        try:
            json.dump(snapshot, stream)
            stream.flush()
            os.chmod(temporary, 0o644)
            os.replace(temporary, args.output)
        finally:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
