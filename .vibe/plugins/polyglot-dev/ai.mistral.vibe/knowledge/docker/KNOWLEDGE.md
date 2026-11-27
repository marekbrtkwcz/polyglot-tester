---
name: docker
description: Container workflows with Docker and Podman: Dockerfile best practices, multi-stage builds, compose for local dev, rootless containers, image security, and registry/tagging discipline.
display_name: Containers (Docker/Podman)
icon: container
---

# Containers Reference (Docker & Podman)

## Dockerfile best practices

- Multi-stage builds: builder stage compiles, final stage copies only artifacts — small runtime image.
- Pin base image tags (`python:3.13-slim`, `golang:1.23-alpine`, `node:22-alpine`); `latest` is not reproducible.
- Run as non-root (`USER app`); set `WORKDIR`; copy only what's needed (`.dockerignore` for node_modules, .git, .env).
- One process per container; handle SIGTERM for graceful shutdown; expose healthcheck (`HEALTHCHECK`) when the orchestrator supports it.
- Layer ordering: dependencies before source code, so source changes don't invalidate the dependency cache.

## Compose for local dev

- `compose.yaml` for the full local stack (app + DB + cache); override files (`compose.override.yaml`) for local tweaks, never committed hacks.
- Bind mounts for source in dev (hot reload), named volumes for data; `depends_on` with `condition: service_healthy`.

## Image security

- Scan images in CI (trivy, grype, docker scout); fail on critical CVEs.
- No secrets in images or ENV — use runtime secrets (env files excluded via .dockerignore, orchestrator secrets).
- Use distroless or slim bases; keep the image updated and rebuild on base CVEs.

## Tags & registry

- Tag images with git SHA (always) + semver tag on release; never push `latest` from a random branch.
- Immutable tags: once pushed, never overwrite — rebuild and push a new tag.

## Podman

- Drop-in Docker replacement: same CLI (`alias docker=podman`), same image format (OCI), so Dockerfiles and most commands work unchanged.
- **Rootless by default**: containers run as your user, no daemon — smaller attack surface, the usual choice on shared machines and in CI.
- `podman compose` (via podman-compose or the built-in `podman compose` using compose spec) for local stacks; `podman play kube` for Kubernetes YAML.
- Pods: `podman pod create` groups containers sharing network/namespace — the Podman-native answer to compose services.
- Systemd integration: `podman generate systemd` turns containers/pods into units (`--new` for resilience on restart).
- Registries: same as Docker (docker.io, ghcr.io, ...); login via `podman login`.

## Docker vs Podman — when which

- Docker: when the team/CI already standardizes on the Docker daemon, or needs Docker-specific tooling (Docker Desktop, Swarm).
- Podman: rootless environments, hardened hosts, Kubernetes-centric workflows (pods, `play kube`), rootless CI runners.

## Official sources

- Docker docs: docs.docker.com · Dockerfile reference: docs.docker.com/reference/dockerfile · Compose spec: github.com/compose-spec/compose-spec
- Podman: podman.io · Podman CLI reference: docs.podman.io/en/latest/Commands.html · podman-compose: github.com/containers/podman-compose
- Image scanning: Trivy (aquasecurity.github.io/trivy), Grype (github.com/anchore/grype), docker scout
