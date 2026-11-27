---
name: ai-integration-polyglot
description: Load this skill when integrating LLM APIs into an app in JavaScript/TypeScript, Python, or Go — provider and SDK choice, prompt structure, structured output, embeddings and vector search, RAG basics, token budgets and cost/latency control, prompt-injection safety, and testing LLM-backed features.
---

# AI Integration (Polyglot)

## Provider & SDK choice

- Use the official SDK, never raw HTTP for chat/completions. Mistral first in a Mistral/Vibe stack: JS/TS — `@mistralai/mistralai`; Python — `mistralai`; the API key lives in `MISTRAL_API_KEY`. Mistral ships NO official Go SDK — in Go use an OpenAI-compatible client against `https://api.mistral.ai/v1` (e.g. `openai-go` with `option.WithBaseURL`) or the community `github.com/gage-technologies/mistral-go`. Other providers: JS/TS — Vercel AI SDK or `openai`/`@anthropic-ai/sdk`; Python — `openai`/`anthropic` SDKs, or `litellm` when multi-provider from one codebase; Go — the `genai` SDK or other provider SDKs.
- Wrap calls in one thin adapter (a port) so swapping provider or model is a config change, not a refactor.
- Model, temperature, and max tokens live in env/config, never hardcoded; log the model ID with every request so you can attribute quality and cost drift.

## Prompting essentials

- System prompt = role + constraints + output contract; user prompt = task + data. Be specific; use few-shot examples for format-sensitive output.
- For long contexts, put the instruction after the data, and delimit untrusted input with explicit markers (XML tags or triple backticks) — never concatenate raw user text into the instructions.
- Prefer structured output (JSON mode, tool/function calling, `response_format`) over asking for JSON in prose; validate the result against a schema in code.

## Embeddings & vector search

- Pick one embedding model per project and version it with the index; store vectors in pgvector, Qdrant, Pinecone, or Weaviate.
- Chunk documents at ~200–500 tokens with overlap; store source metadata (doc ID, section, URL) in every vector for attribution.
- Hybrid search (vector + keyword/BM25) beats pure vector search for exact terms like IDs and error codes.

## RAG basics

- Pipeline: retrieve → (optional rerank) → generate. Ground the answer in the retrieved chunks and make it cite sources.
- Instruct the model to say it does not know when the context is insufficient — an honest "not found" beats a confident invention.
- Budget the context window explicitly: tokens in (system + retrieved + user) vs tokens out; measure both.

## Cost, latency, reliability

- Cache repeated prompts (exact-match first, semantic cache when worth it); batch embedding jobs; stream long generations for UX.
- Set timeouts, retry 429/5xx with exponential backoff + jitter, and define a fallback (cheaper model or a graceful "try again" message) — never fail silently.
- Track prompt/completion tokens and cost per feature; alert on drift after a prompt or model change.

## Safety

- Treat user input and retrieved documents as untrusted: prompt injection means retrieved text must never execute as instructions — keep tool calls on an allowlist and validate arguments server-side against a schema.
- Never put secrets in prompts; redact PII before sending data to a third-party API and check data-residency/privacy requirements first.

## Testing LLM-backed features

- Keep a golden set of input→expected-output cases per prompt template; score deterministically where possible (schema validation, exact match) and with a rubric LLM-as-judge for the rest.
- Regression-gate every prompt or model change against the golden set; record the run (model, prompt version, scores).
- Test the failure paths too: timeout, malformed JSON output, and injection attempts embedded in user content.

## Per-language notes

- **JS/TS**: Mistral `@mistralai/mistralai` (`new Mistral({ apiKey })`, then `client.chat.complete` / `client.chat.stream`); Vercel AI SDK — `generateText`/`streamText`, `generateObject` with a zod schema for structured output.
- **Python**: Mistral `mistralai` (`Mistral(api_key=os.environ["MISTRAL_API_KEY"])`, then `client.chat.complete`); other providers via their SDKs or `litellm`; pydantic + `response_format` (or `instructor`) for structured output; `tenacity` for retries with backoff.
- **Go**: no official Mistral SDK — call the OpenAI-compatible endpoint `https://api.mistral.ai/v1` with `openai-go` (`option.WithBaseURL(...)`) or use community `github.com/gage-technologies/mistral-go`; Google `genai` SDK with response schema via `*genai.Schema`; `errgroup` + context for concurrent calls.

## Related

- `observability-polyglot` — token/cost metrics, latency traces, and drift alerting belong in the same signals as the rest of the app.
- `security` — API-key handling and injection hardening around the integration points.
- `testing` — where the golden-set regression gate for prompts lives in the suite.
- `api-design-polyglot` — if the LLM feature is exposed as an endpoint, the error-envelope and rate-limiting rules apply.
