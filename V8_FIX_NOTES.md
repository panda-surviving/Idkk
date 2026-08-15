# Yalvon360 PSX Divergence Screener — v8 reliability/performance fix

## Production problem fixed
The browser was receiving an HTML `502` from `/api/psxdivergence/scan/status/<job_id>` while the full PSX scan was running. The expensive scan was running inside the same Gunicorn web worker, so heavy Yahoo/PSX I/O plus pandas calculations could starve or kill the web worker. The browser then tried to parse the proxy's HTML 502 as JSON.

## v8 changes
- Moved the PSX divergence scan into a separate Python worker process (`psx_divergence_worker.py`).
- The Gunicorn web process now stays responsive to start/status/cached requests while the scan runs.
- Scan progress and the latest full result are file-backed in `.psx_divergence_jobs/`, so a Gunicorn restart no longer automatically loses the job status/result.
- Status endpoint is deliberately tiny and reads the job state directly from disk.
- Stale/dead worker PIDs are detected and converted to a clear scan error instead of leaving the UI spinning forever.
- Duplicate Run Scan clicks/reloads reuse the active full-market job instead of launching another 555-symbol scan.
- Yahoo batch history prefetch is tuned to 75 symbols/request and 2 concurrent batch requests; per-symbol analysis uses 4 workers. This reduces connection bursts and CPU/memory contention on Render free tier while keeping the scan parallel.
- Frontend status polling retries transient HTML 502/network failures instead of immediately discarding a valid long-running scan.
- Gunicorn request threads reduced from 8 to 4 because the expensive scan is no longer sharing the web worker.

## Data/logic preserved
The scan still requires the complete PSX universe guard, 52-week-low <=3% condition, independent 1D/1W/1M RSI divergence checks, bullish <=50 / strong <=30 and bearish >=70 / strong >=90 zones, Heikin-Ashi confirmation, and trend-structure confirmation.

## Important runtime behavior
The first scan on a cold Render instance can still take time because real market history must be downloaded. Subsequent scans are substantially faster because the in-process history cache is reused while the persistent latest result is available immediately. The worker is intentionally separated from the web process so scan duration no longer causes the status API itself to time out.
