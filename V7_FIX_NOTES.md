# Yalvon360 PSX Hub — V7 Fix Notes

## Major fixes

- PSX live feed no longer replaces a good last-session snapshot with an all-blank response.
- PSX quote chain is now: official company page -> official PSX timeseries price -> Yahoo Finance `.KA` secondary real-market quote. Development sample quotes are no longer exposed by `/api/stocks/live`.
- Market banner distinguishes `LIVE`, `CLOSED • LAST SESSION`, and `FEED UNAVAILABLE`.
- Interactive chart timeframe semantics were corrected:
  - `1H` = genuine 60-minute candles only
  - `5H` = 5-hour candles aggregated from genuine hourly OHLCV only
  - `1D` = daily candles across 12 years where available
  - `5D` = 5-day candles
  - `1M` = monthly candles
  - `3M` = quarterly candles
  - `6M` = half-year candles
  - `1Y` = annual candles across 25 years where available
  - `3Y`, `5Y`, `ALL` = longer-period real history
- The app explicitly refuses to manufacture hourly candles from daily candles.
- Added EPS, book value/share, dividend yield/share, market cap and shares-outstanding extraction when the real source publishes them.
- Added 1D/1W/1M/30D-average volume fields to the stock API and stock directory when real recorded daily volume exists.
- Screener results now have a persistent SQLite cache and include `last_scan_at`. A persistent Render disk can be enabled with `PSX_PERSISTENT_DATA_DIR=/data` for restart survival.
- Added `/api/screener/check-stock` and a manual “Check One Stock” UI to compare one PSX stock against selected technical screener conditions.
- Divergence/technical cached results are also written to the same persistent cache.

## Important data-integrity rule

No synthetic/fake market candles or fake fundamentals are inserted. If a genuine provider does not supply a requested interval/value, the UI reports it as unavailable rather than inventing a number.

## Render commands

Build: `pip install -r requirements.txt`

Start: `gunicorn app:app --workers 1 --threads 8 --timeout 120 --keep-alive 5`
