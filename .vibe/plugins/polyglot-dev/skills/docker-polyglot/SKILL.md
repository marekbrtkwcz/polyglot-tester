---
name: docker-polyglot
description: Load this skill when containerizing a JS/TS, Python, or Go app with Docker or Podman — Dockerfile best practices, multi-stage builds per language, compose for local dev, rootless Podman, image scanning, and tagging discipline.
---

# Containers (Polyglot: Docker & Podman)

Full reference: knowledge `docker`. Docker and Podman are drop-in compatible (same CLI, same OCI images) — write Dockerfiles once, run with either.

## Dockerfile rules (all languages)

- **Multi-stage builds**: builder stage compiles, final stage copies only artifacts — small runtime image.
- Pin base image tags (`node:22-alpine`, `python:3.13-slim`, `golang:1.23-alpine`); `latest` is not reproducible.
- Layer ordering: dependencies before source, so source changes don't invalidate the dependency cache.
- Run as non-root (`USER app`), set `WORKDIR`, copy only what's needed (`.dockerignore`: `node_modules`, `.git`, `.env`, `__pycache__`).
- One process per container; handle SIGTERM for graceful shutdown; `HEALTHCHECK` when the orchestrator supports it.

## Multi-stage per language

- **JS/TS**: `FROM node:22-alpine AS build` → `npm ci && npm run build` → final stage copies `dist/` + `node_modules --omit=dev`; serve with a tiny static server or run the Node server.
- **Python**: build stage installs deps into a venv (`uv pip install` or `pip install --user`), final stage `python:3.13-slim` copies the venv + source; run with `python -m yourapp`.
- **Go**: `FROM golang:1.23-alpine AS build` → `go build -o /app/bin ./cmd/app` → final `FROM alpine` (or distroless) copies the static binary; CGO_ENABLED=0 for a fully static binary.

## Compose for local dev

- `compose.yaml` for the full local stack (app + DB + cache); `depends_on` with `condition: service_healthy`.
- Bind-mount source in dev (hot reload), named volumes for data; keep local overrides in `compose.override.yaml`.

## Image security

- Scan in CI (trivy, grype, docker scout); fail on critical CVEs; rebuild on base-image CVEs.
- No secrets in images or `ENV` — runtime secrets only (orchestrator secrets / env files excluded via `.dockerignore`).
- Prefer slim/distroless bases.

## Tags & registry

- Tag with git SHA (always) + semver on release; never push `latest` from a feature branch.
- Immutable tags: once pushed, never overwrite — push a new tag.

## Podman specifics

- Rootless by default, no daemon — the usual choice on shared machines and rootless CI runners; alias `docker=podman`.
- `podman compose` for compose files, `podman play kube` for Kubernetes YAML, pods (`podman pod create`) group containers sharing a network namespace.
- `podman generate systemd --new` turns containers/pods into resilient units.

## When which

- **Docker**: team already standardized on the daemon, Docker Desktop/Swarm tooling needed.
- **Podman**: rootless environments, hardened hosts, Kubernetes-centric workflows, rootless CI.
