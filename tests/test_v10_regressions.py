
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding="utf-8")

def test_chart_ranges_are_true_ranges():
    app = read("app.py")
    js = read("static/app.js")
    html = read("templates/index.html")
    assert '"1H": {"kind": "intraday"' in app
    assert '"5H": {"kind": "intraday"' in app
    assert '"1D": {"kind": "daily"' in app
    assert '"5D": {"kind": "daily"' in app
    assert '"candle_interval": "5h" if cfg.get("aggregate_hours") else "1h"' in app
    assert 'cfg["label"].split("·", 1)' in app
    assert 'data-tf="5H"' in html
    assert 'display_days' in app
    assert 'aggregate_hours' in app
    assert 'genuine hourly OHLCV' in app
    assert 'd.timeframe || currentChartTimeframe' in js
    assert 'd.candle_interval' in js

def test_psx_closed_market_status_and_last_session():
    app = read("app.py")
    js = read("static/app.js")
    assert "PSX_2026_HOLIDAYS" in app
    assert '"market_status": status' in app
    assert "PSX LIVE" in js
    assert "psxStatus.last_session_date" in js

def test_insider_transactions_section_and_api():
    app = read("app.py")
    js = read("static/app.js")
    html = read("templates/index.html")
    assert '/api/psx/insider-transactions' in app
    assert 'disclosure of interest' in app
    assert 'data-page="insider"' in html
    assert 'id="insiderTransactionsList"' in html
    assert 'loadPsxInsiderTransactions' in js

def test_fundamental_values_are_not_forced_to_vendor_placeholders():
    app = read("app.py")
    js = read("static/app.js")
    assert '"eps_annual"' in app
    assert '"eps_quarterly"' in app
    assert '"dividend_yield_pct"' in app
    assert '"volume_30d_avg"' in app
    assert 'Needs data vendor' not in js[js.find('async function loadFundamentals'):js.find('function sectorRowHtml')]

def test_divergence_tables_include_volume():
    app = read("app.py")
    js = read("static/app.js")
    assert '"volume": float(df["volume"].iloc[-1])' in app
    assert '{ key: "volume", label: "Volume"' in js
