"""Mechanical integrity checks over the wiki/ directory."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Markdown links: [text](target) — capture the target, drop #anchors and titles.
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Files in wiki/ that are NOT "wiki pages" (no front-matter / Sources requirement,
# not required to appear in index.md, exempt from the orphan check).
_NON_PAGE_NAMES = {"index.md", "log.md"}
_NON_PAGE_DIRS = {"_templates"}


@dataclass
class LintReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def _wiki_pages(wiki_dir: Path) -> list[Path]:
    """All markdown files under wiki/ that count as 'pages' (subject to conventions)."""
    pages: list[Path] = []
    for p in sorted(wiki_dir.rglob("*.md")):
        rel_parts = p.relative_to(wiki_dir).parts
        if rel_parts[0] in _NON_PAGE_DIRS:
            continue
        if p.name in _NON_PAGE_NAMES and len(rel_parts) == 1:
            continue
        pages.append(p)
    return pages


def lint_wiki(root: Path) -> LintReport:
    root = Path(root)
    wiki_dir = root / "wiki"
    report = LintReport()
    if not wiki_dir.is_dir():
        report.errors.append(f"no wiki/ directory at {root}")
        return report

    index_path = wiki_dir / "index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_targets = {t for t in _LINK.findall(index_text) if not _is_external(t)}
    # Normalise index targets to wiki-relative posix paths.
    index_pages = set()
    for t in index_targets:
        norm = (index_path.parent / t.split("#")[0]).resolve()
        index_pages.add(norm)

    pages = _wiki_pages(wiki_dir)
    inbound: dict[Path, int] = {p.resolve(): 0 for p in pages}

    for page in pages:
        rel = page.relative_to(root).as_posix()
        text = page.read_text(encoding="utf-8")

        # 1. Sources section present?
        if not re.search(r"^##\s+Sources\s*$", text, flags=re.MULTILINE):
            report.errors.append(f"{rel}: missing a '## Sources' section")

        # 2. Internal links resolve? (and tally inbound links to other wiki pages)
        for target in _LINK.findall(text):
            if _is_external(target) or target.startswith("#"):
                continue
            dest = (page.parent / target.split("#")[0]).resolve()
            if not dest.exists():
                report.errors.append(f"{rel}: broken link -> {target}")
                continue
            if dest in inbound and dest != page.resolve():
                inbound[dest] += 1

        # 3. Page catalogued in index.md? (overview/methodology/playbooks/history/sources pages)
        if page.resolve() not in index_pages and page.name != "index.md":
            # sources/.gitkeep style files won't be .md; .md pages must be indexed.
            report.errors.append(f"{rel}: not catalogued in wiki/index.md")

    # 4. Orphan pages (no inbound link). overview.md exempt (it's linked from index, which we don't count as a page).
    for page in pages:
        if page.name == "overview.md":
            continue
        if inbound.get(page.resolve(), 0) == 0:
            report.warnings.append(f"{page.relative_to(root).as_posix()}: orphan (no inbound link from another wiki page)")

    # 5. posts.jsonl summary_page integrity (only if the index exists & is non-empty)
    posts_jsonl = root / "raw" / "posts.jsonl"
    if posts_jsonl.exists():
        import json
        for i, line in enumerate(posts_jsonl.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            sp = json.loads(line).get("summary_page")
            if sp and not (root / sp).exists():
                report.errors.append(f"raw/posts.jsonl line {i}: summary_page -> {sp} does not exist")

    return report
