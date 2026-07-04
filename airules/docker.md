# Docker Rules

## Docker Live Restore

`docker_daemon_options.live-restore=true` keeps containers running across Docker daemon restarts. After daemon option changes, containers with published ports may still need explicit relaunch/recreate for new networking behavior to apply. I really HATE this option, it adds a lot of unnecessary problems, never suggest to add it.

## Docker Volume Setup

When a local mount/setup issue causes `EXDEV`/cross-device link or permission errors, fix Docker volumes, ownership, and data placement first. Do not add runtime fallback code unless explicitly requested.
