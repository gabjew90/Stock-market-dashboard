from ww.corpus.heuristics import kind_guess


def test_short_post_mentioning_gmi_is_daily_update():
    text = "GMI = 6 (GREEN). T2108 = 61%. QQQ short-term up-trend day 22. Stay the course."
    assert kind_guess(word_count=18, chart_count=1, text=text) == "daily_update"


def test_short_post_without_indicator_words_is_unknown():
    assert kind_guess(word_count=40, chart_count=0, text="Quick note about a webinar tomorrow.") == "unknown"


def test_long_post_is_long_form_even_with_indicator_words():
    text = "Today GMI is green. " + ("methodology " * 800)
    assert kind_guess(word_count=820, chart_count=0, text=text) == "long_form"


def test_medium_length_is_unknown():
    assert kind_guess(word_count=400, chart_count=2, text="Some market commentary without the trigger words.") == "unknown"


def test_indicator_match_is_case_insensitive_and_word_bounded():
    assert kind_guess(word_count=12, chart_count=0, text="gmi flipped to green today, t2108 rising") == "daily_update"
    # 'algmix' should not count as a GMI mention
    assert kind_guess(word_count=12, chart_count=0, text="algmix is not an indicator name at all here") == "unknown"


def test_title_only_daily_post_is_daily_update():
    """485 posts in the corpus have an EMPTY body — the whole post is the title, e.g.
    '41st day of $QQQ short term up-trend'. With text='' the body regex has nothing to
    match, so these were 'unknown' and excluded from raw/timeline.parquet."""
    assert kind_guess(word_count=0, chart_count=1, text="",
                      title="41st day of $QQQ short term up-trend") == "daily_update"


def test_daily_title_pattern_wins_for_short_bodies():
    # 1,861 'unknown' posts carry a daily marker in the title but not the body.
    assert kind_guess(word_count=30, chart_count=2, text="See the chart below.",
                      title="Blog Post: Day 12 of $QQQ short term up-trend; 88 US new highs") == "daily_update"
    assert kind_guess(word_count=15, chart_count=1, text="Charts.", title="GMI:3; GMI-R:5; QQQQ weakens") == "daily_update"


def test_daily_title_does_not_override_a_long_body():
    # A long essay whose title happens to carry the day count is still long_form.
    assert kind_guess(word_count=900, chart_count=0, text="x " * 900,
                      title="Day 5 of $QQQ short term up-trend; my full trading philosophy") == "long_form"


def test_title_is_optional_for_backward_compatibility():
    assert kind_guess(word_count=12, chart_count=0, text="gmi flipped to green today") == "daily_update"
