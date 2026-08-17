# Yalvon360 / PSX Hub — V8 Fix Notes

## Major production fixes

### 1. PSX live/all-stocks data no longer depends on 555+ individual quote requests
The primary quote snapshot now uses two PSX public bulk tables:
- `/screener` for P/E, dividend yield, 1-year change, 30-day average volume, market cap and price.
- `/indices/ALLSHR` for current/most-recent price, change, LDCP, volume, shares and market cap.

The two snapshots are merged by symbol. This reduces a full-market refresh to a handful of requests instead of hundreds of per-stock requests.

### 2. Last successful PSX snapshot survives Render restarts
The complete quote snapshot is persisted in the existing SQLite `screener_runs` table under `__bulk_quotes__`. If a Render instance wakes up with no in-memory cache, the last successful snapshot is loaded immediately and a fresh bulk refresh runs in the background.

### 3. PSX ticker status
The ticker now distinguishes:
- LIVE (public feed may be delayed up to 5 minutes)
- CLOSED — showing the last successful session
- FEED_UNAVAILABLE — only when there is genuinely no cached/bulk data

No fake prices are generated.

### 4. Mutual Funds / MUFAP
The previous parser used the old `nav-all.php` column positions and therefore read the wrong fields. V8 uses MUFAP's current **NAV / Daily Prices Announcement** table and maps columns by header name.

It now captures:
- Fund
- Category
- Inception date
- Offer price
- Repurchase price
- NAV
- NAV validity date
- Front/back load where published
- AUM/AMC metadata from the bundled directory

No NAV is invented when MUFAP is unreachable.

### 5. Screener 0/0 failure
If the PSX universe is empty, the screener no longer pretends a zero-stock scan completed. It explicitly reports that no scan was run and preserves the previous saved result.

### 6. Divergence scanner crash fixed
The market-wide divergence scanner referenced `total` before assigning it during its prefetch progress callback. V8 assigns the universe count before progress reporting, removing that crash.

The divergence scanner also reuses the complete live PSX universe first, avoiding a duplicate symbol-directory request.

### 7. Company quote fast path
Company pages first use the bulk PSX snapshot instead of issuing another individual quote request. The old provider chain remains as a secondary fallback.

## Real-data policy

V8 does not fabricate hourly candles or fundamental values. If a genuine provider does not publish a requested interval/field, the UI must say so rather than create a value.

PSX's public Data Portal currently labels its market data as delayed by 5 minutes unless otherwise indicated. Commercial/public redistribution of PSX market data requires the appropriate PSX rights/license.

## Render

Recommended start command:

`gunicorn app:app --workers 1 --threads 8 --timeout 120 --keep-alive 5`

Build/install:

`pip install -r requirements.txt`

For persistent scanner/snapshot history on Render, use a persistent disk and set:

`PSX_PERSISTENT_DATA_DIR=/data`
