from function_app.main import ingest


def test_ingest_writes_raw(tmp_path, monkeypatch):
    monkeypatch.setattr("function_app.main.RAW_DIR", str(tmp_path / "raw"))
    monkeypatch.setattr("function_app.main.REJECT_DIR", str(tmp_path / "reject"))

    result = ingest({"fonte": "POC", "valor": 1})
    assert result["status"] == "raw"


def test_ingest_rejects_invalid(tmp_path, monkeypatch):
    monkeypatch.setattr("function_app.main.RAW_DIR", str(tmp_path / "raw"))
    monkeypatch.setattr("function_app.main.REJECT_DIR", str(tmp_path / "reject"))

    result = ingest({"fonte": "POC", "valor": "x"})
    assert result["status"] == "reject"
