"""Mechanical integrity checks over the wiki/ directory."""
from __future__ import annotations

import json
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


#: A citation into the corpus: `.../raw/posts/<stem>.md`, at any `../` depth.
_POST_CITATION = re.compile(r"raw/posts/([0-9]{4}-[0-9]{2}-[0-9]{2}-[^)\s]+?)\.md")
_SOURCES_HEADING = re.compile(r"^##\s+Sources\s*$", flags=re.MULTILINE)
#: A line that is nothing but a bare XML-ish closing tag, e.g. `</content>` or `</invoke>`.
_LEAKED_MARKUP = re.compile(r"^\s*</[a-zA-Z][\w-]*>\s*$")


def _is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def _uncited_in_sources(text: str) -> set[str]:
    """Post stems cited in a page's body but absent from its '## Sources' block.

    The Sources block is the page's bibliography (CLAUDE.md §3.4); a claim cited inline
    from a post that the block never lists leaves the page's provenance incomplete. Returns
    an empty set for pages with no Sources heading — the missing heading is reported
    separately.
    """
    m = _SOURCES_HEADING.search(text)
    if not m:
        return set()
    body, sources = text[: m.start()], text[m.end() :]
    return set(_POST_CITATION.findall(body)) - set(_POST_CITATION.findall(sources))


_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", flags=re.S)
_REQUIRED_KEYS = ("title", "type", "updated", "sources")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _front_matter_issues(text: str) -> tuple[list[str], set[str] | None]:
    """Return (issues, front-matter source stems or None if unparseable).

    CLAUDE.md §3.1 requires `title`, `type`, `updated` (YYYY-MM-DD) and `sources` on every
    page. `sources` is parsed as either an inline `[a, b]` list or a `- item` block and
    reduced to post stems for comparison with the `## Sources` block.
    """
    m = _FRONT_MATTER.match(text)
    if not m:
        return ["front-matter missing (page must start with a `---` YAML block)"], None
    fm = m.group(1)
    issues: list[str] = []
    keys = {ln.split(":", 1)[0].strip() for ln in fm.splitlines() if ":" in ln and not ln.startswith((" ", "-"))}
    for k in _REQUIRED_KEYS:
        if k not in keys:
            issues.append(f"front-matter missing required key `{k}`")
    um = re.search(r"^updated:\s*(.+?)\s*$", fm, flags=re.M)
    if um and not _ISO_DATE.match(um.group(1).strip("'\"")):
        issues.append(f"front-matter `updated:` must be YYYY-MM-DD, got `{um.group(1)}`")
    stems = set(_POST_CITATION.findall(fm))
    return issues, stems


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

    # raw/posts/ is committed as of 2026-08-12, so citation links into the corpus are
    # normally verified. This fallback remains for partial checkouts (sparse clones,
    # or a tree where raw/ was cleaned): skip raw/ links with a warning rather than
    # flag every citation in the wiki as broken.
    raw_dir = (root / "raw").resolve()
    corpus_present = (root / "raw" / "posts").is_dir()
    unverified_raw_links = 0

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
            if not corpus_present and dest.is_relative_to(raw_dir):
                unverified_raw_links += 1
                continue
            if not dest.exists():
                report.errors.append(f"{rel}: broken link -> {target}")
                continue
            if dest in inbound and dest != page.resolve():
                inbound[dest] += 1

        # 3. Page catalogued in index.md? (overview/methodology/playbooks/history/sources pages)
        if page.resolve() not in index_pages:
            # sources/.gitkeep style files won't be .md; .md pages must be indexed.
            report.errors.append(f"{rel}: not catalogued in wiki/index.md")

        # 3b. Leaked tool markup. Editing tools that wrap file content in XML-ish tags have
        #     left bare closing tags (`</content>`, `</invoke>`) at the end of pages; a bare
        #     closing tag on its own line is never legitimate wiki prose.
        for lineno, line in enumerate(text.splitlines(), start=1):
            if _LEAKED_MARKUP.match(line):
                report.errors.append(f"{rel}:{lineno}: leaked tool markup `{line.strip()}`")

        # 3c. Front-matter present and well-formed (CLAUDE.md §3.1), and its `sources:` list
        #     agrees with the `## Sources` block — they are the same bibliography twice, and
        #     when they disagree a reader cannot tell which is complete.
        fm_issues, fm_stems = _front_matter_issues(text)
        for issue in fm_issues:
            report.errors.append(f"{rel}: {issue}")
        if fm_stems is not None:
            sm = _SOURCES_HEADING.search(text)
            if sm:
                block_stems = set(_POST_CITATION.findall(text[sm.end():]))
                for stem in sorted(block_stems - fm_stems):
                    report.errors.append(f"{rel}: '## Sources' lists raw/posts/{stem}.md but front-matter `sources:` does not")
                for stem in sorted(fm_stems - block_stems):
                    report.errors.append(f"{rel}: front-matter `sources:` lists raw/posts/{stem}.md but '## Sources' does not")

        # 4. Every post cited in the body is listed in the page's own '## Sources' block
        #    (CLAUDE.md §3.4). Checked on the text, so it works without the corpus.
        for stem in sorted(_uncited_in_sources(text)):
            report.errors.append(f"{rel}: cites raw/posts/{stem}.md but does not list it under '## Sources'")

    # 4b. Leaked tool markup in code as well as prose. The same tag leak that hit the wiki
    #     landed in a .py file during the 2026-08-12 fix pass and produced a SyntaxError.
    for code_dir in ("src", "tests"):
        code_root = root / code_dir
        if not code_root.is_dir():
            continue
        for path in sorted(code_root.rglob("*.py")):
            try:
                for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                    if _LEAKED_MARKUP.match(line):
                        report.errors.append(f"{path.relative_to(root).as_posix()}:{lineno}: leaked tool markup `{line.strip()}`")
            except UnicodeDecodeError:
                continue

    # 5. Orphan pages (no inbound link from another wiki page). overview.md is explicitly exempt as a safety net — it's the entry page.
    for page in pages:
        if page.name == "overview.md":
            continue
        if inbound.get(page.resolve(), 0) == 0:
            report.warnings.append(f"{page.relative_to(root).as_posix()}: orphan (no inbound link from another wiki page)")

    if unverified_raw_links:
        report.warnings.append(
            f"raw/ corpus not present — {unverified_raw_links} link targets under raw/ not verified (rebuild with `ww scrape`)"
        )

    # 6. summary_page integrity for the corpus index and the committed ingest ledger.
    #    Both are committed as of 2026-08-12; each is skipped if absent so the check still
    #    works on a partial checkout.
    for rel_path in ("raw/posts.jsonl", "raw/ingest-ledger.jsonl"):
        jsonl = root / rel_path
        if not jsonl.exists():
            continue
        for i, line in enumerate(jsonl.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            sp = json.loads(line).get("summary_page")
            if sp and not (root / sp).exists():
                report.errors.append(f"{rel_path} line {i}: summary_page -> {sp} does not exist")

    return report
