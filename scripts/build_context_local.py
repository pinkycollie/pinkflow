#!/usr/bin/env python3
"""
Bootstrap Community Context Builder (local, zero-cost).

- Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings (small & free).
- Uses faiss for local vector search (fast, file-backed).
- Uses transformers summarization pipeline (facebook/bart-large-cnn) for synthesis.
- Starts from config/sources.json (URLs / RSS).

Run:
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r scripts/requirements.txt
  python scripts/build_context_local.py

Notes:
- This is lightweight and CPU-friendly. For larger runs, consider Chroma or persistent storage.
- For LLM-quality synthesis later, swap summarizer call to Ollama or a local LLM.
"""
import json
import os
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from transformers import pipeline

BASE = Path.cwd()
SOURCES_PATH = BASE / "config" / "sources.json"
OUTPUT_PATH = BASE / "config" / "context.json"
FAISS_INDEX_PATH = BASE / ".faiss_index.index"
DOCS_PATH = BASE / ".context_docs.json"  # stores raw chunks and metadata

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
MAX_CHUNKS_PER_SOURCE = 30

def load_sources():
    if not SOURCES_PATH.exists():
        print("Create config/sources.json with a small set of pages (see sample). Exiting.")
        return []
    return json.loads(SOURCES_PATH.read_text(encoding="utf8"))

def fetch_text(url):
    print("Fetching", url)
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "PinkFlow/ContextBuilder"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup(["script", "style", "noscript"]):
            s.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())
    except Exception as e:
        print("Failed to fetch", url, e)
        return ""

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if not text:
        return []
    chunks = []
    i = 0
    L = len(text)
    while i < L and len(chunks) < MAX_CHUNKS_PER_SOURCE:
        chunk = text[i:i+size]
        chunks.append(chunk)
        i += size - overlap
    return chunks

def build_embeddings(chunks, model):
    # model.encode accepts list of texts
    return np.array(model.encode(chunks, show_progress_bar=True, convert_to_numpy=True))

def save_faiss(index, docs):
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    DOCS_PATH.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf8")
    print("Saved FAISS index and docs.")

def load_faiss():
    if FAISS_INDEX_PATH.exists() and DOCS_PATH.exists():
        idx = faiss.read_index(str(FAISS_INDEX_PATH))
        docs = json.loads(DOCS_PATH.read_text(encoding="utf8"))
        return idx, docs
    return None, None

def main():
    sources = load_sources()
    if not sources:
        return

    # load or init model & index
    emb_model = SentenceTransformer("all-MiniLM-L6-v2")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  # CPU-friendly-ish

    doc_texts = []
    doc_meta = []

    for s in sources:
        typ = s.get("type","web")
        if typ != "web" and typ != "rss":
            continue
        url = s.get("url")
        text = fetch_text(url)
        chunks = chunk_text(text)
        for i, ch in enumerate(chunks):
            doc_texts.append(ch)
            doc_meta.append({"source": url, "title": s.get("title",""), "source_id": s.get("id",""), "chunk_index": i})

    if not doc_texts:
        print("No chunks produced; check sources.json")
        return

    # embeddings
    embeddings = build_embeddings(doc_texts, emb_model)
    d = embeddings.shape[1]

    # faiss index (flat L2)
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    save_faiss(index, [{"text": t, "meta": m} for t,m in zip(doc_texts, doc_meta)])

    # retrieval + synthesis: run a few seed queries and summarize evidence
    seed_queries = [
        "caption requirements and best practices",
        "transcripts for audio content legal guidance",
        "sign language interpretation for live events requirements"
    ]
    context = {
        "version": "0.1.0",
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_basis": [{"id": s.get("id", s.get("url")), "title": s.get("title",""), "url": s.get("url")} for s in sources],
        "core_principles": [],
        "legal_risks": [],
        "priority": [],
        "sources": [],
        "notes": {"auto_generated": True, "curation_required": True}
    }

    # simple retrieval: encode query and search nearest neighbors
    for q in seed_queries:
        qemb = emb_model.encode([q], convert_to_numpy=True)
        k = min(6, index.ntotal)
        D, I = index.search(qemb, k)
        evidences = []
        for idx in I[0]:
            evidences.append(doc_texts[idx][:1000])
        # ask summarizer to synthesize short bullets
        joined = "\n\n".join(evidences)
        prompt = joined[:4000]  # avoid too-long
        try:
            sum_res = summarizer(prompt, max_length=200, min_length=30, do_sample=False)
            summary_text = sum_res[0]['summary_text']
        except Exception as e:
            summary_text = "Summary failed: " + str(e)
        # naive extraction: split sentences into bullets
        bullets = [s.strip() for s in summary_text.split('. ') if s.strip()]
        context["core_principles"].extend(bullets[:3])
        context["sources"].extend([doc_meta[idx]["source"] for idx in I[0]])

    # dedupe and trim
    def uniq_keep_first(lst):
        seen = set()
        out = []
        for x in lst:
            k = x.strip().lower()
            if k and k not in seen:
                seen.add(k)
                out.append(x)
        return out

    context["core_principles"] = uniq_keep_first(context["core_principles"])[:10]
    context["priority"] = ["Deaf Accessibility","Legal Compliance","Trust"]
    context["legal_risks"] = ["Failure to provide accurate captions","No transcript for audio content"]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(context, indent=2, ensure_ascii=False), encoding="utf8")
    print("Wrote context to", OUTPUT_PATH)

if __name__ == "__main__":
    main()
