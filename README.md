# POC Azure + VS Code + GitHub + CI/CD + Versionamento

Esta POC ("Proof of Concept") implementa um fluxo mínimo inspirado no seu diagrama.

- **GitHub (Repo)**: versionamento do código
- **CI** ("Continuous Integration"): lint + testes com **GitHub Actions**
- **CD** ("Continuous Deployment"): deploy automatizado para **Azure Functions**
- **Ingestão**: uma Function HTTP que gera um JSON e grava em `data/raw/` (simulando a camada **RAW** do "Data Lake")
- **Rejeições**: se falhar uma validação simples, grava em `data/reject/`

> Objetivo: praticar Azure + VS Code + GitHub + CI/CD + versionamento com o menor atrito.

---

## Rodar local (sem Azure)

### 1) Ambiente virtual

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 2) Instalar dependências

```bash
pip install -r requirements.txt
```

### 3) Executar ingestão (modo script)

```bash
python -m function_app.local_run
```

Saída esperada:
- JSON em `data/raw/ingest_YYYYMMDD_HHMMSS.json`
- Se inválido: JSON em `data/reject/reject_YYYYMMDD_HHMMSS.json`

---

## Subir para o GitHub

```bash
git init
git add .
git commit -m "POC inicial"

git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

---

## CI ("Continuous Integration")

Worklow: `.github/workflows/ci.yml`
- `ruff` (lint)
- `pytest` (testes)

---

## CD ("Continuous Deployment") para Azure Functions

Workflow: `.github/workflows/cd.yml`

### Secrets necessários (GitHub → Settings → Secrets and variables → Actions)

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_FUNCTIONAPP_NAME`

> Recomendado: OIDC ("OpenID Connect") com `azure/login@v2`.

