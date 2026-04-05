from datetime import datetime, timezone

from function_app.main import ingest


if __name__ == "__main__":
    payload = {
        "fonte": "POC",
        "valor": 123,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(ingest(payload))