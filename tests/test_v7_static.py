from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text()
JS = (ROOT / "static/app.js").read_text()
HTML = (ROOT / "templates/index.html").read_text()
SW = (ROOT / "static/sw.js").read_text()
CORE = (ROOT / "psx_screener.py").read_text()


def test_divergence_progress_has_real_universe_before_callback():
    start = APP.index("def run_psx_divergence_scan")
    body = APP[start:APP.index("def _run_psx_divergence_job_in_background", start)]
    assert 'total = len(tickers)' in body
    assert 'Preparing batched PSX history for {total} symbols' in body
    assert 'symbols_skipped_insufficient_history' in body


def test_personalized_setup_is_a_real_conjunction():
    assert 'bullish_setup = bool(is_near_low and any(tf_setup_ok(hit, "bullish") for hit in bullish_tf_hits) and ha_color == "green")' in APP
    assert 'bearish_setup = bool(any(tf_setup_ok(hit, "bearish") for hit in bearish_tf_hits) and ha_color == "red")' in APP


def test_chart_timeframes_use_explicit_candle_intervals():
    assert '"1H": {"kind": "intraday"' in APP
    assert '"5H": {"kind": "intraday"' in APP
    assert '"1D": {"kind": "daily"' in APP
    assert '"5D": {"kind": "daily"' in APP
    assert '"candle_interval": "5h" if cfg.get("aggregate_hours") else "1h"' in APP
    assert 'cfg["label"].split("·", 1)' in APP
    assert 'data-tf="1D"' in HTML and 'data-tf="1H"' in HTML


def test_quote_path_never_returns_legacy_development_prices():
    start = APP.index('def get_quote(')
    body = APP[start:APP.index('def record_daily_prices', start)]
    assert 'Development fallback' not in body
    assert 'FALLBACK_QUOTES.get(symbol)' not in body


def test_market_wide_quote_path_is_official_screener_not_dev_subset():
    assert 'PSX_SCREENER_URL' in APP
    assert 'fetch_psx_bulk_quotes' in APP
    assert 'MIN_COMPLETE_PSX_SYMBOLS = 400' in APP
    start = APP.index('def market():')
    body = APP[start:APP.index('@app.get("/api/extras")', start)]
    assert 'FALLBACK_QUOTES' not in body


def test_announcement_feed_has_multiple_official_streams():
    assert 'Corporate Briefing Sessions' in APP
    assert 'CDC Notices' in APP
    assert 'NCCPL Notices' in APP
    assert 'Payouts' in APP
    assert 'psx-360-shell-v13' in SW


def test_divergence_scans_multiple_recent_pivot_pairs():
    assert "for j in range(len(positions) - 1, 0, -1):" in CORE
    assert "for i in range(j - 1, max(-1, j - 6), -1):" in CORE


def test_multi_timeframe_setup_uses_matching_timeframe():
    assert 'tf_setup_ok(hit, "bullish")' in APP
    assert 'tf_setup_ok(hit, "bearish")' in APP
