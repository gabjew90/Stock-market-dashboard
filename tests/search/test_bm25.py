from ww.search.bm25 import BM25


def test_bm25_ranks_the_doc_with_the_rare_query_term_first():
    docs = [
        ["the", "green", "line", "is", "an", "all", "time", "high"],
        ["funding", "and", "open", "interest", "are", "crypto", "things"],
        ["green", "line", "breakout", "buy", "the", "stock", "at", "a", "new", "high"],
    ]
    bm = BM25(docs)
    ranked = bm.query(["green", "line", "breakout"], top_k=3)
    assert ranked[0][0] == 2                     # doc 2 has all three query terms
    assert ranked[-1][0] == 1                    # doc 1 has none -> last (score 0)
    assert ranked[0][1] > ranked[1][1] > ranked[2][1]


def test_bm25_unknown_query_term_contributes_nothing():
    docs = [["alpha", "beta"], ["beta", "gamma"]]
    bm = BM25(docs)
    ranked = bm.query(["zzz"], top_k=2)
    assert all(score == 0.0 for _i, score in ranked)


def test_bm25_empty_corpus_returns_empty():
    assert BM25([]).query(["x"], top_k=5) == []
