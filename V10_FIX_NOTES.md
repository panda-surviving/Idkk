# V10 Fix Notes

## Chart ranges
- Fixed the old `1H` configuration that requested 60 days of hourly candles.
- Added `5H`.
- `1H`: 5-minute candles, last 1 hour of the latest available session.
- `5H`: 5-minute candles, last 5 hours of the latest available session.
- `1D`: 15-minute candles for the latest available PSX session.
- `5D`: 30-minute candles for the latest 5-day window.
- Longer ranges remain daily/weekly/monthly historical charts.
- The chart status now states the actual provider interval.

## PSX ticker / market status
- `/api/stocks/live` now returns PSX regular-market status and last session date.
- On a closed day the ticker remains `PSX LIVE` but explicitly says `CLOSED · LAST SESSION ...`.
- A cold instance makes one real full-universe quote refresh before returning an empty ticker, instead of leaving the bar indefinitely on a warming message.
- The status schedule follows PSX's published regular-market hours and 2026 holiday calendar.

## Insider Transactions
- Added Research → Insider Transactions.
- New endpoint: `/api/psx/insider-transactions`.
- It filters official PSX company announcements for director/CEO/executive/substantial-shareholder interest disclosures and trade-related filings.
- Filing titles, dates and official document links are displayed as published; transaction quantities are not invented from headlines.

## Fundamentals / volume
- PSX company-page parser now extracts annual/quarterly EPS when the tables expose them.
- Calculates TTM EPS as FY EPS minus prior Q1 EPS plus current Q1 EPS when all required values are present.
- Parses book value, P/B, dividend yield and equity-profile fields when actually published.
- Uses the official PSX market-wide screener for EPS/dividend yield/30-day average volume when those columns exist.
- All PSX Stocks now shows current volume, 30D average volume, P/E, EPS and dividend yield.
- Stock fundamentals now show current volume and 30D average volume.

## Divergence
- Divergence result tables now include the latest volume for each scanned symbol.

## Verification
- Python compile: PASS.
- JavaScript syntax: PASS.
- Static/regression tests: 19 PASS.
- Full pytest collection could not run in this sandbox because Flask is not installed and outbound package installation is unavailable.
