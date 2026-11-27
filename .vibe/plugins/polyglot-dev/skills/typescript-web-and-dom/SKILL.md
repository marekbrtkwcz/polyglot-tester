---
name: typescript-web-and-dom
description: Load this skill for browser-side JS/TS: DOM APIs, fetch and networking, storage, events, accessibility basics, and framework-agnostic browser patterns.
---

# Web & DOM (Browser JS/TS)

## DOM

- Select with `querySelector`/`getElementById`; cache references — DOM queries are not free.
- `textContent` for plain text (never `innerHTML` with data); `createElement` + properties over HTML strings.
- Event delegation: one listener on a parent for many children.
- `classList` for classes; `dataset` for `data-*` attributes.

## Networking

- `fetch` with `AbortController` for cancellation and timeouts; check `response.ok`; parse JSON in try/catch (`response.json()` throws on invalid JSON).
- Don't retry non-idempotent requests blindly; use exponential backoff + jitter for retries.
- WebSocket/SSE for realtime: handle reconnect with backoff and `Last-Event-ID` for SSE.

## Storage

- `localStorage`/`sessionStorage` for small client state; `IndexedDB` (or idb wrapper) for larger structured data.
- Never store tokens in localStorage if avoidable — `HttpOnly` cookies are safer against XSS.

## Events & timing

- `addEventListener` with `{ once: true }` where appropriate; always remove listeners you add (`AbortSignal` option: `addEventListener('x', fn, { signal })` auto-removes).
- `requestAnimationFrame` for visual updates; `IntersectionObserver`/`ResizeObserver` instead of scroll/resize polling.

## Accessibility

- Semantic HTML first (button, nav, main, label); ARIA only when semantics fall short.
- Keyboard operability, visible focus, labels for inputs, alt text, sufficient contrast; test with axe-core.

## Related

- Knowledge `javascript-typescript` — JS/TS toolchain and conventions: package managers, Biome linting, tsconfig strictness, everyday commands.
