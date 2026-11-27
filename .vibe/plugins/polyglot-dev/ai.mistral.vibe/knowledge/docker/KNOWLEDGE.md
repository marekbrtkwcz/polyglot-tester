---
name: docker
description: Docker and container workflows: Dockerfile best practices, multi-stage builds, compose for local dev, image security, and registry/tagging discipline.
display_name: Docker
icon: container
---

# Docker Reference

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

## Official sources

- Docker docs: docs.docker.com · Dockerfile reference: docs.docker.com/reference/dockerfile · Compose spec: github.com/compose-spec/compose-spec · Trivy: aquasecurity.github.io/trivy
