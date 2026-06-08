# Docker Rules

## Docker Live Restore

`docker_daemon_options.live-restore=true` keeps containers running across Docker daemon restarts. After daemon option changes, containers with published ports may still need explicit relaunch/recreate for new networking behavior to apply. I really HATE this option, it adds a lot of unnecessary problems, never suggest to add it.
