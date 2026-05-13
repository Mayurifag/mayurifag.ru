import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SERVICES = {
    "Mayurifag/mayurifag.github.io": "mayurifag_github_io",
    "Mayurifag/mus": "mus",
    "Mayurifag/tg-ai-manager": "tg-ai-manager",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="inventories/my-provision/inventory")
    return parser.parse_args()


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def run(args, input_text=None, quiet=False, check=True):
    completed = subprocess.run(
        args,
        input=input_text,
        text=True,
        stdout=subprocess.DEVNULL if quiet else subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and completed.returncode != 0:
        message = (
            completed.stderr.strip()
            or completed.stdout.strip()
            or f"Command failed: {' '.join(args)}"
        )
        fail(message)

    return completed


def ansible_json(args):
    completed = run(args)

    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        fail(f"Failed to parse ansible-inventory output: {error}")


def inventory_hosts(inventory):
    data = ansible_json(["ansible-inventory", "-i", inventory, "--list"])
    return data.get("sample", {}).get("hosts", [])


def watchtower_host(inventory, host):
    data = ansible_json(["ansible-inventory", "-i", inventory, "--host", host])

    if not data.get("watchtower_enabled", False):
        print(f"Skipping {host}: watchtower_enabled is false")
        return None

    server_hostname = str(data.get("server_hostname", ""))
    watchtower_subdomain = str(data.get("watchtower_subdomain", ""))
    watchtower_http_api_token = str(data.get("watchtower_http_api_token", ""))
    ssh_host = str(data.get("ansible_host") or host)
    ssh_user = str(data.get("ansible_user", ""))
    ssh_port = str(data.get("server_ssh_port", ""))
    values = {
        "server_hostname": server_hostname,
        "watchtower_subdomain": watchtower_subdomain,
        "watchtower_http_api_token": watchtower_http_api_token,
        "ssh_host": ssh_host,
    }
    missing = [name for name, value in values.items() if not value]

    if missing:
        fail(f"{host} is missing vars: {', '.join(missing)}")

    if any(char.isspace() for char in watchtower_http_api_token):
        fail(f"{host} watchtower_http_api_token must not contain whitespace")

    return {
        "name": host,
        "ssh_target": f"{ssh_user}@{ssh_host}" if ssh_user else ssh_host,
        "ssh_port": ssh_port,
        "base_url": f"https://{watchtower_subdomain}.{server_hostname}/v1/update",
        "token": watchtower_http_api_token,
    }


def watched_containers(host):
    ssh_args = ["ssh", "-o", "RemoteCommand=none"]

    if host["ssh_port"]:
        ssh_args.extend(["-p", host["ssh_port"]])

    completed = run(
        ssh_args
        + [
            host["ssh_target"],
            "docker",
            "ps",
            "--format",
            "{{.Names}}",
            "--filter",
            "label=com.centurylinklabs.watchtower.enable=true",
        ]
    )
    return set(completed.stdout.split())


def set_secret(repo, name, value):
    run(["gh", "secret", "set", name, "--repo", repo], input_text=value, quiet=True)


def main():
    args = parse_args()

    for command in ("ansible-inventory", "gh", "ssh"):
        if shutil.which(command) is None:
            fail(f"Missing required command: {command}")

    if not Path(args.inventory).is_file():
        fail(f"Inventory not found: {args.inventory}")

    hosts = inventory_hosts(args.inventory)

    if not hosts:
        fail("No Watchtower hosts found")

    targets = {repo: [] for repo in SERVICES}

    for host in hosts:
        endpoint = watchtower_host(args.inventory, host)

        if endpoint is None:
            continue

        containers = watched_containers(endpoint)
        found = []

        for repo, container in SERVICES.items():
            if container in containers:
                targets[repo].append(
                    {
                        # All app images are intentionally expected in GHCR, not Docker Hub.
                        "url": f"{endpoint['base_url']}?image=ghcr.io/{repo.lower()}:latest",
                        "token": endpoint["token"],
                    }
                )
                found.append(container)

        print(f"{host}: {', '.join(found) if found else 'no configured services'}")

    print(f"Syncing Watchtower secrets for {len(SERVICES)} GitHub repo(s)")

    for repo, endpoints in targets.items():
        if not endpoints:
            fail(f"No running Watchtower-labelled container found for {repo}")

        urls_secret = " ".join(endpoint["url"] for endpoint in endpoints)
        tokens = [endpoint["token"] for endpoint in endpoints]
        tokens_secret = (
            tokens[0]
            if all(token == tokens[0] for token in tokens)
            else " ".join(tokens)
        )

        print(f"Syncing {repo}: {len(endpoints)} endpoint(s)")
        set_secret(repo, "WATCHTOWER_URLS", urls_secret)
        set_secret(repo, "WATCHTOWER_TOKENS", tokens_secret)

    print("Done")


if __name__ == "__main__":
    main()
