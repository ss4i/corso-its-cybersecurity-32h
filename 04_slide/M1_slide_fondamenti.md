---
title: "M1 — Fondamenti di Cybersecurity"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M1 — Fondamenti
## 4 ore — 3h teoria + 1h lab

## Obiettivi

- Definire **CIA Triad** con esempi
- Distinguere sicurezza **informatica** vs **del software**
- Classificare le minacce in 8 categorie
- Conoscere i **5 principi del Secure Coding**
- Mentalità **avversaria**

## Sicurezza informatica vs del software

| | Cosa protegge | Da chi |
|---|---|---|
| **Informatica** | Rete, server, OS | Sistemisti |
| **Del software** | App, codice | Sviluppatori |

> Confonderle = errori sistematici
> "Abbiamo HTTPS, basta" → **falso**

## La CIA Triad

- **C** — Confidentiality (riservatezza)
- **I** — Integrity (integrità)
- **A** — Availability (disponibilità)

Sono **proprietà** del sistema, misurabili e violabili.

## Esempi CIA

| Caso | Proprietà violata |
|------|-------------------|
| Equifax 2017 (147M record) | C |
| Bonifico modificato in transito | I |
| WannaCry — ospedali bloccati | A |
| DDoS | A |
| SQL Injection che legge DB | C |

## I 3 fratelli (estensione)

- **Authenticity** — sei davvero tu?
- **Non-repudiation** — non puoi negare di aver fatto X
- **Accountability** — audit trail

CIA + AAA = framework completo.

## Tassonomia minacce — overview

1. Malware
2. Phishing / social engineering
3. Man-in-the-Middle
4. DoS / DDoS
5. Web application attacks
6. Supply chain
7. Zero-day
8. Insider threat

## Malware in dettaglio

- Virus, worm, trojan
- **Ransomware** (WannaCry, Colonial Pipeline)
- Spyware (Pegasus)
- Rootkit
- Botnet

> Difesa: antivirus + EDR + non eseguire allegati

## Phishing & social engineering

- Phishing standard
- **Spear phishing** (mirato)
- Whaling (al CEO)
- Vishing / smishing
- Pretexting, baiting

> Difesa: **MFA** + formazione utenti

## MITM, DoS, Web App

- **MITM**: ARP/DNS spoofing, Wi-Fi rogue
- **DoS/DDoS**: saturare risorse o banda
- **Web App**: OWASP Top 10 → cuore di M6

## Supply chain & zero-day

- **SolarWinds 2020** — 18.000 vittime
- **Log4Shell 2021** — Internet in panico
- **XZ Utils 2024** — backdoor sfiorata

Mercato zero-day: centinaia di migliaia di $ per exploit critici.

## Caso 1 — Equifax 2017

- 147M record rubati
- Causa: Apache Struts CVE-2017-5638 non patchata per 2 mesi
- Costo: ~$1,4 miliardi
- **Lezione**: patching tempestivo è sicurezza quotidiana

## Caso 2 — Heartbleed 2014

- Bug in OpenSSL
- Lettura di 64KB memoria server per richiesta
- ~17% dei server HTTPS al mondo
- **Lezione**: una libreria di tutti = SPOF colossale

## Caso 3 — Target 2013

- 40M numeri di carta rubati
- Punto d'ingresso: **un fornitore HVAC**
- **Lezione**: il tuo perimetro = perimetro fornitore più debole

## Caso 4 — SolarWinds 2020

- Build server compromesso
- 18.000 organizzazioni infettate
- **Lezione**: la firma digitale non basta se la pipeline è bucata

## Caso 5 — Log4Shell 2021

- CVE-2021-44228 in Log4j
- RCE con un campo User-Agent
- ~10% dei server enterprise
- **Lezione**: meno features = meno superficie di attacco

## Mentalità avversaria

> Non chiederti: "fa quello che deve fare?"
> Chiediti: "**cosa fa che non dovrebbe fare?**"

## Esempio — un form di login

```python
@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(
        username=request.form["username"]
    ).first()
    if user and user.password == request.form["password"]:
        ...
```

7 attacchi possibili in 2 minuti. Ne troverai quanti?

## I 5 Principi del Secure Coding

1. **Least Privilege** — solo ciò che serve
2. **Defense in Depth** — più strati indipendenti
3. **Fail Secure** — se si rompe, chiude
4. **KISS** — meno è più
5. **Separation of Duties** — mai uno solo

## Anti-pattern dei 5 principi

| Principio | Anti-pattern |
|-----------|--------------|
| Least Privilege | App che gira come root |
| Defense in Depth | "Abbiamo HTTPS, basta" |
| Fail Secure | `try/except` che ignora errori auth |
| KISS | Log4j → JNDI → RCE |
| Separation of Duties | Stesso utente DB dev e prod |

## Lab M1 — "Cosa è andato storto?"

A coppie, scegli **1 caso reale**:
- Riassunto in 3-4 righe
- CIA violata?
- Categoria minaccia?
- Principio Secure Coding ignorato?
- 1 misura tecnica concreta che avrebbe evitato

Discussione collettiva.

## Prossimo modulo

**M2 — Networking & ISO/OSI (6h)**

Adesso vediamo **come** un attaccante arriva fino al codice.
