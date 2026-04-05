import json
import os
from datetime import datetime, timezone

import azure.functions as func

RAW_DIR = os.path.join("data", "raw")
REJECT_DIR = os.path.join("data", "reject")


def _ensure_dirs() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(REJECT_DIR, exist_ok=True)


def _validate(payload: dict) -> tuple[bool, str]:
    if "fonte" not in payload:
        return False, "Campo 'fonte' ausente"
    if "valor" not in payload:
        return False, "Campo 'valor' ausente"
    if not isinstance(payload["valor"], (int, float)):
        return False, "Campo 'valor' precisa ser numérico"
    return True, "ok"


def _ingest(payload: dict) -> dict:
    _ensure_dirs()
    ok, reason = _validate(payload)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    if ok:
        path = os.path.join(RAW_DIR, f"ingest_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return {"status": "raw", "path": path, "reason": reason}

    path = os.path.join(REJECT_DIR, f"reject_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"payload": payload, "error": reason}, f, ensure_ascii=False, indent=2)
    return {"status": "reject", "path": path, "reason": reason}


def main(req: func.HttpRequest) -> func.HttpResponse:
    # GET: usa default; POST: usa JSON do body
    payload = {}

    try:
        if req.method.upper() == "POST":
            body = req.get_json()
            payload = body if isinstance(body, dict) else {}
    except ValueError:
        payload = {}

    if not payload:
        payload = {"fonte": "POC", "valor": 123}

    payload["timestamp_utc"] = datetime.now(timezone.utc).isoformat()

    result = _ingest(payload)

    return func.HttpResponse(
        body=json.dumps(result, ensure_ascii=False),
        status_code=200,
        mimetype="application/json",
    )