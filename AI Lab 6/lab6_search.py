"""Shared retrieval helper for Lab 6: TF-IDF and sentence embeddings."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Retriever:
    def __init__(self, records, backend="tfidf", model=None):
        if not records or any(not r.get("text", "").strip() for r in records):
            raise ValueError("Provide nonempty records with nonempty text")
        if backend not in {"tfidf", "embedding"}:
            raise ValueError("Use tfidf or embedding")
        self.records = records
        self.backend = backend
        self.model = model

        texts = [r["text"] for r in records]
        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(texts)
        else:
            if self.model is None:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(
                    "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
                )
            self.check_length(texts)
            self.matrix = self.model.encode(texts, normalize_embeddings=True)

    def check_length(self, texts):
        for text in texts:
            token_ids = self.model.tokenizer(text, truncation=False)["input_ids"]
            if len(token_ids) > self.model.max_seq_length:
                raise ValueError(
                    f"Input has {len(token_ids)} model tokens; "
                    f"limit is {self.model.max_seq_length}. Rechunk the text."
                )

    def search(self, query, k=3, filters=None):
        if not query.strip() or k <= 0:
            return []
        if self.backend == "tfidf":
            q = self.vectorizer.transform([query])
            if q.nnz == 0:
                return []
            scores = (q @ self.matrix.T).toarray()[0]
        else:
            self.check_length([query])
            q = self.model.encode([query], normalize_embeddings=True)[0]
            scores = self.matrix @ q

        allowed = [
            i for i, record in enumerate(self.records)
            if all(record.get(key) == value
                   for key, value in (filters or {}).items())
        ]
        ranked = sorted(allowed, key=lambda i: (-float(scores[i]), i))
        return [(self.records[i], float(scores[i])) for i in ranked[:k]]


def show_hits(hits):
    if not hits:
        print("No matching records.")
    for record, score in hits:
        print(record["id"], f"score={score:.3f}")
        print(record["text"])
