# Yalvon360 v12 fixes

## Chart semantics corrected
The chart buttons now represent the candle interval rather than a misleading display-range label:
- 1H = genuine 1-hour OHLCV candles (latest practical Yahoo intraday history)
- 5H = genuine 5-hour candles built from 1-hour OHLCV within each PSX session
- 1D = daily candles, with up to ~3 years displayed when available
- 5D = 5-trading-session candles, with up to ~10 years displayed when available
- 1M = monthly candles, up to ~15 years when source history exists
- 3M = quarterly candles, up to ~15 years
- 6M = half-year candles, up to ~15 years
- 1Y = annual candles, up to ~15 years
- 3Y = 3-year candles, up to ~30 years
- 5Y = 5-year candles, up to ~40 years
- ALL = all available daily candles

No daily fallback is used for 1H/5H. Direct Yahoo Chart API is tried first and yfinance is a second path to the same Yahoo hourly feed. If hourly OHLCV is unavailable, the API says so instead of silently relabelling daily data.

## Persistent screener results
- Added SQLite `screener_results` storage.
- PSX Stock Screener saves each criteria result plus the latest result.
- PSX Divergence Screener saves the latest full-market result to SQLite as well as the worker JSON.
- Results are restored after a Gunicorn/Render process restart on the same persistent filesystem.
- Divergence results now include scan start, completion time and duration.
- The UI shows the last completed scan timestamp at the top.

Note: Render's free service filesystem is not guaranteed to survive an instance replacement/deploy. For persistence across replacement, attach a Render persistent disk or move the result store to an external database/object store.

## PSX fundamentals
- Added Book Value / Share and P/B to the market-wide quote parser when the PSX screener publishes them.
- Existing company-page fundamental parsing continues to expose book value/break-up value, EPS, dividend, payout and financial ratios when the source publishes them.
- All PSX Stocks now displays Book Value / Share and P/B columns when available.

## PSX screener performance/reliability
- Full technical-history prefetch uses 5 years for the PSX universe, batched in parallel requests.
- Empty live quote universes trigger a real full-universe refresh instead of running a zero-stock/partial development scan.
- No ten-symbol development fallback is used for PSX screeners.
- Existing divergence worker remains out-of-process so the status endpoint stays responsive.

## Verification
- Python compilation: PASS
- JavaScript syntax: PASS
- Static/regression tests: 24 passed
- Full Flask runtime suite was not executed in this sandbox because Flask is not installed here.
