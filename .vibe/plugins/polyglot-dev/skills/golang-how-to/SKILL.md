---
name: golang-how-to
description: Load this skill when you need a concrete recipe for a common Go task: copy-paste-ready patterns for HTTP servers, JSON APIs, file handling, env config, graceful shutdown, and more.
---

# Go How-To Recipes

Copy, adapt, delete what you don't need.

## HTTP server with graceful shutdown

```go
srv := &http.Server{Addr: ":8080", Handler: mux, ReadHeaderTimeout: 5 * time.Second}
go func() {
    if err := srv.ListenAndServe(); err != http.ErrServerClosed {
        log.Fatal(err)
    }
}()
quit := make(chan os.Signal, 1)
signal.Notify(quit, os.Interrupt)
<-quit
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
srv.Shutdown(ctx)
```

## JSON API handler

```go
func writeJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(v) // check err in prod code
}
func decodeJSON(r *http.Request, v any) error {
    r.Body = http.MaxBytesReader(nil, r.Body, 1<<20) // 1 MiB cap
    defer r.Body.Close()
    return json.NewDecoder(r.Body).Decode(v)
}
```

## Read env with defaults + required

```go
func env(key, fallback string) string {
    if v, ok := os.LookupEnv(key); ok { return v }
    return fallback
}
func mustEnv(key string) string {
    v, ok := os.LookupEnv(key)
    if !ok { log.Fatalf("missing env %s", key) }
    return v
}
```

## Read/write files safely

```go
data, err := os.ReadFile(path)                      // whole file
w := bufio.NewWriter(f)                             // buffered writes
lines := bufio.Scanner over file                    // line by line, big files
os.WriteFile(path, data, 0o600)                     // secrets: 0600, not 0644
```

## Worker + shutdown

```go
g, ctx := errgroup.WithContext(context.Background())
g.Go(func() error { return workerLoop(ctx) })
<-quitSignal
g.Wait() // with ctx cancelled first
```

## Retry with backoff

```go
backoff := time.Second
for i := 0; i < 5; i++ {
    err := call()
    if err == nil { break }
    if i == 4 { return err }
    time.Sleep(backoff + time.Duration(rand.Int63n(int64(backoff/2)))) // jitter
    backoff *= 2
}
```

## CLI flags

```go
port := flag.Int("port", 8080, "listen port")
flag.Parse()
```

## Related

- Knowledge `go` — Go toolchain and conventions: go.mod, table-driven tests, error wrapping, golangci-lint, everyday commands.
