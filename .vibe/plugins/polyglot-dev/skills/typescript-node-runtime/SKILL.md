---
name: typescript-node-runtime
description: Load this skill for Node.js-specific development in TS: runtime versions, ESM/CJS, streams and buffers, CLI tools, env/config handling, graceful shutdown, and process signals.
---

# Node.js Runtime (TS)

## Versions & modules

- Use current LTS; check `engines` and CI matrix against supported versions (nodejs.org release schedule).
- ESM (`type: module`) for new projects; know the interop pitfalls: `__dirname` doesn't exist in ESM (`import.meta.url` + `fileURLToPath`), `require` of ESM needs Node 22+/flag.
- In ESM, import file extensions explicitly (`./foo.js` even when the source is `./foo.ts` under ts-node/tsx conventions).

## Streams & buffers

- Stream big data: `fs.createReadStream` → `pipeline` → `createWriteStream`; never `readFileSync` on large files on hot paths.
- `Buffer` for binary; `StringDecoder` for chunked text; avoid `buf.toString()` splitting multibyte chars mid-chunk.

## CLI tools

- argv parsing: `node:util` `parseArgs` for simple flags; `commander`/`yargs`/`cac` for full CLIs.
- stdout for output, stderr for diagnostics; exit codes: 0 ok, 1 generic error, 2 usage error. Test exit codes and stdout content.

## Config & env

- `process.env` with validation at startup (zod schema) — fail fast on missing/invalid env, don't discover at runtime.
- 12-factor: config in env, secrets out of code; `.env` only locally (dotenv), never committed.

## Process lifecycle

- Handle `SIGTERM`/`SIGINT`: stop accepting work, close servers (`server.close()`), drain queues, then exit; set a forced-exit timeout.
- `process.on('uncaughtException'/'unhandledRejection')` to log, then exit non-zero.
- `node --watch` for local dev; `tsx`/`ts-node` for running TS directly (not for production).

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
