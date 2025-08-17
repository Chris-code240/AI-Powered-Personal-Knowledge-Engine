## Let's Do Something Awesome!

# AI-Powered Personal Knowledge Engine — Architecture & Roadmap

A local-first, privacy-preserving system that ingests your personal knowledge (docs, code, web pages, videos), builds semantic indices, and answers natural-language questions across your life’s data.

---

## 1) High-Level Architecture

```
+---------------------+         +-----------------------------+         +---------------------------+
|  Sources            |  --->   |  Ingestion & Normalization  |  --->   |  NLP/IR Pipeline          |
|  - Files (PDF, md)  |         |  - Watchers (fs, rss)       |         |  - Chunking               |
|  - Web bookmarks    |         |  - Extractors (PDF, HTML)   |         |  - Embeddings (text/code) |
|  - Code repos       |         |  - Transcribers (audio)     |         |  - NER/Keywords           |
|  - Videos/Audio     |         |  - Metadata Enrichment      |         |  - Summaries              |
+---------------------+         +-----------------------------+         +---------------------------+
                                                                            |
                                                                            v
                                                                  +-------------------+
                                                                  | Storage Layer     |
                                                                  | - Vector DB       |
                                                                  | - Doc Store (SQL) |
                                                                  | - Blob Store      |
                                                                  +-------------------+
                                                                            |
                                                                            v
+----------------------+       +--------------------+            +------------------------+
| Query Interfaces     | --->  | Retrieval Engine   |  <------> | Orchestrator/Indexer   |
| - CLI                |       | - Hybrid (BM25+VEC)|            | - Scheduler/Workers    |
| - Web UI (FastAPI)   |       | - RAG w/ reranking |            | - Pipelines/Retry DLQ  |
| - Chat Bot (tg/discord)|     | - QA/Summarization |            | - Versioning           |
+----------------------+       +--------------------+            +------------------------+
```

**Principles:** local-first by default, modular, event-driven, fault-tolerant, incremental indexing, reproducible pipelines.

---

## 2) Tech Stack (swappable)

* **Core**: Python 3.11+, FastAPI, Pydantic, Typer (CLI)
* **NLP/IR**: sentence-transformers, HuggingFace Transformers, spaCy, rapidfuzz, rank\_bm25
* **ASR**: Whisper (small/medium, local)
* **Storage**:

  * Vector: FAISS (local) → Milvus/Weaviate (optional)
  * Relational: SQLite → Postgres (optional)
  * Blob: local filesystem → S3-compatible (optional)
* **Workers**: Celery/Arq + Redis, or asyncio queues
* **UI**: FastAPI + HTMX/Tailwind (or React), WebSocket streaming
* **Observability**: Rich + Loguru; Prometheus (metrics); SQLite event log
* **Packaging**: Poetry/uv; Docker (optional)

---

## 3) Data Model

### 3.1 Entities

* **Document**(id, path/url, source\_type, mime, created\_at, added\_at, content\_hash)
* **Chunk**(id, document\_id, ord, text, tokens, summary)
* **Embedding**(chunk\_id, model, vector, dim, ts)
* **Metadata**(document\_id, key, value)
* **Entity**(id, type, span, canonical\_name, doc\_id, chunk\_id)
* **Link**(from\_chunk\_id, to\_chunk\_id, score, relation)
* **Event**(id, type, payload, status, retries, ts) — for ingestion/processing

### 3.2 Tables

* `documents`, `chunks`, `embeddings`, `entities`, `links`, `events`, `tags`

### 3.3 Indexes

* BM25 over `chunks.text`
* FAISS IVF/Flat over `embeddings.vector`
* `GIN`/FTS5 index on text (SQLite FTS5 or Postgres tsvector)

---

## 4) Pipelines & Orchestration

### 4.1 Ingestion

* **Watchers**: filesystem (watchdog), bookmarks (Pocket/Instapaper export), RSS, Git repos (local path), manual upload
* **Extract**: pdfminer/pymupdf for PDFs; trafilatura/readability for HTML; AST for code; ffmpeg+whisper for audio/video
* **Normalize**: dedupe by content hash; unify to UTF-8 markdown-like canonical text; attach metadata (title, author, time)

### 4.2 Processing

1. **Chunking**: token-aware sliding windows (e.g., 800–1200 tokens with overlap)
2. **Summarize**: per-chunk TL;DR + per-document abstract
3. **NER/Keyphrases**: spaCy + simple RAKE variant
4. **Embeddings**: text model (e.g., `all-MiniLM-L6-v2`) + optional code model for repos
5. **Store**: upsert vectors → vector DB; chunks → SQL; blobs → fs
6. **Linking**: cross-chunk similarity graph + temporal/link-based edges

### 4.3 Scheduling & Reliability

* Job queue with statuses: `QUEUED → RUNNING → DONE/FAILED` with retry/backoff
* Dead-letter queue (DLQ) & replay
* Idempotency keys (content\_hash)

---

## 5) Retrieval & QA (RAG)

### 5.1 Query Flow

```
User query → query parser → (a) lexical (BM25) + (b) semantic (FAISS)
→ union + re-rank (cross-encoder or Reciprocal Rank Fusion)
→ context window assembly (diversity-aware) → LLM (local or API) for answer/sum
→ citations (chunk ids with scores) → UI render
```

### 5.2 Modes

* **Search**: ranked chunks with facets (time, source, tag)
* **Ask**: conversational QA with citations & follow-ups
* **Browse**: document view with auto-outline & highlights
* **Timeline**: heatmap of when knowledge entered the graph

---

## 6) API Surface (FastAPI)

* `POST /ingest` {path|url, tags} → enqueue
* `GET /documents/{id}` → metadata + outline
* `GET /search` ?q=\&k=\&filters= → results
* `POST /ask` {query, filters} → streamed answer + citations
* `GET /chunks/{id}` → text
* `GET /events` → recent pipeline activity

---

## 7) CLI (Typer)

```
pke ingest path ./notes
pke ingest url https://...
pke status
pke reindex --since 2025-01-01
pke search "graph neural networks"
pke ask "What did I learn about Rust lifetimes?"
```

---

## 8) MVP → v1 Milestones

**M0 – Skeleton (1–2 weeks)**

* FastAPI, Typer CLI, SQLite, FAISS
* Ingest PDFs + Markdown
* Chunk → embed → search (BM25 + FAISS)

**M1 – RAG & Citations (1–2 weeks)**

* Re-rank & context assembly
* QA endpoint with streaming
* Web UI basics: search, results, doc viewer

**M2 – Multimedia + NER (2 weeks)**

* Whisper transcription for audio/video
* spaCy NER + keyphrase tags
* Timeline view

**M3 – Reliability & Scale (2–3 weeks)**

* Job queue + DLQ + retries
* Deduplication + versioning
* Configurable embedding backends

**M4 – Cross-Linking & Graph (1–2 weeks)**

* Similarity graph, related notes, backlink panel
* Export/import of indices

---

## 9) Directory Layout

```
repo/
  app/
    api/           # FastAPI routers
    core/          # settings, logging, DI
    db/            # SQL models, migrations
    ingest/        # watchers, extractors, normalizers
    nlp/           # chunk, embed, ner, summarize
    retriever/     # bm25, vector, fusion, rerank
    rag/           # context assembly, answerer
    workers/       # queue consumers
    ui/            # web frontend
  scripts/
  tests/
  docs/
```

---

## 10) Key Algorithms (concise)

* **Token-aware chunking**: keep semantic boundaries (headings, paragraphs); back-off if tokens exceed window
* **Hybrid retrieval**: RRF: `score = Σ (1 / (k + rank_i))`
* **Diversity-aware context**: MMR with λ to balance relevance vs novelty
* **Cross-encoder rerank** (optional): small bi-encoder for speed, cross for top-50

---

## 11) Observability & Metrics

* Ingestion throughput (docs/min), failure rate
* Index freshness (avg time to indexed)
* Query P95 latency
* RAG utility: click-through on citations, answer acceptance
* Disk usage per corpus/source

---

## 12) Privacy & Security

* Local by default; opt-in for any external API
* Configurable PII redaction before storage
* Secrets via `.env`; per-source allowlist/denylist
* Export & full wipe commands

---

## 13) Testing Strategy

* Unit: extractors, chunker, embedder stubs
* Integration: end-to-end ingestion→search on a mini corpus
* Golden files: stable answers for known questions
* Property tests: idempotency on re-ingest

---

## 14) Risk Register & Mitigations

* **Model drift / embedding swaps** → store `model_name`, `dim`, and migrate with dual-index during transition
* **Large binaries** → transcode & store low-bitrate transcripts; offload blobs
* **Latency** → cache warm top queries; pre-compute doc abstracts
* **Hallucinations** → strict citation requirement; abstain if confidence low

---

## 15) Stretch Features (for extra shine)

* Browser extension → one-click send to engine
* Email ingestion (IMAP label)
* Cross-device sync via encrypted snapshot bundles
* Graph visualization (PyVis) with interactive jumping
* Schedule-aware memory: “What did I read last week about X?”

---

## 16) Minimal Code Starters (pseudo/real-ish)

**Chunking**

```python
from itertools import accumulate

def chunk(paragraphs, max_tokens=1000, overlap=150, tok=len):
    buf, size = [], 0
    for p in paragraphs:
        t = tok(p)
        if size + t > max_tokens:
            yield "\n\n".join(buf)
            # overlap by last N tokens (approx):
            buf = buf[-1:]
            size = tok(buf[0]) if buf else 0
        buf.append(p); size += t
    if buf: yield "\n\n".join(buf)
```

**RRF Fusion**

```python
def rrf(*ranked_lists, k=60):
    scores = {}
    for lst in ranked_lists:
        for rank, id_ in enumerate(lst, 1):
            scores[id_] = scores.get(id_, 0) + 1.0 / (k + rank)
    return [id_ for id_, _ in sorted(scores.items(), key=lambda x: -x[1])]
```

**Context Assembly (MMR)**

```python
import numpy as np

def mmr(query_vec, cand_vecs, λ=0.7, top_k=8):
    S, chosen = [], []
    while len(chosen) < top_k and cand_vecs:
        rel = [q @ c for c in cand_vecs]
        div = [max((c @ cand_vecs[i] for i in chosen), default=0) for c in cand_vecs]
        scores = [λ*r - (1-λ)*d for r,d in zip(rel, div)]
        i = int(np.argmax(scores))
        chosen.append(i); S.append(cand_vecs.pop(i))
    return chosen
```

---

## 17) Day-1 Build Plan (practical)

1. Scaffold repo (FastAPI + Typer + SQLite + FAISS)
2. Implement `ingest file` → extract text → chunk → embed → store
3. Implement `/search` hybrid + CLI search
4. Add `/ask` with streaming answers & citations
5. Basic web: search bar, results, doc viewer

---

## 18) What “Done & Proud” Looks Like

* You can drop a folder or paste a URL and **within minutes** ask: *“Summarize what I learned about CNN vs XGBoost last semester, with sources.”*
* It answers blablabla
