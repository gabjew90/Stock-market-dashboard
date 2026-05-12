"""Render the whole wiki/ directory into one self-contained, mobile-friendly HTML file.

Usage:  uv run --with markdown --with pygments python scripts/build_wiki_html.py
Output: wiki_site.html  (at the repo root; gitignored — it's a generated artifact)

Page citations of the form (../../raw/posts/<stem>.md) are rewritten to the
original wishingwealthblog.com post URL (looked up in raw/posts.jsonl), so they
work on a phone. Internal [x](page.md) links become #anchor jumps. Source-summary
pages are appended at the end under an "Appendix: source notes" section.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import markdown  # provided via `uv run --with markdown`

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"

# Page order. (index.md is rendered first as the landing table-of-contents.)
SECTION_ORDER = [
    ("Overview", ["overview.md"]),
    ("Methodology", sorted(p.name for p in (WIKI / "methodology").glob("*.md"))),
    ("Playbooks", sorted(p.name for p in (WIKI / "playbooks").glob("*.md"))),
    ("History", sorted(p.name for p in (WIKI / "history").glob("*.md"))),
]
SOURCES_DIR = WIKI / "sources"

FRONT_MATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
MD_LINK = re.compile(r"\]\(([^)\s]+?)(#[^)\s]*)?\)")
H1 = re.compile(r"^#\s+(.*)$", re.MULTILINE)


def anchor_for(rel: str) -> str:
    """wiki-relative path -> anchor id, e.g. 'methodology/gmi.md' -> 'methodology-gmi'."""
    return rel[:-3].replace("/", "-").replace(".", "-") if rel.endswith(".md") else rel.replace("/", "-")


def load_post_urls() -> dict[str, str]:
    out: dict[str, str] = {}
    jsonl = ROOT / "raw" / "posts.jsonl"
    if jsonl.exists():
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["stem"]] = r["url"]
    return out


def rewrite_links(text: str, page_rel: str, page_anchors: set[str], post_urls: dict[str, str]) -> str:
    """Rewrite markdown link targets inside one page's body."""
    page_dir = Path(page_rel).parent  # relative to wiki/

    def repl(m: re.Match) -> str:
        target, frag = m.group(1), (m.group(2) or "")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        # Resolve relative to the page's directory, against the wiki/ root.
        # Targets like ../../raw/posts/<stem>.md escape wiki/ — handle those first.
        if "raw/posts/" in target:
            stem = Path(target).stem  # filename without .md
            url = post_urls.get(stem)
            return f"]({url})" if url else f"](javascript:void(0))"
        # Otherwise it should resolve to a wiki page (possibly in another subdir).
        try:
            resolved = (WIKI / page_dir / target).resolve().relative_to(WIKI).as_posix()
        except ValueError:
            return f"](javascript:void(0))"  # points outside wiki/ and isn't a raw post
        a = anchor_for(resolved)
        if a in page_anchors:
            return f"](#{a})"
        return f"](javascript:void(0))"

    return MD_LINK.sub(repl, text)


def render_page(path: Path, post_urls: dict[str, str], page_anchors: set[str]) -> tuple[str, str, str]:
    """Return (anchor_id, title, html_body) for one wiki page."""
    rel = path.relative_to(WIKI).as_posix()
    raw = FRONT_MATTER.sub("", path.read_text(encoding="utf-8"), count=1).strip()
    # drop the "> **Status:** stub ..." line if any (none should remain, but be safe)
    raw = re.sub(r"^>\s*\*\*Status:\*\*.*\n", "", raw, flags=re.MULTILINE)
    m = H1.search(raw)
    title = m.group(1).strip() if m else rel
    raw = rewrite_links(raw, rel, page_anchors, post_urls)
    body_html = markdown.markdown(
        raw,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html", "smarty"],
    )
    return anchor_for(rel), title, body_html


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wishing Wealth Wiki</title>
<style>
  :root {{ color-scheme: light dark; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6; max-width: 760px; margin: 0 auto; padding: 1rem 1.1rem 6rem;
    font-size: 17px; color: #1a1a1a; background: #fff;
  }}
  @media (prefers-color-scheme: dark) {{ body {{ color: #e6e6e6; background: #161616; }}
    a {{ color: #6cb6ff; }} hr {{ border-color: #333; }} blockquote {{ border-color: #444; color: #bbb; }}
    code, pre {{ background: #222; }} .top, header small {{ color: #888; }} th, td {{ border-color: #333; }}
    thead th {{ background: #222; }} }}
  h1, h2, h3 {{ line-height: 1.25; margin-top: 1.8rem; }}
  h1 {{ font-size: 1.7rem; border-bottom: 2px solid #ddd; padding-bottom: .25rem; }}
  h2 {{ font-size: 1.3rem; }} h3 {{ font-size: 1.1rem; }}
  a {{ color: #0a58ca; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 3rem 0; }}
  blockquote {{ border-left: 3px solid #ccc; margin: 1rem 0; padding: .1rem 1rem; color: #555; }}
  code {{ background: #f3f3f3; padding: .1rem .3rem; border-radius: 3px; font-size: .9em; }}
  pre {{ background: #f3f3f3; padding: .8rem; border-radius: 5px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid #ccc; padding: .4rem .6rem; text-align: left; font-size: .92em; }}
  thead th {{ background: #f3f3f3; }}
  header {{ position: sticky; top: 0; background: inherit; padding: .5rem 0; border-bottom: 1px solid #ddd;
    margin-bottom: 1rem; font-weight: 600; }}
  header small {{ font-weight: 400; color: #888; }}
  section {{ scroll-margin-top: 3.5rem; }}
  .top {{ float: right; font-size: .8rem; color: #888; text-decoration: none; }}
  .src-note {{ font-size: .95em; }}
  .gen {{ color: #888; font-size: .85rem; margin-top: 3rem; }}
</style>
</head>
<body>
<header>📈 Wishing Wealth Wiki <small>— Dr. Eric Wish's methodology, synthesised from his blog</small></header>
{toc}
{sections}
{appendix}
<p class="gen">Generated from the <code>wishing-wealth-wiki</code> repo · {n_pages} pages · citations link to the original posts on wishingwealthblog.com.</p>
</body>
</html>
"""


def main() -> int:
    post_urls = load_post_urls()

    # First pass: collect every page rel-path so link-rewriting knows valid anchors.
    page_rels: list[str] = []
    for _label, names in SECTION_ORDER:
        subdir = "" if names == ["overview.md"] else _label.lower()
        for name in names:
            rel = name if subdir == "" else f"{subdir}/{name}"
            if (WIKI / rel).exists():
                page_rels.append(rel)
    source_rels = [f"sources/{p.name}" for p in sorted(SOURCES_DIR.glob("*.md")) if p.name != ".gitkeep"] if SOURCES_DIR.exists() else []
    page_anchors = {anchor_for(r) for r in page_rels + source_rels}

    # index.md = landing TOC
    idx_path = WIKI / "index.md"
    idx_raw = FRONT_MATTER.sub("", idx_path.read_text(encoding="utf-8"), count=1).strip() if idx_path.exists() else "# Wiki index"
    idx_raw = rewrite_links(idx_raw, "index.md", page_anchors, post_urls)
    # strip the "*(stub)*" markers — everything's real enough now
    idx_raw = idx_raw.replace("*(stub)*", "")
    toc_html = '<section id="index">' + markdown.markdown(idx_raw, extensions=["tables", "sane_lists", "attr_list"]) + "</section><hr>"

    # main sections
    section_blocks: list[str] = []
    for label, names in SECTION_ORDER:
        subdir = "" if names == ["overview.md"] else label.lower()
        if subdir:
            section_blocks.append(f'<h1 id="cat-{subdir}">{html.escape(label)}</h1>')
        for name in names:
            rel = name if subdir == "" else f"{subdir}/{name}"
            p = WIKI / rel
            if not p.exists():
                continue
            anchor, _title, body = render_page(p, post_urls, page_anchors)
            section_blocks.append(
                f'<section id="{anchor}"><a class="top" href="#index">↑ contents</a>\n{body}\n</section>\n<hr>'
            )

    # appendix: source notes
    appendix_blocks: list[str] = []
    if source_rels:
        appendix_blocks.append('<h1 id="cat-sources">Appendix — source notes</h1>')
        appendix_blocks.append('<p class="src-note">One short note per ingested post (what it teaches, key claims). The methodology pages above link into these.</p>')
        for rel in source_rels:
            anchor, _title, body = render_page(WIKI / rel, post_urls, page_anchors)
            appendix_blocks.append(
                f'<section id="{anchor}" class="src-note"><a class="top" href="#index">↑ contents</a>\n{body}\n</section>\n<hr>'
            )

    n_pages = 1 + len(page_rels) + len(source_rels)
    out_html = TEMPLATE.format(
        toc=toc_html,
        sections="\n".join(section_blocks),
        appendix="\n".join(appendix_blocks),
        n_pages=n_pages,
    )
    out_path = ROOT / "wiki_site.html"
    out_path.write_text(out_html, encoding="utf-8")
    print(f"wrote {out_path}  ({out_path.stat().st_size / 1024:.0f} KB, {n_pages} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
