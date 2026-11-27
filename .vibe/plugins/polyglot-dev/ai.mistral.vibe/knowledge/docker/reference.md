# Container Diagnostics Reference

Companion to the containers knowledge: the commands for "why is my image
big", "what is failing inside", and "is it safe to ship".

## Image size — where the bytes went

- Biggest offenders: `docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"`.
- Layer-by-layer: `docker history <image>` — the fat layer is the suspect.
- Inside the layers: `dive <image>` — shows wasted bytes (files overwritten
  or deleted in later layers still paid for in earlier ones).
- Final-stage sanity: a multi-stage build's runtime image must not contain
  the compiler, `node_modules`, or `.git` — if it does, the stage boundary
  is in the wrong place.

## Debugging a running container

- App output: `docker logs --tail 100 -f <ctr>`.
- Look inside: `docker exec -it <ctr> sh` (slim images ship `sh` only).
- Why did it exit: `docker inspect -f "{{.State.ExitCode}} {{.State.OOMKilled}}" <ctr>`.
- Which service failed its healthcheck: `docker compose up --wait` (waits
  for healthchecks) followed by `docker compose ps`.
- Grab a file without exec: `docker cp <ctr>:/path ./local`.

## Pre-ship security gate

- CVEs: `trivy image --severity HIGH,CRITICAL <image>` or `grype <image>`;
  fail CI on critical findings with a fix available.
- Secrets: `docker history` prints ARG/ENV values — a secret visible there
  is baked into the image config forever; rebuild with runtime secret injection.
- Running as root? `docker inspect -f "{{.Config.User}}" <image>` — an empty
  string means root; the Dockerfile needs a `USER`.

## Podman — where it differs

- Everyday commands are the same: `podman ps -a`, `podman logs`,
  `podman inspect`, `podman cp`.
- Rootless: ports below 1024 need slirp4netns port handling — prefer
  publishing ports >= 1024 in dev setups.
- `podman generate systemd --new <ctr>` — a unit file that recreates the
  container on start; `podman play kube` runs the same YAML Kubernetes uses.
