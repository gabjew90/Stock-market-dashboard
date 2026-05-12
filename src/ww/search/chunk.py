"""Split a markdown document into heading-scoped chunks and tokenize text for BM25."""
from __future__ import annotations

import re
from dataclasses import dataclass

_FRONT_MATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_HEADING = re.compile(r"^(#{1,3})\s+(.*?)\s*$")
_TOKEN = re.compile(r"[a-z0-9]+")
# light markdown stripping before tokenizing
_MD_NOISE = re.compile(r"[*_`>#~]|!\[|\]\([^)]*\)|\[|\]")


def tokenize(text: str) -> list[str]:
    cleaned = _MD_NOISE.sub(" ", text.lower())
    return _TOKEN.findall(cleaned)


@dataclass
class Chunk:
    source: str       # "wiki:<rel-path>" or "post:<stem>"
    heading: str      # the heading path, e.g. "GMI > What it is"
    text: str         # the chunk body (including its heading line)


def chunk_markdown(text: str, *, source: str) -> list[Chunk]:
    body = _FRONT_MATTER.sub("", text, count=1).strip()
    lines = body.splitlines()
    chunks: list[Chunk] = []
    # heading stack: list of (level, title)
    stack: list[tuple[int, str]] = []
    cur_lines: list[str] = []

    def flush() -> None:
        if any(ln.strip() for ln in cur_lines):
            heading = " > ".join(t for _l, t in stack) if stack else (source.split(":", 1)[-1])
            chunks.append(Chunk(source=source, heading=heading, text="\n".join(cur_lines).strip()))

    for ln in lines:
        m = _HEADING.match(ln)
        if m:
            flush()
            cur_lines = [ln]
            level = len(m.group(1))
            title = m.group(2).strip()
            # pop deeper-or-equal levels, then push
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        else:
            cur_lines.append(ln)
    flush()
    if not chunks:  # no headings at all
        chunks.append(Chunk(source=source, heading=source.split(":", 1)[-1], text=body))
    return chunks
