from ww.paths import post_stem


def test_post_stem_prefixes_iso_date():
    assert post_stem("2026-05-10T18:47:42", "day-22-of-qqq-up-trend") == "2026-05-10-day-22-of-qqq-up-trend"


def test_post_stem_accepts_date_only():
    assert post_stem("2005-04-17", "april-17-2005-short-or-in-cash") == "2005-04-17-april-17-2005-short-or-in-cash"


def test_post_stem_truncates_very_long_slugs():
    long_slug = "a" * 200
    stem = post_stem("2020-01-01T00:00:00", long_slug)
    assert stem.startswith("2020-01-01-")
    assert len(stem) <= 120


def test_post_stem_strips_unsafe_chars():
    assert post_stem("2020-01-01", "weird/slug:with*chars") == "2020-01-01-weird-slug-with-chars"
