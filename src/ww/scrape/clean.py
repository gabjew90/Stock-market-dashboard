"""Clean a WordPress post body (`content.rendered` HTML) into markdown."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup
from markdownify import markdownify

# Tags removed entirely (with their contents).
_DROP_TAGS = ("script", "style", "noscript", "iframe", "ins", "form")
# Class substrings whose containing element (and contents) are removed —
# Jetpack share buttons, related-posts widgets, AddToAny, etc.
_DROP_CLASS_SUBSTRINGS = ("sharedaddy", "jp-relatedposts", "addtoany", "sd-sharing")
# Attributes kept on surviving tags; everything else is stripped.
_KEEP_ATTRS = {"href", "src", "alt", "title"}
# His charts live under wp-content/uploads; used to identify "chart" images.
_CHART_SRC_MARKER = "wp-content/uploads"


@dataclass
class CleanedPost:
    markdown: str
    chart_image_urls: list[str] = field(default_factory=list)
    word_count: int = 0
    chart_count: int = 0


def clean_post_html(html: str) -> CleanedPost:
    soup = BeautifulSoup(html or "", "lxml")

    for tag_name in _DROP_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    to_drop = [
        el for el in soup.find_all(class_=True)
        if any(sub in " ".join(el.get("class") or []) for sub in _DROP_CLASS_SUBSTRINGS)
    ]
    for el in to_drop:
        el.decompose()

    # WP wraps images in <figure class="wp-caption">; unwrap so markdownify
    # renders a clean image + the caption text as a following paragraph.
    for figure in soup.find_all(["figure", "div"], class_=lambda c: c and "wp-caption" in " ".join(c if isinstance(c, list) else [c])):
        figure.unwrap()
    for cap in soup.find_all("figcaption"):
        cap.name = "p"

    # Collect chart image URLs (in document order) and strip noisy attributes.
    chart_image_urls: list[str] = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and _CHART_SRC_MARKER in src and src not in chart_image_urls:
            chart_image_urls.append(src)
    for el in soup.find_all(True):
        el.attrs = {k: v for k, v in el.attrs.items() if k in _KEEP_ATTRS}

    cleaned_html = str(soup)
    markdown = markdownify(cleaned_html, heading_style="ATX", strip=["span"]).strip()
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())

    return CleanedPost(
        markdown=markdown,
        chart_image_urls=chart_image_urls,
        word_count=word_count,
        chart_count=len(chart_image_urls),
    )
