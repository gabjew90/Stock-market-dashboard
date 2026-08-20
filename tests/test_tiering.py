from ww.corpus.tiering import screen, teaching_markers


class TestTeachingMarkers:
    def test_finds_first_person_rule_statements(self):
        text = "I have learned that the key to this is patience. I never average down."
        found = teaching_markers(text)
        assert "i have learned" in found
        assert "the key to" in found
        assert "i never " in found

    def test_is_case_insensitive_and_deduplicated(self):
        text = "I PREFER this. I prefer that. I prefer the other."
        assert teaching_markers(text) == {"i prefer"}

    def test_returns_empty_for_a_routine_market_note(self):
        text = "GMI = 6 (of 6). T2108 at 61%. Day 22 of the QQQ short term up-trend. 88 new highs."
        assert teaching_markers(text) == set()


class TestScreen:
    def test_routine_note_is_tiered_daily_update(self):
        s = screen(kind_guess="daily_update", word_count=40,
                   text="GMI = 6. T2108 61%. Charts below.", title="Day 22 of $QQQ short term up-trend")
        assert s.tier == "daily_update"
        assert s.hold is False

    def test_post_with_teaching_markers_is_held_not_tiered(self):
        s = screen(kind_guess="daily_update", word_count=40,
                   text="GMI = 6. I have learned that the key to this is waiting.",
                   title="Day 22 of $QQQ short term up-trend")
        assert s.hold is True
        assert s.tier is None
        assert "teaching marker" in s.reason

    def test_long_body_is_held_even_without_markers(self):
        """Length correlates with teaching; read before dismissing."""
        s = screen(kind_guess="unknown", word_count=500, text="Market commentary. " * 20, title="Some title")
        assert s.hold is True
        assert "long body" in s.reason

    def test_short_unknown_without_markers_is_tiered_daily_update(self):
        s = screen(kind_guess="unknown", word_count=30, text="Charts below.", title="Some stocks to watch")
        assert s.tier == "daily_update"
        assert s.hold is False

    def test_long_form_is_never_bulk_tiered(self):
        """long_form posts are the curated ingest queue — they must be read, never swept."""
        s = screen(kind_guess="long_form", word_count=900, text="An essay.", title="How I trade")
        assert s.hold is True
        assert s.tier is None

    def test_reason_is_populated_for_tiered_posts_too(self):
        s = screen(kind_guess="daily_update", word_count=10, text="GMI 6.", title="GMI: 6")
        assert s.reason
