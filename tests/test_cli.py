import json
from pathlib import Path

import httpx
from typer.testing import CliRunner

from ww import cli
from ww.scrape import ingest as ingest_mod

runner = CliRunner()


def test_stats_command_empty(tmp_path: Path):
    result = runner.invoke(cli.app, ["stats", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "total_posts: 0" in result.stdout


def test_scrape_command_uses_root_and_reports_count(fixtures_dir, tmp_path, monkeypatch):
    page1 = json.loads((fixtures_dir / "wp_api_page1.json").read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page == 1:
            return httpx.Response(200, json=page1, headers={"X-WP-TotalPages": "1"})
        return httpx.Response(400, json={"code": "rest_post_invalid_page_number"})

    real_scrape = ingest_mod.scrape_blog

    def patched(base_url="https://wishingwealthblog.com", **kw):
        kw.setdefault("client", httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example.test"))
        kw["delay"] = 0.0
        return real_scrape("https://example.test", **kw)

    monkeypatch.setattr(cli, "scrape_blog", patched)

    result = runner.invoke(cli.app, ["scrape", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "2 posts" in result.stdout
    assert (tmp_path / "raw" / "posts.jsonl").exists()

    # And `ww stats` then reads it back:
    result2 = runner.invoke(cli.app, ["stats", "--root", str(tmp_path)])
    assert result2.exit_code == 0
    assert "total_posts: 2" in result2.stdout
