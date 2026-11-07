"""Task 3: evaluate three chunkers and two retrieval backends."""
import csv
import json
import time
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def evaluate(score_matrix, chunks, items):
    hits, reciprocal = [], []
    for row, query in zip(score_matrix, items):
        if query["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        relevant_ranks = [
            rank for rank, index in enumerate(top, 1)
            if chunks[index]["doc"] == query["doc"]
            and query["evidence"] in chunks[index]["text"]
        ]
        hits.append(bool(relevant_ranks))
        reciprocal.append(1 / relevant_ranks[0] if relevant_ranks else 0)
    if not hits:
        return None, None
    return float(np.mean(hits)), float(np.mean(reciprocal))

def load_data():
    docs = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
    items = json.loads(Path("queries.json").read_text(encoding="utf-8"))
    assert docs and len(items) >= 10
    assert sum(q["doc"] is not None for q in items) >= 8
    assert sum(q["doc"] is None for q in items) >= 2
    assert sum(q["split"] == "dev" and q["doc"] is not None for q in items) == 4
    assert sum(q["split"] == "test" and q["doc"] is not None for q in items) == 4
    for query in items:
        assert query["split"] in {"dev", "test"}
        if query["doc"] is not None:
            assert query["doc"] in docs
            assert query["evidence"] in docs[query["doc"]]
    return docs, items

def main():
    docs, items = load_data()
    query_texts = [q["query"] for q in items]
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "sentence-transformers is required for the full six-configuration "
            "evaluation. Install requirements.txt and rerun."
        ) from exc

    start = time.perf_counter()
    model = SentenceTransformer(MODEL_NAME, device="cpu")
    model_load_seconds = time.perf_counter() - start
    print(f"Model load seconds: {model_load_seconds:.4f}")
    logs, summary = [], []

    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        texts = [chunk["text"] for chunk in chunks]
        token_lengths = [
            len(model.tokenizer(text, truncation=False)["input_ids"])
            for text in texts + query_texts
        ]
        if max(token_lengths) > model.max_seq_length:
            raise ValueError(
                f"{strategy}: model token limit {model.max_seq_length} exceeded "
                f"(maximum observed {max(token_lengths)}). Rechunk before encoding."
            )

        for method in ["tfidf", "embedding"]:
            start = time.perf_counter()
            if method == "tfidf":
                vectorizer = TfidfVectorizer()
                C = vectorizer.fit_transform(texts)
                Q = vectorizer.transform(query_texts)
                encode_seconds = time.perf_counter() - start
                start = time.perf_counter()
                scores = (Q @ C.T).toarray()
            else:
                C = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                Q = model.encode(query_texts, normalize_embeddings=True, show_progress_bar=False)
                encode_seconds = time.perf_counter() - start
                start = time.perf_counter()
                scores = Q @ C.T
            search_seconds = time.perf_counter() - start

            for split in ["dev", "test"]:
                indices = [i for i, q in enumerate(items) if q["split"] == split and q["doc"]]
                hit, mrr = evaluate(scores[indices], chunks, [items[i] for i in indices])
                row = {
                    "strategy": strategy, "method": method, "split": split,
                    "hit_at_3": hit, "mrr_at_3": mrr,
                    "chunk_count": len(chunks), "max_model_tokens": max(token_lengths),
                    "model_load_seconds": model_load_seconds,
                    "encode_seconds": encode_seconds, "search_seconds": search_seconds
                }
                summary.append(row)
                print(row)

            # Log top-three candidates for every query, including unanswerable ones.
            for score_row, query in zip(scores, items):
                for rank, index in enumerate(np.argsort(-score_row, kind="stable")[:3], 1):
                    chunk = chunks[index]
                    logs.append({
                        "strategy": strategy, "method": method,
                        "query": query["query"], "split": query["split"],
                        "answerable": query["doc"] is not None, "rank": rank,
                        "score": float(score_row[index]), "chunk_id": chunk["id"],
                        "doc": chunk["doc"], "source": chunk["source"],
                        "start": chunk["start"], "end": chunk["end"],
                        "text": chunk["text"]
                    })
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(logs[0]))
        writer.writeheader()
        writer.writerows(logs)
    with open("evaluation_summary.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Saved {len(logs)} ranked candidates to retrieval_log.csv")
    print("Saved six-configuration metrics to evaluation_summary.csv")
    print("Unanswerable queries are logged as candidates, not scored as relevant.")

if __name__ == "__main__":
    main()
