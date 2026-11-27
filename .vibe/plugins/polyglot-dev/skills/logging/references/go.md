# Go Logging

## Default: log/slog (stdlib, Go 1.21+)

Structured logging built in:

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
logger.Info("user logged in", "user_id", u.ID, "ip", r.RemoteAddr)
```

- Levels: Debug < Info < Warn < Error; set the minimum in `HandlerOptions.Level` (from env in prod).
- Attributes: key-value pairs as args (`"key", value`) — use `slog.String`, `slog.Int`, `slog.Duration`, `slog.Any` helpers or plain pairs.
- Context: `logger.InfoContext(ctx, ...)` — handlers can extract ctx values (request ID).
- Groups: `slog.Group("request", "method", r.Method, "path", r.URL.Path)`.

## Choosing a logger

- Set `slog.SetDefault(logger)` once at startup so `slog.Info(...)` works everywhere.
- Replace the handler, keep the API: text handler for dev (`slog.NewTextHandler`), JSON for prod.
- **zap** (uber) — when you need max throughput in hot paths (allocation-free API); **zerolog** — similar, fluent style. Both can be plugged into slog via handler adapters, so you can switch output without changing call sites.

## What to log

- One line per event, structured fields over formatted strings: `logger.Info("order failed", "order_id", id, "err", err)` — never `fmt.Sprintf` the whole message.
- Include correlation: request ID from ctx, user ID, trace ID (OpenTelemetry).
- Log at the level that matches actionability: Error = pager, Warn = investigate, Info = audit trail, Debug = local dev.

## What NOT to log

- Passwords, tokens, full credit cards — redact or drop fields; never log raw request bodies with credentials.
- Sensitive personal data (GDPR): log IDs, not emails/names.
- Every loop iteration at Info — sample or aggregate.

## Errors + logging

- Log an error once, at the layer that decides the response; wrap with `%w` on the way up, log at the top.
- `logger.Error("request failed", "err", err)` — slog prints the error chain readably.

## Testing

- Inject the logger (field or param), in tests use `slog.New(slog.NewTextHandler(io.Discard, nil))` to silence, or a buffer handler to assert on output.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
