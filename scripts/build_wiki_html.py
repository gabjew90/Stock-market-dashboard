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
# Pages we deliberately exclude from the rendered wiki even when their .md files exist on disk.
_SKIP_PAGES = {"backtest-timing-overlay.md"}

SECTION_ORDER = [
    ("Overview", ["overview.md"]),
    ("Methodology", sorted(p.name for p in (WIKI / "methodology").glob("*.md") if p.name not in _SKIP_PAGES)),
    ("Playbooks", sorted(p.name for p in (WIKI / "playbooks").glob("*.md") if p.name not in _SKIP_PAGES)),
    ("History", sorted(p.name for p in (WIKI / "history").glob("*.md") if p.name not in _SKIP_PAGES)),
]
SOURCES_DIR = WIKI / "sources"

FRONT_MATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
MD_LINK = re.compile(r"\]\(([^)\s]+?)(#[^)\s]*)?\)")
H1 = re.compile(r"^#\s+(.*)$", re.MULTILINE)


def anchor_for(rel: str) -> str:
    """wiki-relative path -> anchor id, e.g. 'methodology/gmi.md' -> 'methodology-gmi'."""
    return rel[:-3].replace("/", "-").replace(".", "-") if rel.endswith(".md") else rel.replace("/", "-")


def load_post_urls() -> dict[str, str]:
    """Stem → wishingwealthblog.com URL. Prefer the full posts.jsonl (local dev) but fall back
    to the slim raw/url_map.json that's committed to the repo for CI builds."""
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
    url_map = ROOT / "raw" / "url_map.json"
    if url_map.exists():
        out.update(json.loads(url_map.read_text(encoding="utf-8")))
    return out


def rewrite_links(text: str, page_rel: str, page_anchors: set[str], post_urls: dict[str, str]) -> str:
    """Rewrite markdown link targets inside one page's body."""
    page_dir = Path(page_rel).parent  # relative to wiki/

    def repl(m: re.Match) -> str:
        target, frag = m.group(1), (m.group(2) or "")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        # Image / static-asset paths — pass through untouched. The daily workflow copies
        # the repo's `assets/` tree into the deployed site so these resolve correctly from wiki.html.
        if target.startswith("assets/") or target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            return m.group(0)
        # Resolve relative to the page's directory, against the wiki/ root.
        # Targets like ../../raw/posts/<stem>.md escape wiki/ — handle those first.
        if "raw/posts/" in target:
            stem = Path(target).stem  # filename without .md
            url = post_urls.get(stem)
            return f"]({url})" if url else f"](javascript:void(0))"
        # Source-summary links — we no longer render the source notes appendix;
        # redirect any ../sources/<stem>.md or sources/<stem>.md link straight to the original blog post.
        if "sources/" in target:
            stem = Path(target).stem
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
    # Strip the per-page "## Sources" citation block entirely. The body already cites each post
    # inline via the (WW YYYY-MM-DD) links, so the trailing bibliographic list is redundant.
    body_html = re.sub(
        r"<h2[^>]*>\s*Sources\s*</h2>.*$",
        "",
        body_html,
        count=1,
        flags=re.DOTALL,
    )
    return anchor_for(rel), title, body_html


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stock market dashboard — About</title>
<style>
  :root {{
    --bg: #0d1117; --panel: #161b22; --panel-2: #1c2330; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
    --green: #2ea043; --red: #f85149;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    color-scheme: dark;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    line-height: 1.6; font-size: 16px;
  }}

  /* shared top nav (matches GMI playground) */
  .pages-nav {{
    position: sticky; top: 0; z-index: 100; display: flex; align-items: center;
    gap: 6px; padding: 12px 16px; background: rgba(13,17,23,0.96);
    backdrop-filter: blur(8px); border-bottom: 1px solid var(--border);
  }}
  .pages-nav .brand {{ font-weight: 600; margin-right: auto; font-size: 14px; letter-spacing: -0.01em; color: var(--text); }}
  .pages-nav .brand .sub {{ color: var(--muted); font-weight: 400; font-size: 12px; margin-left: 6px; }}
  .pages-nav a {{
    color: var(--muted); text-decoration: none; padding: 6px 12px; border-radius: 6px;
    font-size: 12px; font-family: var(--mono); font-weight: 500;
    border: 1px solid transparent;
    transition: color 0.15s, background 0.15s, border-color 0.15s;
  }}
  .pages-nav a.active {{ color: var(--text); border-color: var(--accent); background: rgba(88,166,255,0.14); }}
  .pages-nav a:hover {{ color: var(--text); background: var(--panel-2); }}
  @media (max-width: 480px) {{
    .pages-nav {{ padding: 10px 12px; gap: 4px; }}
    .pages-nav .brand {{ font-size: 12px; }}
    .pages-nav a {{ padding: 5px 9px; font-size: 11px; }}
  }}

  .wrap {{ max-width: 820px; margin: 0 auto; padding: 12px 16px 48px; }}
  .panel {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
    padding: 18px 20px; margin: 12px 0;
  }}

  h1, h2, h3 {{ line-height: 1.3; }}
  h1 {{ font-size: 22px; margin: 24px 0 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px; color: var(--text); }}
  h2 {{ font-size: 18px; margin: 22px 0 10px; color: var(--text); }}
  h3 {{ font-size: 15px; margin: 16px 0 6px; color: var(--text); }}
  p {{ margin: 8px 0; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  hr {{ border: none; border-top: 1px solid var(--border); margin: 28px 0; }}
  blockquote {{
    border-left: 3px solid var(--accent); margin: 12px 0; padding: 6px 14px;
    color: var(--muted); background: var(--panel-2); border-radius: 0 6px 6px 0;
  }}
  code {{
    background: var(--panel-2); color: #f0b429; padding: 2px 5px;
    border-radius: 4px; font-family: var(--mono); font-size: 13px;
  }}
  pre {{
    background: var(--panel-2); padding: 12px 14px; border-radius: 8px;
    overflow-x: auto; border: 1px solid var(--border); font-size: 13px;
  }}
  pre code {{ background: none; padding: 0; color: var(--text); }}
  table {{
    border-collapse: collapse; width: 100%; margin: 12px 0;
    display: block; overflow-x: auto; font-size: 13px;
  }}
  th, td {{ border: 1px solid var(--border); padding: 6px 10px; text-align: left; }}
  thead th {{ background: var(--panel-2); color: var(--text); font-weight: 600; }}
  ul, ol {{ padding-left: 22px; }}
  li {{ margin: 3px 0; }}
  strong {{ color: var(--text); font-weight: 600; }}
  em {{ color: var(--muted); }}

  section {{ scroll-margin-top: 64px; }}
  .top {{
    float: right; font-size: 11px; color: var(--muted); text-decoration: none;
    padding: 2px 8px; border: 1px solid var(--border); border-radius: 999px;
    margin-top: 6px; font-family: var(--mono);
  }}
  .top:hover {{ color: var(--accent); border-color: var(--accent); }}
  .src-note {{ font-size: 14px; opacity: 0.92; }}
  .src-note h1 {{ font-size: 17px; }}
  .gen {{ color: var(--muted); font-size: 12px; margin-top: 40px; text-align: center; }}
  .gen code {{ font-size: 11px; }}

  /* TOC styling — make the landing page feel like a card stack */
  #index ul {{ list-style: none; padding-left: 8px; }}
  #index li {{ margin: 4px 0; }}
  #index ul ul {{ padding-left: 16px; margin: 2px 0; }}

  /* Collapsed per-page Sources block */
  details.sources-fold {{ margin-top: 18px; border-top: 1px solid var(--border); padding-top: 8px; }}
  details.sources-fold summary {{
    cursor: pointer; color: var(--muted); font-size: 12px; padding: 4px 0;
    font-family: var(--mono); list-style: none;
  }}
  details.sources-fold summary::before {{ content: "▸ "; }}
  details.sources-fold[open] summary::before {{ content: "▾ "; }}
  details.sources-fold summary:hover {{ color: var(--accent); }}
  details.sources-fold ul {{ margin-top: 6px; font-size: 13px; }}
</style>
</head>
<body>
<nav class="pages-nav">
  <span class="brand">Stock market dashboard</span>
  <a href="./">Market Trend</a>
  <a href="./pulse/">News &amp; Macro</a>
  <a href="./wiki.html" class="active">About</a>
</nav>
<div class="wrap">
{toc}
{sections}
{appendix}
<p class="gen">Generated from <code>wishing-wealth-wiki</code> · {n_pages} pages · citations link to the original posts on wishingwealthblog.com.</p>
</div>
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
    # Source-summary pages are no longer rendered inline — methodology citations to them now redirect
    # straight to the original wishingwealthblog.com post via rewrite_links().
    page_anchors = {anchor_for(r) for r in page_rels}

    # index.md = landing TOC
    idx_path = WIKI / "index.md"
    idx_raw = FRONT_MATTER.sub("", idx_path.read_text(encoding="utf-8"), count=1).strip() if idx_path.exists() else "# Wiki index"
    idx_raw = rewrite_links(idx_raw, "index.md", page_anchors, post_urls)
    # strip the "*(stub)*" markers — everything's real enough now
    idx_raw = idx_raw.replace("*(stub)*", "")
    toc_inner = markdown.markdown(idx_raw, extensions=["tables", "sane_lists", "attr_list"])
    # Drop the bibliographic Sources list from the TOC — per-page citations are already inline.
    toc_inner = re.sub(r"<h2[^>]*>\s*Sources\s*</h2>.*$", "", toc_inner, count=1, flags=re.DOTALL)
    toc_html = '<section id="index" class="panel">' + toc_inner + "</section>"

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
                f'<section id="{anchor}" class="panel"><a class="top" href="#index">↑ contents</a>\n{body}\n</section>'
            )

    n_pages = 1 + len(page_rels)
    out_html = TEMPLATE.format(
        toc=toc_html,
        sections="\n".join(section_blocks),
        appendix="",
        n_pages=n_pages,
    )
    out_path = ROOT / "wiki_site.html"
    out_path.write_text(out_html, encoding="utf-8")
    print(f"wrote {out_path}  ({out_path.stat().st_size / 1024:.0f} KB, {n_pages} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
