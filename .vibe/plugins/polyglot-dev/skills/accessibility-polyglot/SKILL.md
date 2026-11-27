---
name: accessibility-polyglot
description: Load this skill when building or auditing accessible UI in JavaScript/TypeScript, Python-generated HTML, or Go templates — WCAG 2.2 AA: semantics, keyboard, screen readers, contrast, focus, and automated a11y testing per stack.
---

# Accessibility (Polyglot, WCAG 2.2 AA)

## Semantics first

- Use native elements with their built-in semantics: `<button>`, `<nav>`, `<main>`, `<label>`, `<dialog>`. ARIA only when native semantics genuinely fall short — and then correctly (`role`, `aria-label`, `aria-describedby`).
- One `h1` per page; heading levels don't skip. Landmarks: `header`/`nav`/`main`/`footer`.
- Forms: every input has a visible `<label for>` (not placeholder-as-label); errors announced via `aria-live` or linked with `aria-describedby` + `aria-invalid`.

## Keyboard & focus

- Everything operable by mouse must be operable by keyboard; visible focus indicator (`:focus-visible`, never `outline: none` without replacement).
- Focus management: move focus into a dialog on open, return it on close; trap focus inside modal dialogs; skip-link to main content.
- No keyboard traps; custom widgets need arrow-key/Enter/Escape behavior per ARIA APG patterns.

## Screen readers & visual

- Meaningful alt text (empty `alt=""` for decorative images); text alternatives for charts (data table fallback).
- Contrast: 4.5:1 for normal text, 3:1 for large text and UI components. Don't convey meaning by color alone.
- Respect `prefers-reduced-motion`; support 200% zoom without loss of content (test at 400% for reflow).

## Automated testing per stack

- **JS/TS**: axe-core in unit/E2E tests (`@axe-core/playwright` in Playwright, `jest-axe` in Vitest) — assert zero critical/serious violations per page; also manual keyboard + screen-reader pass (NVDA/VoiceOver).
- **Python** (Django/Flask/Jinja templates): `axe` via Playwright against rendered pages; `html5lib`/template linting for unclosed tags; check `django-axe` or equivalent smoke hooks.
- **Go** (html/template): templates are just as vulnerable — same axe/Playwright pass against rendered output; escape by default (Go does), watch `template.HTML` misuse.
- Automated tools catch ~30-40% of issues — manual keyboard/screen-reader testing is required for sign-off.

## Process

- a11y checks in CI as test failures, not a separate report; new components ship with their a11y test.
- Fix findings by WCAG success criterion; prioritize blockers (keyboard traps, missing names) over contrast nits.
