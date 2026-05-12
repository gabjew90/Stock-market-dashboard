"""A tiny Okapi-BM25 ranker over pre-tokenized documents (no external deps)."""
from __future__ import annotations

import math
from collections import Counter


class BM25:
    def __init__(self, corpus: list[list[str]], *, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.n = len(corpus)
        self.doc_len = [len(d) for d in corpus]
        self.avgdl = (sum(self.doc_len) / self.n) if self.n else 0.0
        self.tf: list[Counter[str]] = [Counter(d) for d in corpus]
        df: Counter[str] = Counter()
        for d in corpus:
            df.update(set(d))
        # BM25 idf (the standard "plus 0.5" form, floored at a small positive value)
        self.idf: dict[str, float] = {}
        for term, freq in df.items():
            self.idf[term] = max(1e-9, math.log((self.n - freq + 0.5) / (freq + 0.5) + 1.0))

    def score(self, query_tokens: list[str], doc_index: int) -> float:
        if self.n == 0 or self.avgdl == 0:
            return 0.0
        tf = self.tf[doc_index]
        dl = self.doc_len[doc_index]
        s = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            idf = self.idf.get(term, 0.0)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += idf * freq * (self.k1 + 1) / denom
        return s

    def query(self, query_tokens: list[str], *, top_k: int = 10) -> list[tuple[int, float]]:
        """Return [(doc_index, score), ...] sorted by score desc, length min(top_k, n)."""
        scored = [(i, self.score(query_tokens, i)) for i in range(self.n)]
        scored.sort(key=lambda x: (-x[1], x[0]))
        return scored[:top_k]
