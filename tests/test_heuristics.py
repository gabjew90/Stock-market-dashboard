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
