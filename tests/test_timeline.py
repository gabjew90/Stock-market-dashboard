import pandas as pd

from ww.corpus.timeline import DailyRow, build_timeline, parse_daily_update


def test_gmi_value_various_phrasings():
    assert parse_daily_update("GMI is still at the maximum of +6, and all indicators...").gmi_value == 6
    assert parse_daily_update("GMI: +2; Weakness continues; in puts or cash").gmi_value == 2
    assert parse_daily_update("The GMI is back to 6, and the window dressing...").gmi_value == 6
    assert parse_daily_update("GMI rises to 4; market trend?").gmi_value == 4
    assert parse_daily_update("GMI remains at 5 (of 6) but the longer term trend...").gmi_value == 5
    assert parse_daily_update("...GMI= 6 (of 6) and Green. Note the stocks").gmi_value == 6


def test_gmi_state():
    r = parse_daily_update("...GMI= 6 (of 6) and Green. Note the stocks")
    assert r.gmi_state == "Green"
    r2 = parse_daily_update("The GMI is still on a Buy signal from January, but is holding to a middle 3 our of 6.")
    assert r2.gmi_state == "Buy" and r2.gmi_value == 3


def test_gmi2_and_gmi_s_are_not_read_as_gmi_value():
    r = parse_daily_update("GMI-2 is now at 8 (of 8). These are a collection of very short term indicators.")
    assert r.gmi_value is None
    assert r.gmi2_value == 8
    r2 = parse_daily_update("The GMI is back to 6 but the GMI-S slipped to 63.")
    assert r2.gmi_value == 6
    assert r2.gmi_s == 63
    r3 = parse_daily_update("The GMI-S is back to 100. 84-88% of the stocks...")
    assert r3.gmi_value is None and r3.gmi_s == 100


def test_qqq_day_and_direction():
    assert parse_daily_update("Day 13 of $QQQ short term up-trend and GMI= 6").qqq_day == 13
    assert parse_daily_update("Day 13 of $QQQ short term up-trend and GMI= 6").qqq_dir == "up"
    assert parse_daily_update("The QQQQ is in the 26th day of its short term up-trend.").qqq_day == 26
    assert parse_daily_update("3rd day of $QQQ short term down-trend; small-caps out-perform").qqq_day == 3
    assert parse_daily_update("3rd day of $QQQ short term down-trend; small-caps out-perform").qqq_dir == "down"
    assert parse_daily_update("Friday was the 81st day of QQQQ up-trend.").qqq_day == 81


def test_t2108():
    assert parse_daily_update("the Worden T2108 indicator is about as high as it gets, 82%.").t2108 == 82
    assert parse_daily_update("T2108 = 45%. Stay the course.").t2108 == 45
    assert parse_daily_update("T2108 indicator at peak.").t2108 is None    # no number -> None


def test_stance_keywords():
    assert parse_daily_update("GMI: +2; in puts or cash").stance == "cash"
    assert parse_daily_update("With the QQQ now back above its 30 week average, I am ready to reenter this market.").stance == "invested"
    assert parse_daily_update("The GMI declined to 3; I get defensive in my trading IRA and raise stops.").stance == "cautious"
    assert parse_daily_update("ASGN recently re-tested its green line break-out and headed up.").stance is None


def test_parse_confidence():
    assert parse_daily_update("GMI: +6").parse_confidence == "high"
    assert parse_daily_update("Day 5 of $QQQ short term up-trend").parse_confidence == "high"
    assert parse_daily_update("Some chart commentary with no indicators mentioned at all.").parse_confidence == "flagged"


def test_build_timeline_over_the_corpus(tmp_path, monkeypatch):
    # build a tiny fake corpus: 3 posts, 2 daily_update + 1 long_form
    import json
    (tmp_path / "raw" / "posts").mkdir(parents=True)
    rows = [
        {"post_id": 1, "url": "u1", "date": "2014-01-28T00:00:00", "slug": "a", "stem": "2014-01-28-a", "title": "Day 13", "word_count": 50, "chart_count": 0, "chart_image_urls": [], "kind_guess": "daily_update"},
        {"post_id": 2, "url": "u2", "date": "2007-10-08T00:00:00", "slug": "b", "stem": "2007-10-08-b", "title": "T2108 peak", "word_count": 60, "chart_count": 0, "chart_image_urls": [], "kind_guess": "daily_update"},
        {"post_id": 3, "url": "u3", "date": "2012-07-23T00:00:00", "slug": "c", "stem": "2012-07-23-c", "title": "long teaching post", "word_count": 900, "chart_count": 0, "chart_image_urls": [], "kind_guess": "long_form"},
    ]
    (tmp_path / "raw" / "posts.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    (tmp_path / "raw" / "posts" / "2014-01-28-a.md").write_text("---\nurl: u1\n---\n\nDay 13 of $QQQ short term up-trend and GMI= 6 (of 6) and Green.\n", encoding="utf-8")
    (tmp_path / "raw" / "posts" / "2007-10-08-b.md").write_text("---\nurl: u2\n---\n\nThe GMI remains at 6, but the Worden T2108 indicator is about as high as it gets, 82%. The QQQQ is in the 26th day of its short term up-trend.\n", encoding="utf-8")
    (tmp_path / "raw" / "posts" / "2012-07-23-c.md").write_text("---\nurl: u3\n---\n\nLong teaching post about stage analysis.\n", encoding="utf-8")

    df = build_timeline(tmp_path)
    assert list(df["date"]) == [pd.Timestamp("2007-10-08T00:00:00"), pd.Timestamp("2014-01-28T00:00:00")]   # only the 2 daily updates, sorted
    r1 = df.set_index("date").loc[pd.Timestamp("2014-01-28T00:00:00")]
    assert r1["gmi_value"] == 6 and r1["gmi_state"] == "Green" and r1["qqq_day"] == 13 and r1["qqq_dir"] == "up"
    r2 = df.set_index("date").loc[pd.Timestamp("2007-10-08T00:00:00")]
    assert r2["gmi_value"] == 6 and r2["t2108"] == 82 and r2["qqq_day"] == 26 and r2["qqq_dir"] == "up"
    assert (df["parse_confidence"] == "high").all()
