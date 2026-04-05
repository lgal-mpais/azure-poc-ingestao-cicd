import json  # importa o módulo para serializar dicionários em JSON e gravar arquivos JSON
import os  # importa o módulo para manipular caminhos e criar diretórios
from datetime import datetime  # importa datetime para gerar timestamps em UTC

try:
    import azure.functions as func  # tenta importar a biblioteca de runtime do Azure Functions
except Exception:  # pragma: no cover
    func = None  # se não estiver disponível, mantém func como None para execução local

RAW_DIR = os.path.join("data", "raw")  # define o diretório de saída para ingestões válidas
REJECT_DIR = os.path.join("data", "reject")  # define o diretório de saída para rejeições inválidas


def _ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)  # cria data/raw se não existir
    os.makedirs(REJECT_DIR, exist_ok=True)  # cria data/reject se não existir


def _validate(payload: dict):
    if "fonte" not in payload:
        return False, "Campo 'fonte' ausente"  # valida presença do campo fonte
    if "valor" not in payload:
        return False, "Campo 'valor' ausente"  # valida presença do campo valor
    if not isinstance(payload["valor"], (int, float)):
        return False, "Campo 'valor' precisa ser numérico"  # valida tipo numérico do valor
    return True, "ok"  # payload válido, retorna sinalizador ok


def ingest(payload: dict) -> dict:
    _ensure_dirs()  # garante que os diretórios de saída existam antes de gravar arquivos
    ok, reason = _validate(payload)  # valida o payload e obtém motivo em caso de rejeição
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")  # cria timestamp para nome de arquivo exclusivo

    if ok:
        path = os.path.join(RAW_DIR, f"ingest_{ts}.json")  # define o caminho do arquivo RAW válido
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)  # escreve o payload validado em JSON
        return {"status": "raw", "path": path, "reason": reason}  # retorna metadados de sucesso

    path = os.path.join(REJECT_DIR, f"reject_{ts}.json")  # define o caminho do arquivo de rejeição
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"payload": payload, "error": reason}, f, ensure_ascii=False, indent=2)  # grava o payload rejeitado com motivo
    return {"status": "reject", "path": path, "reason": reason}  # retorna metadados de rejeição


def main(req):
    # Runtime Azure Functions
    if func is not None and isinstance(req, func.HttpRequest):  # valida se está sendo chamado pelo Azure Functions
        try:
            body = req.get_json()  # tenta extrair JSON do corpo da requisição HTTP
            payload = body if isinstance(body, dict) else {}  # usa o JSON se for um dicionário
        except Exception:
            payload = {}  # em caso de erro, usa payload vazio

        if not payload:
            payload = {"fonte": "POC", "valor": 123}  # fallback para payload padrão em chamadas Azure

        payload["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"  # adiciona timestamp UTC ao payload
        result = ingest(payload)  # executa a lógica de ingestão com validação e gravação

        return func.HttpResponse(
            body=json.dumps(result, ensure_ascii=False),  # converte o resultado para JSON na resposta HTTP
            status_code=200,  # código HTTP de sucesso
            mimetype="application/json",  # define o tipo de conteúdo como JSON
        )

    # Fallback local
    payload = {"fonte": "POC", "valor": 123, "timestamp_utc": datetime.utcnow().isoformat() + "Z"}  # payload padrão para execução local sem Azure
    return ingest(payload)  # retorna o resultado da ingestão no modo local
