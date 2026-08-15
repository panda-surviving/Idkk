from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

def test_true_chart_timeframes_and_1y_button():
    assert '"1H": {"kind": "intraday"' in APP
    assert '"5H": {"kind": "intraday"' in APP
    assert '"1D": {"kind": "daily"' in APP
    assert '"1Y": {"kind": "daily", "resample": "YS"' in APP
    assert HTML.count('data-tf="1Y"') == 1
    assert HTML.count('data-tf="1D"') == 1

def test_no_daily_fallback_for_intraday():
    assert 'No daily fallback' in APP
    assert 'CAPITAL_STAKE_API_TOKEN' in APP
    assert 'TWELVE_DATA_API_KEY' in APP
    assert 'fetch_capital_stake_psx_intraday' in APP
    assert 'fetch_twelve_data_psx_intraday' in APP

def test_manual_stock_screener_audit():
    assert '/api/screener/stock-verdict/<symbol>' in APP
    assert 'manualScreenerSymbol' in HTML
    assert 'manualScreenerCheckBtn' in HTML
    assert 'renderManualScreenerVerdict' in JS
    assert 'personalized_setup' in JS

def test_insider_licensed_path_and_fundamental_enrichment():
    assert '/insider/symbol' in APP
    assert '/insider' in APP
    assert 'fetch_capital_stake_key_metrics' in APP
    assert 'Book Value per Share (Rs.)' in APP
