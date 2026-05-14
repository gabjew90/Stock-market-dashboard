"""Build all three site pages and stage them to litterbox.catbox.moe for a 72-h preview.

Pages staged:
* GMI Daily      — built by scripts/build_gmi_playground.py
* Methodology    — built by scripts/build_wiki_html.py
* Daily Pulse    — static at web/pulse.html (owned by the other Claude session)

Usage:
    uv run python scripts/stage_all.py                # nav links go to production
    uv run python scripts/stage_all.py --cross-link   # 2-pass: nav links cross-reference the staging set

With --cross-link, each staged file's nav block is patched to point at the *other two* staging URLs
before a final upload. Note: the FINAL URLs are the pass-2 URLs; clicking through their nav links
arrives at the pass-1 URLs (which carry the same content, just with production nav). Same content
either way; only the navigation chain differs by one hop. Good enough for visual review.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROD = "https://gabjew90.github.io/Stock-market-dashboard"
PROD_GMI = f"{PROD}/"
PROD_PULSE = f"{PROD}/pulse/"
PROD_WIKI = f"{PROD}/wiki.html"

# Each page's nav block currently uses a different link style — normalise to absolute
# production URLs first, then we can find-and-replace those with staging URLs.
# (Build scripts may emit any of these; static pulse.html has its own.)
RELATIVE_TO_ABSOLUTE = {
    # GMI playground already uses absolute prod URLs (since 185c7b3)
    # Wiki uses ./, ./pulse/, ./wiki.html
    "wiki": [
        (re.compile(r'href="\./"'),               f'href="{PROD_GMI}"'),
        (re.compile(r'href="\./pulse/"'),         f'href="{PROD_PULSE}"'),
        (re.compile(r'href="\./wiki\.html"'),     f'href="{PROD_WIKI}"'),
    ],
    # Pulse uses ../, ../wiki.html, ./
    "pulse": [
        (re.compile(r'href="\.\./"'),             f'href="{PROD_GMI}"'),
        (re.compile(r'href="\.\./wiki\.html"'),   f'href="{PROD_WIKI}"'),
        (re.compile(r'href="\./"'),               f'href="{PROD_PULSE}"'),
    ],
    "gmi": [],  # already absolute
}


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, check=True, **kw)


def build_gmi() -> Path:
    print("==> building GMI Daily...")
    run(["uv", "run", "python", "scripts/build_gmi_playground.py"])
    return ROOT / "gmi_playground_daily.html"


def build_wiki() -> Path:
    print("==> building Methodology wiki...")
    run(["uv", "run", "--with", "markdown", "--with", "pygments",
         "python", "scripts/build_wiki_html.py"])
    return ROOT / "wiki_site.html"


def get_pulse() -> Path:
    return ROOT / "web" / "pulse.html"


def upload(path: Path, label: str) -> str:
    print(f"==> uploading {label} ({path.stat().st_size // 1024} KB)...")
    r = subprocess.run(
        ["curl", "-k", "--max-time", "180", "-s",
         "-F", "reqtype=fileupload", "-F", "time=72h",
         "-F", f"fileToUpload=@{path.as_posix()}",
         "https://litterbox.catbox.moe/resources/internals/api.php"],
        capture_output=True, text=True, cwd=ROOT,
    )
    url = r.stdout.strip()
    if not url.startswith("https://"):
        print(f"upload failed for {path.name}: {url}", file=sys.stderr)
        sys.exit(1)
    print(f"    -> {url}")
    return url


def normalize_nav(content: str, page: str) -> str:
    """Convert this page's relative nav URLs to absolute production URLs."""
    for pat, repl in RELATIVE_TO_ABSOLUTE.get(page, []):
        content = pat.sub(repl, content)
    return content


def patch_to_staging(content: str, urls: dict[str, str]) -> str:
    """Replace production nav URLs with staging URLs. More specific patterns FIRST."""
    content = content.replace(PROD_PULSE, urls["pulse"])
    content = content.replace(PROD_WIKI, urls["wiki"])
    content = content.replace(PROD_GMI, urls["gmi"])
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cross-link", action="store_true",
                        help="Do a 2-pass upload that patches each file's nav to cross-reference the staging set "
                             "(otherwise nav links go to production).")
    args = parser.parse_args()

    # Build / locate the three files
    gmi_path = build_gmi()
    wiki_path = build_wiki()
    pulse_path = get_pulse()

    # Normalise their nav blocks to absolute production URLs (so the patcher has a uniform target)
    for label, p in [("gmi", gmi_path), ("wiki", wiki_path), ("pulse", pulse_path)]:
        original = p.read_text(encoding="utf-8")
        normalised = normalize_nav(original, label)
        if normalised != original:
            # Write a sibling .staged.html file so we don't mutate the canonical wiki/pulse content
            staged = p.with_suffix(".staged.html")
            staged.write_text(normalised, encoding="utf-8")
            if label == "wiki": wiki_path = staged
            elif label == "pulse": pulse_path = staged
            elif label == "gmi": gmi_path = staged

    # Pass 1: upload all three (nav links currently point at production)
    print()
    urls = {
        "gmi": upload(gmi_path, "GMI Daily"),
        "wiki": upload(wiki_path, "Methodology"),
        "pulse": upload(pulse_path, "Daily Pulse"),
    }

    if args.cross_link:
        print("\n==> cross-link mode: patching nav links and re-uploading...")
        urls_v2 = {}
        for label, p in [("gmi", gmi_path), ("wiki", wiki_path), ("pulse", pulse_path)]:
            content = p.read_text(encoding="utf-8")
            patched = patch_to_staging(content, urls)
            crosslink_path = p.with_suffix(".xlinked.html")
            crosslink_path.write_text(patched, encoding="utf-8")
            urls_v2[label] = upload(crosslink_path, f"{label} (cross-linked)")
            crosslink_path.unlink(missing_ok=True)
        urls = urls_v2

    # Cleanup any .staged.html sibling files we created
    for p in [gmi_path, wiki_path, pulse_path]:
        if p.name.endswith(".staged.html"):
            p.unlink(missing_ok=True)
    # And the originals from the build scripts
    (ROOT / "gmi_playground_daily.html").unlink(missing_ok=True)
    (ROOT / "wiki_site.html").unlink(missing_ok=True)

    print()
    print("=" * 72)
    print("STAGING URLS (72-h preview):")
    print(f"  GMI Daily:   {urls['gmi']}")
    print(f"  Daily Pulse: {urls['pulse']}")
    print(f"  Methodology: {urls['wiki']}")
    print("=" * 72)
    if not args.cross_link:
        print("Nav links go to production. Use --cross-link to cross-reference the staging set.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
