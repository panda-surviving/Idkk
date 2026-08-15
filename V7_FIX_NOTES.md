# Yalvon360 v7 fixes

## Divergence Screener reliability
- Fixed the full-scan progress initialization bug: the real universe count is now established before any progress callback runs.
- Full scans still refuse the ten-symbol development fallback and use the complete PSX equity directory.
- Batched Yahoo `.KA` history warm-up now uses a smaller 2-year payload, 40-symbol batches, three concurrent batches, no nested yfinance thread pool, and a 10-second batch timeout.
- Direct PSX/scraper/Yahoo single-symbol providers remain the fallback for symbols missing from the batch feed.
- Scan result accounting now distinguishes usable history, insufficient-history skips, and actual provider failures.
- Personalized master matches are real conjunctions: bullish reversal = near 52-week low + bullish divergence on 1D/1W/1M + RSI <=50 (strong <=30) + downtrend structure + green Heikin-Ashi; bearish reversal = bearish divergence + RSI >=70 (strong >=90) + uptrend structure + red Heikin-Ashi.
- Bearish divergence and structure now use actual swing highs rather than switching to closing-price pivots.

## PSX live/latest market quotes
- Added a fast official PSX screener-table parser for market-wide price/change snapshots, avoiding ~555 individual company-page requests just to populate the ticker/directory.
- The global PSX LIVE ticker, All PSX Stocks and market breadth now share the complete market-wide quote snapshot.
- The app retains the last good full snapshot during temporary feed outages and only falls back to per-company pages when no prior snapshot exists.
- Quote source/status is exposed rather than silently presenting development values.

## Stock charts and indicators
- Added intraday chart windows: 1D (5-minute), 5D (15-minute), and 1H (60-minute bars over the provider's supported retention window), when Yahoo exposes PSX `.KA` intraday data.
- Intraday candles, volume, RSI, MACD and SMA/EMA overlays use the same real returned bars.
- Daily/weekly/monthly historical chart behavior remains intact.
- Fibonacci and classic pivot levels continue to be computed from the most recent completed daily session.
- Existing OHLC sanitization remains in place to prevent malformed provider values from creating impossible candle wicks.

## News & announcements
- Market-wide announcements now merge official PSX Company Announcements, PSX Notices, Corporate Briefing Sessions, CDC, SECP, NCCPL and Payout streams in parallel.
- Announcement rows are displayed directly in Yalvon360 even when PSX does not expose a document URL; document links are preserved when present.
- Stock-specific pages continue to fetch only that company's PSX filing rows.

## Verification
- `python -m py_compile app.py psx_screener.py` passes.
- `node --check static/app.js` and `node --check static/sw.js` pass.
- Existing pure/static regression tests pass: 6 tests.
- A full live PSX/Yahoo/Render scan cannot be honestly executed from this sandbox because outbound package installation/network access is unavailable; runtime code is therefore written to fail explicitly or use provider fallbacks rather than fabricate results.
