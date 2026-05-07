# EXTRA — Strumenti Enterprise (SAST, DAST, SCA, SIEM, CI/CD security)

**Materiale integrativo — Corso ITS Cybersecurity**
**Tipologia**: estensione di M6 + introduzione a DevSecOps
**Tempo suggerito**: 4-5 ore (lettura + lab pratico)
**Prerequisiti**: M6 (vulnerabilità web), conoscenza base di Git/CI

> Materiale per chi entra in azienda e troverà tool che il corso base **non ha visto**. Standard moderno: ogni grande azienda ha pipeline CI/CD con security gate. Sapere cosa fanno questi tool = esser produttivi dal giorno 1.

---

## Indice

- [1. La famiglia dei tool — *AST](#cap1)
- [2. SAST — Static Application Security Testing](#cap2)
- [3. SCA — Software Composition Analysis](#cap3)
- [4. DAST — Dynamic Application Security Testing](#cap4)
- [5. IAST — Interactive AST](#cap5)
- [6. Secrets scanning](#cap6)
- [7. Container & Infrastructure security](#cap7)
- [8. SIEM — Security Information and Event Management](#cap8)
- [9. CI/CD Security Pipeline](#cap9)
- [10. Lab pratico — pipeline minimal con bandit + gitleaks + trivy](#cap10)
- [11. Tabella riassuntiva tool](#cap11)

---

<a name="cap1"></a>
## 1. La famiglia dei tool — *AST

| Acronimo | Cosa significa | Quando agisce | Esempio tool |
|----------|----------------|---------------|--------------|
| **SAST** | Static App Security Testing | A code-time | Bandit, Semgrep, SonarQube |
| **SCA** | Software Composition Analysis | A build-time | pip-audit, Snyk, Dependabot |
| **DAST** | Dynamic App Security Testing | A run-time | OWASP ZAP, Burp |
| **IAST** | Interactive AST | A run-time, dentro l'app | Contrast Security |
| **RASP** | Runtime App Self-Protection | A run-time, blocca attacchi | Imperva RASP |
| **CSPM** | Cloud Security Posture Management | A run-time | Wiz, Prisma |
| **SBOM** | Software Bill of Materials | A build-time | Syft, CycloneDX |

### 1.1 Mappa nel ciclo SDLC

```
[Idea]──[Design]──[Code]──[Build]──[Deploy]──[Run]──[Monitor]
                    ▲       ▲         ▲        ▲       ▲
                  SAST    SCA       DAST    IAST     SIEM
                Secrets  SBOM      ZAP      RASP    Splunk
                Linter   Image                       Wazuh
                         scan                         ELK
```

> Pipeline matura = security check **a ogni fase**.

---

<a name="cap2"></a>
## 2. SAST — Static Application Security Testing

### 2.1 Cos'è

Analisi del **codice sorgente** senza eseguirlo. Cerca pattern di vulnerabilità (SQLi, XSS, segreti hardcoded, ecc.).

### 2.2 Bandit (Python)

Tool gratuito, ufficiale Python.

```bash
pip install bandit
bandit -r my_project/
```

Output esempio:
```
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Low
   Location: app.py:42
41    user_id = request.args.get("id")
42    sql = f"SELECT * FROM users WHERE id = {user_id}"
43    cursor.execute(sql)
```

Bandit conosce ~70 pattern Python. Falsi positivi normali — vanno triagiati.

#### Configurazione `.bandit`:

```yaml
# .bandit
skips: ["B101"]   # ignora "assert used" nei test
exclude_dirs: ["tests", ".venv"]
```

### 2.3 Semgrep — il moderno

Open source, multi-linguaggio, **regole leggibili**.

```bash
pip install semgrep
semgrep --config "p/python" my_project/
semgrep --config "p/owasp-top-ten" my_project/
semgrep --config "p/r2c-security-audit" my_project/
```

Regola custom esempio (`semgrep_rules.yml`):

```yaml
rules:
  - id: hardcoded-secret
    pattern-either:
      - pattern: SECRET_KEY = "..."
      - pattern: API_KEY = "..."
    message: "Possibile secret hardcoded"
    languages: [python]
    severity: ERROR
```

Eseguire:
```bash
semgrep --config semgrep_rules.yml .
```

### 2.4 SonarQube — l'enterprise

Server centralizzato che analizza tutti i progetti dell'azienda. Dashboard, trend, integrazione PR.

- **Community Edition** (free): SAST base, code quality.
- **Developer/Enterprise**: SAST avanzato, branch analysis, multi-linguaggio (Java, C#, JS, Python, Go, Rust...).

Pattern aziendale: pipeline GitLab/GitHub Actions chiama SonarQube → fail PR se "quality gate" non passato.

### 2.5 Snyk Code

Servizio cloud (freemium). SAST con AI. Buona integrazione IDE (VS Code plugin).

### 2.6 Confronto SAST tool

| Tool | Linguaggi | Costo | Quando usare |
|------|-----------|-------|--------------|
| Bandit | Python | Free | Progetti Python piccoli/medi |
| Semgrep | 20+ | Free + paid | Progetti multi-linguaggio, regole custom |
| SonarQube | 30+ | Free + paid | Aziende strutturate, policy centralizzata |
| Snyk Code | 10+ | Freemium | Quick start, integrazione IDE |
| CodeQL (GitHub) | 8 | Free su pubblico | Progetti GitHub, query custom |

### 2.7 Limiti SAST

- ❌ Falsi positivi (alti su Java/JS, meno su Python)
- ❌ Non vede vulnerabilità run-time
- ❌ Non vede misconfigurazioni
- ❌ Non vede vulnerabilità di dipendenze (serve SCA)

---

<a name="cap3"></a>
## 3. SCA — Software Composition Analysis

### 3.1 Cos'è

Analizza le **dipendenze** del progetto e trova CVE note nelle versioni usate.

### 3.2 pip-audit (già visto in M6.6)

```bash
pip install pip-audit
pip-audit
```

### 3.3 Snyk Open Source

Versione cloud più ricca. Trovaa CVE + suggerisce fix automatici via PR.

```bash
npm install -g snyk
snyk auth
snyk test
snyk monitor    # invia stato per monitoring continuo
```

### 3.4 Dependabot (GitHub)

Built-in di GitHub. Apre PR automatiche per aggiornare dipendenze vulnerabili.

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
    open-pull-requests-limit: 5
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: { interval: "weekly" }
```

### 3.5 Renovate — il concorrente open-source

Più configurabile di Dependabot. Standard in alcune aziende.

### 3.6 OWASP Dependency-Check

Tool gratuito, analizza dipendenze Java/Maven/Gradle (e altre con plugin).

```bash
dependency-check --project myapp --scan ./pom.xml --format HTML
```

### 3.7 SBOM — Software Bill of Materials

> Lista completa di tutto ciò che il tuo software include (librerie, versioni, hash).

Formati standard:
- **CycloneDX** (OWASP, JSON/XML)
- **SPDX** (Linux Foundation, JSON/RDF)

Tool generazione:

```bash
# CycloneDX per Python
pip install cyclonedx-bom
cyclonedx-py -o sbom.json

# Syft (multi-lingua, multi-formato)
syft my_project/ -o cyclonedx-json > sbom.json
syft docker:nginx:latest -o spdx-json > nginx-sbom.json
```

> **CRA dal 2027 lo richiederà obbligatorio** per prodotti UE.

---

<a name="cap4"></a>
## 4. DAST — Dynamic Application Security Testing

### 4.1 Cos'è

Test attivi sull'app **in esecuzione**. Non legge il codice, **bombarda** l'app con payload e osserva risposte.

### 4.2 OWASP ZAP — Open Source

Tool gratuito, GUI + CLI. Standard de facto per DAST gratuito.

#### Modalità

- **Manuale**: proxy il traffico, esplora a mano.
- **Automated Scan**: dato un URL, scansiona automaticamente.
- **API Scan**: con OpenAPI spec, testa tutti gli endpoint.

#### Esempio CLI

```bash
docker run -t owasp/zap2docker-stable \
  zap-baseline.py -t https://target.example.com \
  -r report.html
```

Report HTML con vulnerabilità trovate.

### 4.3 Burp Suite

- **Community Edition**: free, manuale.
- **Professional**: ~$450/anno, scanner attivo, intruder, repeater avanzato.

Standard per pentester. Più potente di ZAP a livello tool, ma costa.

### 4.4 Nikto

Veloce, focus su misconfigurazioni server web.

```bash
nikto -h https://target.example.com
```

### 4.5 sqlmap

Specifico per SQL Injection.

```bash
sqlmap -u "https://target.com/page?id=1" --batch
sqlmap -u "https://target.com/page?id=1" --dbs    # enumera DB
```

⚠️ **Solo su target autorizzati**.

### 4.6 Limiti DAST

- ❌ Non trova vulnerabilità "deep" (es. logica business)
- ❌ Lento (può richiedere ore)
- ❌ Falsi positivi
- ❌ Coverage parziale (non tutti gli endpoint testati)

---

<a name="cap5"></a>
## 5. IAST — Interactive AST

### 5.1 Cos'è

Agente **dentro l'app** durante run-time (testing). Ibrido: vede sia il codice (come SAST) sia le richieste (come DAST).

### 5.2 Vantaggi

- Pochi falsi positivi (sa cosa è davvero exploitable)
- Coverage code-level
- Funziona durante test funzionali esistenti

### 5.3 Tool

- **Contrast Security** (commerciale, leader)
- **Seeker** (Synopsys)
- **Bright Security**

### 5.4 Quando vale

In aziende con QA testing già strutturato. Aggiungi un agente all'app di test, fai i tuoi test funzionali, l'agente registra vulnerabilità trovate.

---

<a name="cap6"></a>
## 6. Secrets scanning

### 6.1 Il problema

Sviluppatori committano per sbaglio:
- API key (AWS, Stripe, GitHub token)
- Password DB
- Chiavi private SSH
- Token JWT

In repo Git → **leak permanente** (anche se cancelli, resta nella history).

### 6.2 Tool

#### gitleaks

```bash
gitleaks detect --source . --report-format json
```

Scansiona repo Git per ~150 pattern di segreti.

Pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

#### TruffleHog

```bash
trufflehog git https://github.com/myorg/myrepo.git --only-verified
```

`--only-verified` filtra **solo** segreti che TruffleHog ha **verificato come validi** (chiamando il servizio). Riduce falsi positivi.

#### GitHub native — Secret Scanning

GitHub scansiona **automaticamente** i repo (anche privati su account paid) per pattern di secrets di provider partner (AWS, Stripe, Slack, ecc.).

Quando trova: notifica + revoca automatica con il provider.

### 6.3 Cosa fare se hai committato un secret

1. **Revoca subito** la credenziale (genera nuova).
2. Cancella dal repo (`git filter-branch` o BFG Repo-Cleaner).
3. Force push (warning: rompe collaboratori).
4. **NON pensare** "ho cancellato il commit, è risolto". Tutti i fork/clone hanno ancora il secret.

### 6.4 Come prevenire

- Pre-commit hook con gitleaks
- `.gitignore` aggressivo (`.env`, `*.pem`, `secrets/`)
- Secrets management (Vault, AWS Secrets Manager, Doppler)
- Review attenta dei PR

---

<a name="cap7"></a>
## 7. Container & Infrastructure security

### 7.1 Container scanning

#### Trivy (Aqua Security) — gratuito, eccellente

```bash
trivy image nginx:latest
trivy image my-registry/myapp:v1.0
trivy fs ./my_project    # scansiona filesystem
```

Trovaa CVE in:
- Pacchetti OS (debian, alpine, ubuntu)
- Dipendenze applicative (pip, npm, gem)
- Misconfigurazioni Dockerfile

#### Snyk Container

Equivalente commerciale, più features (priorità basata su EPSS, ecc.).

#### Grype (Anchore)

Veloce, formato output strutturato. Spesso usato in CI.

### 7.2 Dockerfile linting

#### hadolint

```bash
hadolint Dockerfile
```

Trova:
- `USER root` non necessario
- `ADD` invece di `COPY`
- Latest tag
- Comandi `apt-get install` senza pulizia

### 7.3 Kubernetes security

- **kube-bench** — verifica conformità a CIS Kubernetes Benchmark
- **kube-hunter** — pentest del cluster
- **Falco** — runtime security (rilevamento intrusioni in container)
- **Polaris** — best practice K8s yaml
- **OPA/Gatekeeper** — policy as code

### 7.4 IaC scanning (Infrastructure as Code)

#### Checkov

```bash
pip install checkov
checkov -d terraform/
checkov -f docker-compose.yml
```

Scansiona Terraform, CloudFormation, K8s YAML, Dockerfile, Helm. Trova ~1000+ misconfigurazioni cloud (S3 pubblici, security group aperti, ecc.).

#### tfsec, kics

Alternative valide, focus IaC.

---

<a name="cap8"></a>
## 8. SIEM — Security Information and Event Management

### 8.1 Cos'è

Sistema centralizzato che:
- **Raccoglie** log da decine di fonti (server, app, firewall, EDR, cloud)
- **Normalizza** in un formato comune
- **Cerca pattern** di attacco
- **Allertaa** il SOC

### 8.2 Vendor principali

| Tool | Tipo | Note |
|------|------|------|
| **Splunk** | Commerciale, leader | Costoso, potente |
| **IBM QRadar** | Commerciale | Enterprise, comune in banche |
| **Microsoft Sentinel** | Cloud (Azure) | SIEM-as-a-service |
| **Google Chronicle** | Cloud | Petabyte scale |
| **Elastic Stack (ELK)** | Open source | Self-hosted, configurazione lunga |
| **Wazuh** | Open source | XDR + SIEM |
| **Graylog** | Open source | Più semplice di ELK |

### 8.3 Cosa logghi nel SIEM (dal punto di vista app developer)

Il developer **non** gestisce il SIEM, ma deve **inviare i log giusti**:

- Login (ok / fail) con IP, user-agent, timestamp
- Logout
- Cambi password
- Modifiche permessi/ruoli
- Accessi a risorse sensibili (vista profilo, vista fattura, export dati)
- Errori 5xx (con context)
- Tentativi 4xx pattern (es. 100x 403 in 1 min = brute force authz)

**Formato consigliato**: JSON strutturato (Elastic Common Schema, OpenTelemetry).

### 8.4 Esempio log strutturato

```python
import logging
import json
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("security")
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)

# Uso
logger.info("login", extra={
    "event_type": "auth.login.success",
    "user_id": user.id,
    "ip": request.remote_addr,
    "user_agent": request.user_agent.string,
})
```

Output:
```json
{"event_type":"auth.login.success","user_id":12,"ip":"1.2.3.4",...}
```

Il SIEM lo ingerisce e correla con altri log.

### 8.5 Casi d'uso SIEM tipici

- **Brute force detection**: 50 login failed dallo stesso IP in 5 min → alert
- **Anomaly detection**: utente che si logga da Italia poi 5 min dopo da India → alert
- **Lateral movement**: account che accede a sistemi inusuali → alert
- **Data exfiltration**: download massivo di file → alert

### 8.6 SOC vs SOAR

- **SOC** (Security Operations Center): team umano che monitora il SIEM 24/7.
- **SOAR** (Security Orchestration, Automation, Response): automazione delle risposte (es. blocca IP automaticamente, isola host).

---

<a name="cap9"></a>
## 9. CI/CD Security Pipeline

### 9.1 Architettura tipica

```
Developer commit
   ↓
Pre-commit hooks (locali)
   - secrets scanning (gitleaks)
   - linting (ruff, eslint)
   ↓
Push a GitHub/GitLab
   ↓
CI Pipeline (GitHub Actions / GitLab CI)
   - SAST (Bandit, Semgrep)        ← FAIL su Critical
   - SCA (pip-audit, Snyk)         ← FAIL su High+
   - Secret scanning (gitleaks)    ← FAIL se trova
   - Test unitari + coverage
   - Build immagine Docker
   - Image scan (Trivy)            ← FAIL su Critical
   - SBOM generation
   ↓
Deploy a staging
   - DAST (ZAP baseline scan)      ← REPORT (non fail)
   - Smoke test
   ↓
Approval manuale (per prod)
   ↓
Deploy produzione
   - Monitoring (SIEM ingest)
```

### 9.2 Esempio GitHub Actions completo

```yaml
# .github/workflows/security.yml
name: Security CI

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # serve a gitleaks per analisi history

      - name: Setup Python
        uses: actions/setup-python@v5
        with: { python-version: "3.12" }

      - name: Install
        run: |
          pip install -r requirements.txt
          pip install bandit pip-audit semgrep

      # SAST
      - name: Bandit
        run: bandit -r . -ll -ii    # -ll = solo Medium+, -ii = High confidence
        # In CI strict: || exit 1

      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: "p/owasp-top-ten p/python"

      # SCA
      - name: pip-audit
        run: pip-audit -r requirements.txt --strict

      # Secrets
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Test + coverage
      - name: Tests
        run: pytest --cov=. --cov-fail-under=80

      # SBOM
      - name: Generate SBOM
        run: |
          pip install cyclonedx-bom
          cyclonedx-py -o sbom.json
      - uses: actions/upload-artifact@v4
        with: { name: sbom, path: sbom.json }

      # Container
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1
```

### 9.3 Quality gates

Concetto chiave: alcune check **bloccano** il merge/deploy. Altre **alertano** ma non bloccano.

| Check | Bloccante? |
|-------|-----------|
| Test fail | Sì |
| Coverage <80% | Sì (se policy aziendale) |
| SAST: Critical/High | Sì |
| SAST: Medium/Low | No (issue creata) |
| SCA: CVE Critical | Sì |
| SCA: CVE High | Sì + Dependabot PR |
| Secrets trovati | Sì |
| Image scan: Critical | Sì |
| DAST: vulnerabilità | No (in staging — alert) |

### 9.4 Signed commits

```bash
# Genera chiave GPG
gpg --gen-key

# Configura Git per firmare
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Aggiungi chiave pubblica a GitHub: Settings → SSH and GPG keys
```

In repo: `git log --show-signature` mostra firme. Branch protection può richiedere "verified" commits.

### 9.5 Branch protection rules

GitHub Settings → Branches → Add rule:

- Require pull request reviews (≥1 approver)
- Require status checks to pass (security CI)
- Require signed commits
- Restrict who can push to main
- Include administrators

> Senza queste regole, security CI è **opzionale** = inutile.

---

<a name="cap10"></a>
## 10. Lab pratico — pipeline minimal con bandit + gitleaks + trivy

### 10.1 Setup repo

```bash
mkdir secure-pipeline-demo && cd secure-pipeline-demo
git init
python -m venv .venv
source .venv/bin/activate    # o .\.venv\Scripts\Activate.ps1
```

### 10.2 App vulnerabile di esempio

```python
# app.py
import sqlite3
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "AKIA1234567890ABCDEF"   # 🚩 segreto hardcoded (per il lab)

@app.route("/login")
def login():
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    conn = sqlite3.connect("db.sqlite")
    sql = f"SELECT * FROM users WHERE user='{user}' AND pwd='{pwd}'"  # 🚩 SQLi
    return str(conn.execute(sql).fetchone())

if __name__ == "__main__":
    app.run(debug=True)   # 🚩 debug in prod
```

```
# requirements.txt
flask==2.0.0    # 🚩 versione vulnerabile
```

### 10.3 Lancio dei tool localmente

```bash
pip install bandit pip-audit
pip install -r requirements.txt

# 1. SAST
bandit app.py
# Output: hardcoded SECRET_KEY, SQL injection, debug=True

# 2. SCA
pip-audit
# Output: flask 2.0.0 ha CVE-XXX

# 3. Secrets scan
# (richiede gitleaks installato — vedi gitleaks.io)
git add app.py requirements.txt && git commit -m "first commit"
gitleaks detect --source . --no-git
# Output: AKIA... (AWS key pattern)
```

### 10.4 Pipeline GitHub Actions

```yaml
# .github/workflows/sec.yml
name: Sec
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt bandit pip-audit
      - name: Bandit
        run: bandit -r . -lll
      - name: pip-audit
        run: pip-audit
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

Push a GitHub → workflow gira → vedi le 3 vulnerabilità.

### 10.5 Esercizio: correggi e riesegui

1. Sposta `SECRET_KEY` in env var (`os.getenv("SECRET_KEY")`).
2. Riscrivi la query con parametrizzazione.
3. Rimuovi `debug=True`.
4. Aggiorna Flask a versione patchata.
5. Riesegui i 3 tool: zero issue.

---

<a name="cap11"></a>
## 11. Tabella riassuntiva tool

### 11.1 Per categoria

| Categoria | Tool free | Tool commerciale |
|-----------|-----------|--------------------|
| **SAST Python** | Bandit, Semgrep | SonarQube, Snyk Code |
| **SAST multi-lang** | Semgrep, CodeQL | SonarQube, Veracode, Checkmarx |
| **SCA Python** | pip-audit, OWASP DC | Snyk, Mend, JFrog Xray |
| **DAST** | OWASP ZAP, Nikto | Burp Pro, Acunetix |
| **Secrets** | gitleaks, TruffleHog | GitGuardian |
| **Container** | Trivy, Grype, Clair | Snyk Container, Aqua, Prisma |
| **IaC** | Checkov, tfsec, kics | Snyk IaC, Bridgecrew |
| **K8s runtime** | Falco, kube-bench | Aqua, Wiz |
| **SBOM** | Syft, CycloneDX, SPDX | (commercial wrappers) |
| **SIEM** | Elastic, Wazuh | Splunk, QRadar, Sentinel |

### 11.2 Cosa proporre alla prima azienda

Se entri in azienda e **non c'è nulla**, proponi questi 5 in ordine:

1. **Pre-commit hook gitleaks** (5 minuti, zero costo).
2. **Dependabot** o `pip-audit` in CI (10 minuti, zero costo).
3. **Bandit** in CI (10 minuti, zero costo).
4. **Trivy** in CI (10 minuti, zero costo).
5. **OWASP ZAP baseline scan** in staging (30 minuti, zero costo).

In una settimana hai una pipeline DevSecOps **decente** a costo zero.

### 11.3 Tool da conoscere ma probabilmente non userai

- **Veracode**, **Checkmarx**, **Fortify**: SAST enterprise pesanti.
- **Splunk**: tutti ne parlano, pochi lo configurano.
- **Burp Pro**: lo usi se diventi pentester, no se sei dev.

> Sapere che **esistono** + a cosa servono è abbastanza per il colloquio.

---

## Per approfondire

- **OWASP DevSecOps Guideline**: https://owasp.org/www-project-devsecops-guideline/
- **CNCF Cloud Native Security Map**: https://github.com/cncf/tag-security
- **NIST Secure Software Development Framework (SSDF)**: https://csrc.nist.gov/Projects/ssdf
- **OWASP Cheat Sheet — Vulnerable Dependency Management**: https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html

---

> **Suggerimento di integrazione**:
> - Lettura assegnata "primo giorno in azienda"
> - Lab di 2-3h dopo M6 con Bandit/pip-audit/gitleaks già visti
> - Capitolo principale per un eventuale "Modulo DevSecOps" di II anno
