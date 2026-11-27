# Web & APIs in Go

## Framework choice

- **net/http (stdlib + router)**: Go 1.22+ has method+pattern routing (`mux.HandleFunc(\"GET /users/{id}\", h)`) and path values (`r.PathValue(\"id\")`) — start here; add a router (chi, gorilla/mux, huma) only when you need groups/middleware chains.
- **gin / echo / fiber**: batteries-included, fast; pick one team-wide. Fiber is fasthttp-based (different request model — don't mix idioms).

## Handlers

- One handler per route; keep them thin: parse → call service → write response.
- Decode JSON with `json.NewDecoder(r.Body).Decode(&v)`; set `DisallowUnknownFields()` when strictness matters; cap body size (`http.MaxBytesReader`).
- Validate input (go-playground/validator or hand-rolled); never trust path/query params — parse and range-check them.

## Middleware

- Chain small middlewares: request ID, logging, recover (panic → 500, never crash the server), auth, timeouts.
- Order matters: recover outermost, then logging, then auth, then timeout closest to the handler.

## Responses & errors

- Consistent envelope: `{ "data": ... }` / `{ "error": { "code", "message" } }`; map domain errors to status codes in one place.
- `http.Error` for plain text errors; JSON envelope for APIs. Never leak stack traces.

## Graceful shutdown

```go
srv := &http.Server{Addr: ":8080", Handler: mux}
go func() { srv.ListenAndServe() }()
quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGTERM, syscall.SIGINT)
<-quit
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
srv.Shutdown(ctx) // drains in-flight requests
```

## Per-route context

- Use `r.Context()` for cancellation; `context.WithTimeout` per request at the middleware level.
- Put request ID / user ID in context values with typed keys (see `context`).

## Testing handlers

- `httptest.NewRecorder` + `httptest.NewRequest` — test handlers without a network.
- Table-driven tests over routes: method, path, body, want status, want JSON.

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
