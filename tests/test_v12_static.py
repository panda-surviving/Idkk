from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text()
JS = (ROOT / 'static/app.js').read_text()
HTML = (ROOT / 'templates/index.html').read_text()
SW = (ROOT / 'static/sw.js').read_text()


def test_chart_buttons_are_candle_intervals():
    assert '"1H": {"kind": "intraday"' in APP
    assert '"5H": {"kind": "intraday"' in APP
    assert '"1D": {"kind": "daily"' in APP
    assert '"5D": {"kind": "daily"' in APP
    assert '"1Y": {"kind": "daily", "resample": "YS"' in APP
    assert '"3Y": {"kind": "daily", "resample": "3YS"' in APP
    assert '"5Y": {"kind": "daily", "resample": "5YS"' in APP
    assert '_group_ohlc_by_trading_days' in APP
    assert '_group_intraday_hours' in APP
    assert 'real hourly OHLCV' in APP


def test_intraday_never_falls_back_to_daily():
    start = APP.index('def stock_chart(symbol):')
    body = APP[start:]
    assert 'fetch_yahoo_psx_intraday' in body
    assert 'No daily fallback' in body


def test_scan_results_persist_in_sqlite():
    assert 'CREATE TABLE IF NOT EXISTS screener_results' in APP
    assert 'psxdivergence_latest' in APP
    assert 'def _save_screener_result' in APP
    assert 'def screener_last' in APP
    assert 'Last completed scan' in JS
    assert '/api/screener/last' in JS


def test_fundamental_book_value_is_wired():
    assert 'book_value_per_share' in APP
    assert 'i_bvps' in APP
    assert 'Book Value / Share' in JS
    assert 'Book Value / Share' in HTML
    assert '<th>P/B</th>' in HTML


def test_service_worker_is_bumped():
    assert 'psx-360-shell-v12' in SW
