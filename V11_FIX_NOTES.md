# Yalvon360 v11 fixes

- 1H and 5H charts now request genuine 1-hour OHLCV candles.
- 1D and 5D charts now use genuine daily candles; 1D is a 30-trading-day daily-candle view and 5D is the latest 5 daily candles.
- Chart API exposes `candle_interval` and the UI displays the actual candle interval/source.
- Removed the misleading “Waiting for the latest PSX snapshot” ticker fallback. Closed markets retain the `PSX LIVE · CLOSED · LAST SESSION` label without pretending a snapshot is loading.
- Added latest-session, 1-week and 1-month cumulative volume plus 1-week/1-month average daily volume to PSX stock fundamentals.
- Added source-backed PSX fields when actually published: face value, dividend/share, payout ratio, debt/equity, current ratio, ROE and ROA. Missing source fields remain blank rather than fabricated.
- Bumped service-worker cache to v11 so deployed browsers do not keep the old chart JavaScript.
- Static/regression verification: 19 tests passed. Full Flask runtime tests were not run in this sandbox because Flask is not installed.
