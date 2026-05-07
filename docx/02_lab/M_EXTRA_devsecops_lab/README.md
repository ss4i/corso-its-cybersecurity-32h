# Lab EXTRA — DevSecOps Pipeline Minimal

**Modulo**: EXTRA — Strumenti Enterprise
**Tempo stimato**: 2-3 ore
**Livello**: intermedio-avanzato

> Costruiamo una pipeline CI/CD con security gate. App Flask volutamente vulnerabile, 4 tool che la analizzano, GitHub Actions che blocca la merge se trova problemi.

---

## Obiettivi

1. Far girare **localmente** Bandit, pip-audit, gitleaks su un'app vulnerabile
2. Vedere ognuno dei tool produrre alert su problemi diversi
3. Scrivere un workflow GitHub Actions che applica gli stessi check in CI
4. Correggere l'app e vedere la pipeline diventare verde
5. Aggiungere Trivy per scan immagine Docker (bonus)

---

## File del lab

```
M_EXTRA_devsecops_lab/
├── README.md                  ← questo file
├── app.py                     ← app Flask volutamente vulnerabile
├── requirements.txt           ← dipendenze (alcune con CVE)
├── .github/
│   └── workflows/
│       └── security.yml       ← pipeline CI completa
├── Dockerfile                 ← per scan container (bonus)
└── solution/                  ← versione corretta (NON aprire prima!)
    ├── app.py
    └── requirements.txt
```

---

## Setup

### 1. Crea il progetto

```bash
mkdir devsec-lab && cd devsec-lab
git init
python -m venv .venv
source .venv/bin/activate    # o .venv\Scripts\Activate.ps1
```

### 2. Copia i file vulnerabili (fornito)

Vedi `app.py` e `requirements.txt` nello stesso lab.

### 3. Installa dipendenze + tool

```bash
pip install -r requirements.txt
pip install bandit pip-audit
```

### 4. Installa gitleaks

- macOS: `brew install gitleaks`
- Linux: `wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz`
- Windows: `choco install gitleaks` o scarica da releases

### 5. Installa Trivy (opzionale per Docker scan)

- macOS: `brew install trivy`
- Linux: `sudo apt install trivy`
- Windows: scarica da github.com/aquasecurity/trivy/releases

---

## Step 1 — App vulnerabile

`app.py`:

```python
import sqlite3
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"   # 🚩 AWS access key pattern hardcoded

@app.route("/login")
def login():
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    conn = sqlite3.connect("db.sqlite")
    sql = f"SELECT * FROM users WHERE user='{user}' AND pwd='{pwd}'"  # 🚩 SQLi
    return str(conn.execute(sql).fetchone())

@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd")
    import os
    return os.popen(cmd).read()   # 🚩 RCE catastrofica

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")   # 🚩 debug in prod, bind 0.0.0.0
```

`requirements.txt`:

```
flask==2.0.0      # CVE-2023-30861 (cookie sec issue)
requests==2.20.0  # CVE-2018-18074
pyyaml==5.1       # CVE-2020-1747
jinja2==2.11.0    # CVE-2020-28493
```

---

## Step 2 — Esegui i tool localmente

### 2.1 Bandit (SAST)

```bash
bandit app.py
```

Output atteso (estratto):
```
>> Issue: [B608] hardcoded_sql_expressions - SQL injection vector
   app.py:12
>> Issue: [B602] subprocess_popen_with_shell_equals_true - Possible shell injection
   app.py:17
>> Issue: [B201] flask_debug_true - DEBUG=True in Flask
   app.py:21
>> Issue: [B104] hardcoded_bind_all_interfaces - 0.0.0.0
   app.py:21
```

**Bandit trova 4 problemi**.

### 2.2 pip-audit (SCA)

```bash
pip-audit
```

Output atteso:
```
Found 4+ known vulnerabilities in 4+ packages
Name      Version  ID                  Fix Versions
flask     2.0.0    GHSA-...            2.2.5+
requests  2.20.0   GHSA-...            2.20.0+
pyyaml    5.1      GHSA-...            5.4
jinja2    2.11.0   GHSA-...            2.11.3+
```

**pip-audit trova le CVE in dipendenze**.

### 2.3 gitleaks (Secrets scanning)

```bash
git add app.py requirements.txt
git commit -m "first commit"
gitleaks detect --source . --no-git
```

Output atteso:
```
Finding:     SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"
RuleID:      aws-access-token
File:        app.py
Line:        4
```

**gitleaks identifica il pattern AWS key**.

### 2.4 Riassunto problemi trovati

| Tool | Problema |
|------|----------|
| Bandit | SQLi, RCE, debug=True, bind 0.0.0.0 |
| pip-audit | CVE in flask, requests, pyyaml, jinja2 |
| gitleaks | AWS key hardcoded |

**Totale: ~9 problemi** in un'app di 20 righe.

---

## Step 3 — Pipeline GitHub Actions

Crea `.github/workflows/security.yml`:

```yaml
name: Security CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # gitleaks ha bisogno della history

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install deps
        run: |
          pip install -r requirements.txt
          pip install bandit pip-audit

      # ============== SAST ==============
      - name: Bandit (SAST)
        run: |
          bandit -r . -ll -ii -f json -o bandit-report.json || true
          bandit -r . -ll -ii   # second run to fail
        continue-on-error: false

      # ============== SCA ==============
      - name: pip-audit (SCA)
        run: pip-audit --strict

      # ============== Secrets ==============
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # ============== Tests ==============
      - name: Tests
        run: |
          pip install pytest
          pytest --tb=short || true   # se hai test

      # ============== SBOM ==============
      - name: Generate SBOM
        run: |
          pip install cyclonedx-bom
          cyclonedx-py environment -o sbom.json
        continue-on-error: true

      - name: Upload SBOM
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json

      # ============== Container scan (bonus) ==============
      - name: Build Docker
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1
        continue-on-error: false
```

Push su GitHub → tab Actions → vedi il workflow girare.

**Il workflow fail su tutti i 9 problemi**.

---

## Step 4 — Correzione

### 4.1 Fix `app.py`

```python
import os
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)
SECRET_KEY = os.environ["SECRET_KEY"]   # ✅ env var

@app.route("/login")
def login():
    user = request.args.get("user", "")
    pwd = request.args.get("pwd", "")
    if not user or not pwd:
        abort(400)
    conn = sqlite3.connect("db.sqlite")
    # ✅ query parametrizzata
    cursor = conn.execute(
        "SELECT id FROM users WHERE user = ? AND pwd = ?",
        (user, pwd)
    )
    row = cursor.fetchone()
    return {"ok": row is not None}

# ✅ rimosso /run (RCE)

if __name__ == "__main__":
    # ✅ no debug, bind solo localhost
    app.run(host="127.0.0.1", port=5000, debug=False)
```

### 4.2 Fix `requirements.txt`

```
flask>=3.0.0
requests>=2.32.0
pyyaml>=6.0.1
jinja2>=3.1.4
```

### 4.3 Pre-commit hook locale (anti-recidiva)

Crea `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-ll", "-ii"]
```

Installa:
```bash
pip install pre-commit
pre-commit install
```

Da ora ogni `git commit` esegue automaticamente Bandit + gitleaks. Se trova problemi → commit bloccato.

---

## Step 5 — Verifica finale

Riesegui la pipeline:

```bash
bandit -r .         # → No issues identified
pip-audit           # → No known vulnerabilities found
gitleaks detect     # → leaks found: 0
```

E push su GitHub → workflow **verde**.

---

## Step 6 — Bonus: Container scan

`Dockerfile`:

```dockerfile
FROM python:3.12-slim

# ✅ user non-root
RUN useradd -m -u 1000 appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
```

Build + scan:

```bash
docker build -t myapp:latest .
trivy image myapp:latest
```

Trivy scansiona:
- Pacchetti del base image (Debian)
- Dipendenze Python
- Dockerfile misconfigurations

---

## Esercizi di approfondimento

### E1) Aggiungi Semgrep

```bash
pip install semgrep
semgrep --config "p/owasp-top-ten" .
```

Confronta cosa trova rispetto a Bandit. Quale è migliore per quale tipo?

### E2) Aggiungi DAST con OWASP ZAP

In CI, dopo deploy a staging:

```yaml
- name: ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.10.0
  with:
    target: "http://localhost:5000"
```

### E3) Hardcoded secrets in modi creativi

Prova a "nascondere" secret in modi non banali:
- Reverse string
- Base64-encoded
- Split su più righe

Vedi se gitleaks li trova. Aggiungi rule custom se manca.

### E4) Branch protection

In GitHub: Settings → Branches → main → "Require status checks before merging".
Seleziona il workflow Security.
Da ora **nessun PR può essere mergiato** se il workflow fallisce.

### E5) Dependabot

Crea `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
```

Pushalo. Dependabot apre PR automatiche per ogni dipendenza vulnerabile.

### E6) SAST + AI

Prova **Snyk Code** (gratuito tier) o **CodeQL**:

```yaml
- uses: github/codeql-action/init@v3
  with: { languages: python }
- uses: github/codeql-action/analyze@v3
```

Confronta findings con Bandit.

---

## Domande di verifica

1. Differenza SAST vs SCA vs DAST?
2. Perché gitleaks va eseguito **prima** del commit (pre-commit hook)?
3. Cosa significa "fail the build" in CI?
4. Perché Bandit ha falsi positivi più di pip-audit?
5. Cosa fa `--strict` in pip-audit?
6. Differenza tra Trivy e Snyk Container?
7. Cosa contiene un SBOM CycloneDX?
8. Quando si usa `continue-on-error: true` in GitHub Actions?

---

## Risorse

- OWASP DevSecOps Guideline: https://owasp.org/www-project-devsecops-guideline/
- Bandit docs: https://bandit.readthedocs.io
- pip-audit: https://pypi.org/project/pip-audit/
- gitleaks: https://github.com/gitleaks/gitleaks
- Trivy: https://trivy.dev
- GitHub Actions docs: https://docs.github.com/actions
