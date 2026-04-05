from datetime import datetime

from function_app.main import ingest


if __name__ == "__main__":
    payload = {
        "fonte": "POC",
        "valor": 123,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
    }
    print(ingest(payload))