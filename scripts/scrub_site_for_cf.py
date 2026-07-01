"""Scrub the staged _site/ copy before deploying to Cloudflare (seraphsys.us).

The seraphsys.us deployment must not reveal the GitHub account behind it:

1. Absolute https://gabjew90.github.io/Stock-market-dashboard/... nav links
   are rewritten to relative paths.
2. The pulse page's client-side fetches to raw.githubusercontent.com are
   rewritten to same-origin /pulse-data/... paths; the Cloudflare Worker
   (deploy/cloudflare/src/index.js) proxies those upstream server-side, so
   visitors' browsers never contact GitHub.
3. Comments naming the upstream repo/hosts are neutralized.
4. LEAK GATE: after rewriting, every served file is scanned for identifying
   strings — any hit fails the build so a leak can never reach production.

Usage: python scripts/scrub_site_for_cf.py _site
"""

import re
import sys
from pathlib import Path

NEEDLES = ("gabjew90", "Institutional-report", "github", "githack", "jsdelivr")

PULSE_CONSTANTS = re.compile(
    r"const REPO = 'gabjew90/Institutional-report-bot';.*?"
    r"const FRAGMENT_BASE = `https://\$\{RAW_HOST\}/\$\{REPO\}/\$\{BRANCH\}/pulse-output/web/fragments`;",
    re.DOTALL,
)
PULSE_CONSTANTS_REPLACEMENT = (
    "const ARCHIVE_URL = '/pulse-data/archive.json';\n"
    "  const FRAGMENT_BASE = '/pulse-data/fragments';"
)

NORMALIZE_FUNC = re.compile(r"function normalizeRawUrl\(url\) \{.*?\n  \}", re.DOTALL)
NORMALIZE_REPLACEMENT = (
    "function normalizeRawUrl(url) {\n"
    "    if (!url) return url;\n"
    "    const m = String(url).match(/\\/fragments\\/([^\\/?#]+)$/);\n"
    "    return m ? `${FRAGMENT_BASE}/${m[1]}` : url;\n"
    "  }"
)

HOSTING_COMMENT = re.compile(
    r"// The pulse content lives in a separate project.*?// was returning 403 intermittently\.",
    re.DOTALL,
)
TODO_COMMENT = re.compile(
    r"// TODO\(remove-after-upstream-host-fix\):.*?drop this shim and the call below\.",
    re.DOTALL,
)


def scrub_common(text: str) -> str:
    text = text.replace("https://gabjew90.github.io/Stock-market-dashboard/pulse/", "./pulse/")
    text = text.replace("https://gabjew90.github.io/Stock-market-dashboard/", "./")
    return text


def scrub_pulse(text: str) -> str:
    text = PULSE_CONSTANTS.sub(PULSE_CONSTANTS_REPLACEMENT, text)
    text = NORMALIZE_FUNC.sub(NORMALIZE_REPLACEMENT, text)
    text = HOSTING_COMMENT.sub(
        "// Pulse content is served same-origin from /pulse-data/ (proxied by the site worker).",
        text,
    )
    text = TODO_COMMENT.sub(
        "// Fragment URLs from older archive entries are remapped onto the same-origin path.",
        text,
    )
    text = re.sub(r"Institutional-report-\s*//\s*bot", "the upstream feed", text)
    text = text.replace("Institutional-report-bot", "the upstream bridge")
    text = text.replace("raw.githubusercontent.com", "the upstream host")
    text = text.replace("raw.githack.com", "a prior host")
    text = text.replace("cdn.jsdelivr.net", "a prior host")
    text = text.replace("gabjew90", "")
    return text


def main(site_dir: str) -> int:
    site = Path(site_dir)
    if not site.is_dir():
        print(f"::error::site dir not found: {site}")
        return 1

    for path in site.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        text = scrub_common(text)
        if path.parent.name == "pulse":
            text = scrub_pulse(text)
        path.write_text(text, encoding="utf-8")

    # Leak gate: nothing identifying may survive in ANY served file.
    leaks = []
    for path in site.rglob("*"):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        for needle in NEEDLES:
            if needle.lower() in content:
                leaks.append(f"{path.relative_to(site)} -> '{needle}'")
    if leaks:
        for leak in leaks:
            print(f"::error::leak gate: {leak}")
        return 1

    print(f"scrubbed OK — leak gate clean across {sum(1 for _ in site.rglob('*') if _.is_file())} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_site"))
