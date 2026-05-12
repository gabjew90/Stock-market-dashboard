from ww.search.chunk import chunk_markdown, tokenize


def test_tokenize_lowercases_and_strips_markdown():
    # The plan allows relaxing to membership checks when the exact list depends on
    # regex evaluation order for link syntax like [T2108](t2108.md).
    # Substantive requirements: key words survive, markdown syntax is stripped.
    tokens = tokenize("The **GMI** is at 6 (of 6) — see [T2108](t2108.md).")
    assert "the" in tokens
    assert "gmi" in tokens
    assert "is" in tokens
    assert "6" in tokens
    assert "see" in tokens
    assert "t2108" in tokens
    # markdown noise stripped: no asterisks, brackets, parens in tokens
    assert not any("*" in t or "[" in t or "]" in t or "(" in t for t in tokens)


def test_chunk_splits_on_h2_and_h3_headings():
    md = (
        "---\ntitle: GMI\n---\n\n"
        "# General Market Index\n\nIntro text.\n\n"
        "## What it is\n\nThe six components.\n\n"
        "### Component 1\n\nNew highs.\n\n"
        "## How he uses it\n\nThreshold of 4.\n"
    )
    chunks = chunk_markdown(md, source="wiki:methodology/gmi.md")
    headings = [c.heading for c in chunks]
    assert "General Market Index" in headings[0]                  # the intro chunk under the H1
    assert any("What it is" in h for h in headings)
    assert any("Component 1" in h for h in headings)
    assert any("How he uses it" in h for h in headings)
    # front-matter is stripped from chunk text
    assert all("title: GMI" not in c.text for c in chunks)
    # source carried through
    assert all(c.source == "wiki:methodology/gmi.md" for c in chunks)


def test_chunk_short_doc_with_no_headings_is_one_chunk():
    chunks = chunk_markdown("Just a paragraph of body text, no headings here.", source="post:2020-01-01-x")
    assert len(chunks) == 1
    assert chunks[0].text.strip().startswith("Just a paragraph")
