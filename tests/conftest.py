import sys
from pathlib import Path

# Adiciona a raiz do repositório ao sys.path para permitir imports como:
# from function_app.main import ingest
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))