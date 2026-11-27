---
name: i18n-polyglot
description: Load this skill when internationalizing an app in JavaScript/TypeScript, Python, or Go — locale switching, translation files, date/number/currency formatting, pluralization, RTL, and fallback behavior.
---

# Internationalization (Polyglot)

## Architecture

- Externalize all user-facing strings into message catalogs — never string literals in templates/code. One catalog per locale.
- Key-based messages (`welcome_user` with `{name}` interpolation), not sentence-fragments concatenated.
- Locale from user preference (account setting) > `Accept-Language` header > default; store the choice; never guess from IP alone.

## Per-language tooling

- **JS/TS**: `react-intl` / `next-intl` / `i18next` — ICU message format (`{count, plural, one {...} other {...}}`); `Intl.NumberFormat`, `Intl.DateTimeFormat`, `Intl.RelativeTimeFormat`, `Intl.ListFormat` for formatting (never hand-rolled).
- **Python**: `gettext` (stdlib) or `Babel` for extraction/plurals; `babel.dates/numbers` for formatting; Django has built-in i18n (`{% trans %}`, `{% blocktrans %}`).
- **Go**: `golang.org/x/text/message` for number/date formatting and message catalogs; `text/template` with locale-aware data; plurals via `x/text` selectors or explicit forms.

## Formatting rules

- Dates/times: always locale-aware (`Intl.DateTimeFormat(locale)`, `babel.dates.format_date`, `message.NewPrinter(locale)`); store instants in UTC, render in the user's zone.
- Numbers/currency/percent: locale-aware grouping and symbols; never `toFixed(2)` for display of money.
- Never concatenate translated fragments to build sentences — word order differs by language; use full-sentence messages with placeholders.

## Pluralization & gender

- Use the framework's plural rules (ICU) — Slavic languages have 3+ plural forms; test with Polish/Czech/Arabic examples.
- Avoid gendered strings where possible; when needed, use ICU `select`.

## RTL

- Set `dir="rtl"` per locale on `<html>`; use logical CSS properties (`margin-inline-start`, not `margin-left`); mirror icons that imply direction.
- Test layout with a RTL locale (Arabic/Hebrew) — screenshots catch mirrored-icon bugs.

## Fallbacks & testing

- Missing translation → fall back to the default locale and log/monitor the gap (don't show the raw key to users in prod).
- Tests: pseudo-localization pass (expand strings ~30% with accents) to catch hardcoded-width layouts; snapshot key completeness across locales in CI.
