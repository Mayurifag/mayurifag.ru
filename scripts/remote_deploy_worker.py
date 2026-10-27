"""Linux half of remote_deploy.py; received over SSH, never installed globally."""

import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile


def safe_path(root, name):
    relative = PurePosixPath(name)
    if (
        not name
        or relative.is_absolute()
        or ".." in relative.parts
        or str(relative) != name
    ):
        raise ValueError("Unsafe synchronization path")
    path = root / name
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError("Symlink in controller workspace; refusing to synchronize")
    return path


def save_json(path, data):
    temporary = safe_path(path.parent, path.with_suffix(".tmp").name)
    try:
        temporary.write_text(json.dumps(data), encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def synchronize(root, state_path, files):
    previous = json.loads(state_path.read_text()) if state_path.exists() else []
    for name in previous:
        safe_path(root, name)
    for name in files:
        safe_path(root, name)
    # Remove stale managed paths first to support file/directory replacements.
    for name in sorted(set(previous) - set(files), reverse=True):
        path = safe_path(root, name)
        if path.exists():
            path.unlink()
        parent = path.parent
        while parent != root:
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent
    needed = []
    for name, metadata in files.items():
        path = safe_path(root, name)
        current_hash = None
        if path.exists():
            with path.open("rb") as source:
                current_hash = hashlib.file_digest(source, "sha256").hexdigest()
        if current_hash != metadata["sha256"]:
            needed.append(name)
    # Track in-flight paths so interrupted initial uploads can be reconciled too.
    save_json(state_path, sorted(files))
    print(json.dumps(needed), flush=True)
    for name in needed:
        metadata = files[name]
        path = safe_path(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=".sync-", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            digest = hashlib.sha256()
            remaining = metadata["size"]
            with os.fdopen(descriptor, "wb") as destination:
                while remaining:
                    chunk = sys.stdin.buffer.read(min(1024 * 1024, remaining))
                    if not chunk:
                        raise ValueError("Interrupted upload; deployment not started")
                    destination.write(chunk)
                    digest.update(chunk)
                    remaining -= len(chunk)
            if digest.hexdigest() != metadata["sha256"]:
                raise ValueError("Source changed during upload; retry deployment")
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    for name, metadata in files.items():
        safe_path(root, name).chmod(0o700 if metadata["executable"] else 0o600)


def main():
    os.umask(0o077)
    request = json.loads(sys.stdin.buffer.readline())
    workspace = request["workspace"]
    if not re.fullmatch(r"[0-9a-f]{20}", workspace):
        raise ValueError("Invalid workspace identifier")
    base = Path.home() / ".cache" / "mayurifag-deploy" / workspace
    safe_path(Path.home(), base.relative_to(Path.home()).as_posix())
    base.mkdir(parents=True, exist_ok=True)
    base.chmod(0o700)
    with safe_path(base, "lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError(
                "Another sync/deployment is using this workspace"
            ) from None
        root = safe_path(base, "repo")
        state = safe_path(base, "files.json")
        if root.exists() and not state.exists() and any(root.iterdir()):
            raise ValueError("Refusing to adopt a nonempty unmanaged workspace")
        root.mkdir(exist_ok=True)
        root.chmod(0o700)
        # Persist ownership before the first transfer so interrupted initial syncs can retry.
        if not state.exists():
            save_json(state, [])
        action = request["action"]
        if action not in {"sync", "ci", "deploy", "deploy-all"}:
            raise ValueError("Unknown controller action")
        if action != "sync":
            for tool in (
                ["ansible-playbook"] if action.startswith("deploy") else ["make"]
            ):
                if not shutil.which(tool):
                    raise ValueError(f"Missing controller dependency: {tool}")
        synchronize(root, state, request["files"])
        print(f"==> Synchronized private workspace: {root}", flush=True)
        if action == "sync":
            return 0
        if action == "ci":
            command = [
                "make",
                "--no-print-directory",
                "DEPLOY_REMOTE=",
                "OS=Linux",
                "ci",
            ]
        else:
            # Do not interpolate Ansible host patterns into a Make/shell recipe.
            command = [
                "ansible-playbook",
                "-i",
                request["inventory"],
                "provisioning.yml",
                "--limit",
                request["target"],
            ]
            if action == "deploy":
                command.extend(["--tags", request["tags"]])
        environment = os.environ.copy()
        environment.update(request["environment"])
        # Do not inherit Make jobserver/command-line overrides from another invocation.
        environment.pop("MAKEFLAGS", None)
        environment.pop("MFLAGS", None)
        environment.pop("MAKEOVERRIDES", None)
        return subprocess.call(
            command, cwd=root, env=environment, stdin=subprocess.DEVNULL
        )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"Controller failed: {error}", file=sys.stderr)
        sys.exit(1)
