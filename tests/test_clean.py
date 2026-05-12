from pathlib import Path

from ww.scrape.clean import clean_post_html


def test_clean_returns_markdown_text(fixtures_dir: Path):
    html = (fixtures_dir / "wp_post_sample.html").read_text(encoding="utf-8")
    cleaned = clean_post_html(html)
    assert "The 10 week average is finally back above its 30 week average." in cleaned.markdown
    assert "GMI = 6 (GREEN)" in cleaned.markdown


def test_clean_keeps_chart_image_as_markdown(fixtures_dir: Path):
    html = (fixtures_dir / "wp_post_sample.html").read_text(encoding="utf-8")
    cleaned = clean_post_html(html)
    assert "![QQQ weekly chart](https://wishingwealthblog.com/wp-content/uploads/2026/05/Screenshot-A.jpg)" in cleaned.markdown


def test_clean_collects_chart_image_urls(fixtures_dir: Path):
    html = (fixtures_dir / "wp_post_sample.html").read_text(encoding="utf-8")
    cleaned = clean_post_html(html)
    assert cleaned.chart_image_urls == [
        "https://wishingwealthblog.com/wp-content/uploads/2026/05/Screenshot-A.jpg"
    ]
    assert cleaned.chart_count == 1


def test_clean_drops_scripts_and_share_and_related_blocks(fixtures_dir: Path):
    html = (fixtures_dir / "wp_post_sample.html").read_text(encoding="utf-8")
    cleaned = clean_post_html(html)
    assert "tracking pixel" not in cleaned.markdown
    assert "SHARE THIS" not in cleaned.markdown
    assert "jp-relatedposts" not in cleaned.markdown
    assert "Related" not in cleaned.markdown


def test_clean_keeps_internal_links(fixtures_dir: Path):
    html = (fixtures_dir / "wp_post_sample.html").read_text(encoding="utf-8")
    cleaned = clean_post_html(html)
    assert "[my glossary](https://wishingwealthblog.com/glossary/)" in cleaned.markdown


def test_clean_counts_words():
    cleaned = clean_post_html("<p>one two three four five</p>")
    assert cleaned.word_count == 5
