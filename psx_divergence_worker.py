"""Out-of-process PSX divergence scanner for Render/Gunicorn reliability."""
import json
import os
import time
from pathlib import Path

JOB_ID = os.environ.get("PSX_SCAN_JOB_ID", "").strip()
if not JOB_ID:
    raise SystemExit("PSX_SCAN_JOB_ID is required")

import app

JOB_DIR = app.PSX_DIVERGENCE_JOB_DIR
JOB_PATH = JOB_DIR / f"{JOB_ID}.json"
RESULT_PATH = JOB_DIR / "latest_result.json"


def read_job():
    try:
        return json.loads(JOB_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"job_id": JOB_ID}


def write_job(payload):
    tmp = JOB_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(app._clean_for_json(payload), separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, JOB_PATH)


def save_result(result):
    # Persist to SQLite as well as the job JSON. SQLite survives a Gunicorn
    # process restart, so the last completed full-market result is available
    # immediately after a Render wake-up instead of forcing a new 555-symbol scan.
    app._psx_save_persistent_result(result)
    payload = {"result": app._clean_for_json(result), "saved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    tmp = RESULT_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    os.replace(tmp, RESULT_PATH)


def main():
    job = read_job()
    job.update({"status": "running", "pid": os.getpid(), "started_epoch": job.get("started_epoch") or time.time(),
                "progress": {"done": 0, "total": 0, "symbol": ""}, "result": None, "error": None})
    write_job(job)

    def progress(done, total, symbol):
        current = read_job()
        current.update({"status": "running", "pid": os.getpid(), "progress": {"done": int(done), "total": int(total), "symbol": str(symbol or "")}})
        write_job(current)

    try:
        result = app.run_psx_divergence_scan(progress_cb=progress)
        save_result(result)
        current = read_job()
        current.update({"status": "done", "pid": os.getpid(), "progress": {"done": int(result.get("symbols_scanned", 0)),
                      "total": int(result.get("symbols_scanned", 0)), "symbol": ""}, "result": result, "error": None})
        write_job(current)
    except Exception as exc:
        current = read_job()
        current.update({"status": "error", "pid": os.getpid(), "error": str(exc), "result": None})
        write_job(current)
        raise


if __name__ == "__main__":
    main()
