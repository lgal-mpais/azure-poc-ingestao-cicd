from datetime import datetime  # importa a classe datetime para gerar timestamps
from function_app.main import ingest  # importa a função ingest do módulo main

if __name__ == "__main__":  # garante que o código só rode quando o arquivo for executado diretamente
    payload = {  # define o dicionário de entrada para a função ingest
        "fonte": "POC",  # campo que identifica a origem do payload
        "valor": 123,  # campo de valor numérico de exemplo
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",  # timestamp UTC no formato ISO 8601
    }
    # chama ingest para validar e armazenar o payload em data/raw ou data/reject
    print(ingest(payload))  # imprime o resultado no console
