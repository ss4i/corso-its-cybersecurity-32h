---
title: "EXTRA — Strumenti Enterprise (DevSecOps)"
subtitle: "Corso ITS Cybersecurity — Modulo Avanzato"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# EXTRA — Strumenti Enterprise
## 4-5 ore — SAST, DAST, SCA, SIEM, CI/CD

## Obiettivi

- La famiglia dei tool *AST
- SAST con Bandit, Semgrep, SonarQube
- SCA con pip-audit, Snyk
- DAST con OWASP ZAP, Burp
- Secrets scanning, Container security
- SIEM basics
- CI/CD security pipeline completa
- Cosa proporre il primo giorno in azienda

## La famiglia *AST

| Acronimo | Significato | Quando |
|----------|-------------|--------|
| **SAST** | Static AST | Code-time |
| **SCA** | Software Composition Analysis | Build-time |
| **DAST** | Dynamic AST | Run-time |
| **IAST** | Interactive AST | Run-time interno |
| **RASP** | Runtime App Self-Protection | Run-time blocco |
| **CSPM** | Cloud Security Posture | Run-time cloud |

## Pipeline DevSecOps

```
[Idea]──[Design]──[Code]──[Build]──[Deploy]──[Run]──[Monitor]
                    ▲       ▲         ▲        ▲       ▲
                  SAST    SCA       DAST    IAST     SIEM
                Secrets  SBOM      ZAP      RASP    Splunk
                Linter   Image
```

> Maturo = security check **a ogni fase**.

## SAST — Bandit (Python)

```bash
pip install bandit
bandit -r my_project/
```

Output:
```
B608 hardcoded_sql_expressions Medium
  app.py:42  sql = f"SELECT * FROM u WHERE id={uid}"
```

~70 pattern Python. Falsi positivi normali.

## SAST — Semgrep (multi-lang)

```bash
semgrep --config "p/python"
semgrep --config "p/owasp-top-ten"
semgrep --config "p/r2c-security-audit"
```

Regole **leggibili**, custom facili.

## Semgrep — regola custom

```yaml
rules:
  - id: hardcoded-secret
    pattern-either:
      - pattern: SECRET_KEY = "..."
      - pattern: API_KEY = "..."
    message: "Secret hardcoded"
    languages: [python]
    severity: ERROR
```

## SAST — confronto

| Tool | Lang | Costo |
|------|------|-------|
| Bandit | Python | Free |
| Semgrep | 20+ | Free + paid |
| SonarQube | 30+ | Free + paid |
| Snyk Code | 10+ | Freemium |
| CodeQL | 8 | Free su pubblico |

## SCA — pip-audit

```bash
pip-audit -r requirements.txt
```

```
flask    2.0.0    GHSA-m2qf  → 2.2.5
pyyaml   5.1      GHSA-6757  → 5.4
```

## SCA — Dependabot

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
```

PR automatiche per CVE in dipendenze.

## SBOM — Software Bill of Materials

> Lista completa dipendenze (versioni, hash)

```bash
# CycloneDX
pip install cyclonedx-bom
cyclonedx-py -o sbom.json

# Syft (multi-lingua)
syft my_project/ -o cyclonedx-json
```

**Obbligatorio per CRA dal 2027.**

## DAST — OWASP ZAP

```bash
docker run owasp/zap2docker-stable \
  zap-baseline.py -t https://target.example.com \
  -r report.html
```

Standard gratuito DAST.

## Burp Suite

- **Community** (free): manuale
- **Pro** (~$450/anno): scanner attivo, intruder

Standard pentester.

## Secrets — gitleaks

```bash
gitleaks detect --source . --report-format json
```

Pre-commit hook:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    hooks: [{id: gitleaks}]
```

## Secrets — TruffleHog

```bash
trufflehog git https://github.com/repo --only-verified
```

`--only-verified`: chiama il provider per **confermare** secret valido. Riduce falsi positivi.

## Cosa fare se hai committato un secret

1. **Revoca subito** la credenziale (genera nuova)
2. Cancella dal repo (BFG Repo-Cleaner)
3. Force push
4. **NON pensare** "ho cancellato il commit, ok". Tutti i fork hanno ancora il secret.

## Container — Trivy

```bash
trivy image nginx:latest
trivy image my-app:v1.0
trivy fs ./project
```

CVE in OS packages, dipendenze, Dockerfile misconfiguration.

## Dockerfile linting — hadolint

```bash
hadolint Dockerfile
```

Trova: USER root, ADD invece di COPY, latest tag, apt-get senza pulizia.

## Kubernetes security

| Tool | Cosa fa |
|------|---------|
| kube-bench | CIS Kubernetes Benchmark |
| kube-hunter | Pentest cluster |
| Falco | Runtime security in container |
| Polaris | Best practice K8s YAML |
| OPA/Gatekeeper | Policy as code |

## IaC scanning — Checkov

```bash
pip install checkov
checkov -d terraform/
checkov -f docker-compose.yml
```

~1000+ misconfigurazioni cloud (S3 pubblici, security group aperti).

## SIEM — vendor

| Tool | Tipo |
|------|------|
| Splunk | Commerciale leader |
| IBM QRadar | Enterprise |
| Microsoft Sentinel | Cloud Azure |
| Google Chronicle | Cloud petabyte |
| Elastic (ELK) | Open source |
| Wazuh | OSS XDR |
| Graylog | OSS più semplice |

## SIEM — cosa loghi (dev view)

- Login OK/FAIL (IP, UA, MFA)
- Logout, password change
- Modifiche permessi/ruoli
- Accessi a risorse sensibili
- Errori 5xx con context
- Pattern 4xx (es. 100x 403 in 1 min)

> Formato: **JSON strutturato** (ECS, OpenTelemetry).

## SIEM — esempio log

```python
logger.info("login", extra={
    "event_type": "auth.login.success",
    "user_id": user.id,
    "ip": request.remote_addr,
    "user_agent": request.user_agent.string,
})
```

→ JSON → SIEM lo ingerisce e correla.

## SIEM — casi d'uso

- **Brute force**: 50 fail in 5 min stesso IP → alert
- **Anomaly**: Italia poi India in 5 min → alert
- **Lateral movement**: account su sistemi inusuali
- **Exfiltration**: download massivo file

## CI/CD pipeline tipica

```
Commit
  ↓
Pre-commit (gitleaks, ruff)
  ↓
CI: SAST + SCA + Secrets + Test + Coverage + Build + Image scan + SBOM
  ↓
Staging deploy + DAST
  ↓
Approval
  ↓
Production deploy + SIEM
```

## GitHub Actions — esempio

```yaml
- name: Bandit
  run: bandit -r . -ll
- name: pip-audit
  run: pip-audit --strict
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
- name: Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
```

## Quality gates

| Check | Bloccante? |
|-------|-----------|
| Test fail | Sì |
| Coverage <80% | Sì (policy) |
| SAST Critical | Sì |
| SAST Medium | No (issue) |
| SCA CVE Critical | Sì |
| Secrets trovati | Sì |
| Container Critical | Sì |
| DAST staging | No (alert) |

## Signed commits

```bash
gpg --gen-key
git config --global user.signingkey YOUR_KEY
git config --global commit.gpgsign true
```

Branch protection può richiedere "verified" commits.

## Branch protection rules

GitHub Settings → Branches:

- [ ] Require PR review (≥1)
- [ ] Require status checks (security CI)
- [ ] Require signed commits
- [ ] Restrict push a main
- [ ] Include administrators

> Senza queste regole, security CI è **opzionale** = inutile.

## Cosa proporre il primo giorno in azienda

Se entri in azienda e **non c'è nulla**, ordine:

1. **Pre-commit gitleaks** (5 min, zero costo)
2. **Dependabot** o pip-audit in CI (10 min)
3. **Bandit** in CI (10 min)
4. **Trivy** in CI (10 min)
5. **OWASP ZAP** baseline in staging (30 min)

In una settimana hai DevSecOps pipeline decente a costo zero.

## Lab — pipeline minimal

App vulnerabile + 3 tool:
- Bandit trova SQLi + hardcoded secret + debug
- pip-audit trova CVE in flask 2.0
- gitleaks trova AWS key pattern

Esercizio: correggi tutti, rilancia, zero issue.

> Codice in `02_lab/M_EXTRA_devsecops_lab/`

## Tabella riassuntiva tool

| Categoria | Free | Commerciale |
|-----------|------|-------------|
| SAST | Bandit, Semgrep | SonarQube, Snyk |
| SCA | pip-audit, Dependabot | Snyk, Mend |
| DAST | ZAP, Nikto | Burp Pro |
| Secrets | gitleaks | GitGuardian |
| Container | Trivy, Grype | Snyk Container, Aqua |
| IaC | Checkov, tfsec | Snyk IaC |
| SIEM | ELK, Wazuh | Splunk, QRadar |

## Tool da conoscere ma non userai

- Veracode, Checkmarx, Fortify (SAST enterprise pesanti)
- Splunk (tutti ne parlano, pochi lo configurano)
- Burp Pro (se diventi pentester)

> Sapere che esistono = abbastanza per il colloquio.

## Risorse

- OWASP DevSecOps Guideline
- CNCF Cloud Native Security Map
- NIST SSDF (Secure Software Development Framework)
- OWASP Vulnerable Dependency Cheat Sheet

## Domande?
