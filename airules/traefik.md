# Traefik Rules

Keep the Traefik CrowdSec middleware as the real plugin and keep `/plugins-storage` persistent. Do not replace it with a permanent no-op fallback; only use no-op live config as a temporary emergency recovery step.

Traefik v3.7 prints the encoded-character startup warning unconditionally upstream; config cannot remove it. Do not hide it by lowering log verbosity.
