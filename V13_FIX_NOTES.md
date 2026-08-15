# Yalvon360 V13

- Restored the missing 1Y chart button (v12 had a duplicate 1D button).
- 1D remains true daily candles across multi-year history; 1Y is true yearly OHLCV candles across available history.
- 1H/5H are strict genuine intraday charts. No daily fallback is permitted.
- Added licensed Capital Stake PSX intraday source (5m exchange-derived bars) and optional Twelve Data XKAR 1h source before Yahoo.
- Added Capital Stake key-metrics enrichment for book value/share, P/B, EPS, dividend yield and other published fundamentals when a token is configured.
- Added licensed Capital Stake insider transaction feed with transaction name/type/price/shares when configured; PSX announcement scrape remains fallback.
- Added manual Technical Screener stock audit: `/api/screener/stock-verdict/<SYMBOL>` and UI in the Screener page.
- Manual audit reports PASS/FAIL/UNAVAILABLE for live technical criteria and separately audits the personalized RSI-divergence setup.
- Service-worker cache bumped to v13.
