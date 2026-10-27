"""Synchronize working-tree files and run deployment on a private Linux controller."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import socket
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
CHUNK = 1024 * 1024
MAINTENANCE_ENV = (
    "HOMELAB_STORAGE_CONFIRM",
    "HOMELAB_MAINTENANCE_CONFIRM",
)


def manifest():
    tracked = subprocess.check_output(
        ["git", "ls-files", "--stage", "-z"],
        cwd=ROOT,
    )
    modes = {}
    for record in tracked.split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, _, stage = metadata.split()
        if stage != b"0":
            raise ValueError("Resolve Git conflicts before deploying")
        if mode not in {b"100644", b"100755"}:
            raise ValueError("Git symlinks and submodules are not supported")
        modes[os.fsdecode(name)] = mode == b"100755"
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    for name in untracked.split(b"\0"):
        if name:
            modes.setdefault(os.fsdecode(name), False)

    files = {}
    for name, executable in sorted(modes.items()):
        parts = PurePosixPath(name).parts
        if any(
            part in {".git", ".git-crypt", ".ansible", "__pycache__"} for part in parts
        ):
            continue
        if name == "makefiles/private.mk":
            continue
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"File resolves outside the source checkout: {name}")
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f"Symlinks are not supported: {name}")
        if not path.exists():
            continue
        if not path.is_file():
            raise ValueError(
                f"Expected a regular file (submodules are not supported): {name}"
            )
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as source:
            first = source.read(CHUNK)
            if first.startswith(b"\0GITCRYPT\0"):
                raise ValueError(f"Unlock git-crypt before deploying: {name}")
            digest.update(first)
            size += len(first)
            while chunk := source.read(CHUNK):
                digest.update(chunk)
                size += len(chunk)
        files[name] = {
            "sha256": digest.hexdigest(),
            "size": size,
            "executable": executable,
        }
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--remote", required=True, help="SSH destination of the Linux controller"
    )
    parser.add_argument(
        "--action", choices=["sync", "ci", "deploy", "deploy-all"], required=True
    )
    parser.add_argument("--target", default="")
    parser.add_argument("--inventory", default="inventories/my-provision/inventory")
    parser.add_argument("--tags", default="")
    parser.add_argument("--forward-agent", action="store_true")
    args = parser.parse_args()
    if (
        not args.remote
        or args.remote.startswith("-")
        or any(c.isspace() for c in args.remote)
    ):
        parser.error(
            "Set DEPLOY_REMOTE to a trusted Linux SSH destination; see README.md"
        )
    if args.action == "deploy" and not args.tags.strip():
        parser.error("Specify role tags, or explicitly use deploy-all")
    if args.target.startswith("-") or not re.fullmatch(
        r"[\w.*:!&,\[\]-]*", args.target, flags=re.ASCII
    ):
        parser.error(
            "Target must be an inventory host or a noninteractive Ansible host pattern"
        )
    if args.tags and not re.fullmatch(
        r"[\w.-]+(?:,[\w.-]+)*", args.tags, flags=re.ASCII
    ):
        parser.error("Tags must be literal role names separated by commas")
    files = manifest()
    inventory = PurePosixPath(args.inventory.replace("\\", "/"))
    if (
        inventory.is_absolute()
        or ".." in inventory.parts
        or not re.fullmatch(r"[\w./-]+", str(inventory), flags=re.ASCII)
    ):
        parser.error("INVENTORY must be a relative path inside this repository")
    if args.action.startswith("deploy") and str(inventory) not in files:
        parser.error(
            "The inventory is missing or ignored by Git; it cannot be synchronized"
        )
    if args.action.startswith("deploy") and not args.target.strip():
        parser.error("A target inventory host is required")

    workspace = hashlib.sha256(f"{socket.gethostname()}:{ROOT}".encode()).hexdigest()[
        :20
    ]
    request = {
        "workspace": workspace,
        "files": files,
        "action": args.action,
        "target": args.target,
        "inventory": str(inventory),
        "tags": args.tags,
        "environment": {},
    }
    if args.action.startswith("deploy"):
        # Explicitly clear absent confirmations on the controller as well.
        request["environment"] = {
            name: os.environ.get(name, "") for name in MAINTENANCE_ENV
        }
    worker = (ROOT / "scripts" / "remote_deploy_worker.py").read_bytes()
    bootstrap = (
        "import sys; "
        "exec(compile(sys.stdin.buffer.read(int(sys.stdin.buffer.readline())), "
        "'<remote-deploy>', 'exec'))"
    )
    command = [
        "ssh",
        "-T",
        "-A" if args.forward_agent else "-a",
        "-o",
        "RemoteCommand=none",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=15",
        "-o",
        "ServerAliveInterval=15",
        "-o",
        "ServerAliveCountMax=3",
        args.remote,
        "python3 -u -c " + shlex.quote(bootstrap),
    ]
    print(f"==> Linux controller: {args.remote}", flush=True)
    with subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    ) as process:
        try:
            process.stdin.write(f"{len(worker)}\n".encode())
            process.stdin.write(worker)
            process.stdin.write(json.dumps(request).encode() + b"\n")
            process.stdin.flush()
            response = process.stdout.readline()
            if not response:
                raise ValueError(
                    "Controller exited before synchronization; check SSH and remote Python 3"
                )
            needed = json.loads(response)
            if not isinstance(needed, list) or len(needed) != len(set(needed)):
                raise ValueError("Invalid controller response")
            for name in needed:
                if name not in files:
                    raise ValueError("Controller requested an unknown file")
                remaining = files[name]["size"]
                with (ROOT / name).open("rb") as source:
                    while remaining:
                        chunk = source.read(min(CHUNK, remaining))
                        if not chunk:
                            raise ValueError(
                                f"File changed while synchronizing; retry: {name}"
                            )
                        process.stdin.write(chunk)
                        remaining -= len(chunk)
            process.stdin.close()
            print(
                f"==> Transferred {len(needed)}/{len(files)} files (content changes only)",
                flush=True,
            )
            shutil.copyfileobj(process.stdout, sys.stdout.buffer)
            return process.wait()
        except BaseException:
            process.kill()
            process.wait()
            raise


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Remote deployment failed: {error}", file=sys.stderr)
        sys.exit(1)
