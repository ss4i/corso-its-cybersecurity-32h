---
title: "M5 — Security & Privacy by Design"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M5 — Security & Privacy by Design
## 3 ore — 2h teoria + 1h workshop

## Obiettivi

- Security by Design (perché)
- **STRIDE** per threat modeling
- Data Flow Diagram + trust boundary
- 7 principi di **Cavoukian** (Privacy by Design)
- Pseudonimizzazione vs Anonimizzazione
- DPIA in pillole
- Workshop su BancaPiccola

## Il problema

Due modi di costruire un'app:

**A**: requisiti → design → codice → test → spedisco → aggiungo sicurezza dopo
**B**: requisiti **+ sicurezza** → threat modeling → codice sicuro → test sec → spedisco

## Costo del fix

| Quando si trova | Costo |
|-----------------|-------|
| Design | 1× |
| Coding | 5× |
| Testing/QA | 10× |
| Produzione | **100×** |

> "Costo" = soldi + tempo + reputazione

## Shift Left

```
[Idea]──[Design]──[Code]──[Test]──[Deploy]──[Run]
   ↑       ↑
   └───────┴── shift left
```

Threat modeling, linter, static analysis, dependency scanning **a sinistra**.

## Caso Equifax 2017 (ricapitolazione)

- Patch disponibile da 2 mesi → non installata
- 147M record rubati → $1,4B di costo
- **Decisioni a "design time"** mancate:
  - Inventario dipendenze
  - Patching SLA
  - Network segmentation

## Le 4 domande di Shostack

1. **Cosa stiamo costruendo?** (DFD)
2. **Cosa può andare storto?** (STRIDE)
3. **Cosa facciamo a riguardo?**
4. **Abbiamo fatto un buon lavoro?**

## STRIDE — l'acronimo

| Lettera | Categoria | Proprietà violata |
|---------|-----------|-------------------|
| **S** | Spoofing | Authenticity |
| **T** | Tampering | Integrity |
| **R** | Repudiation | Non-repudiation |
| **I** | Info Disclosure | Confidentiality |
| **D** | DoS | Availability |
| **E** | Elevation of Priv. | Authorization |

## S — Spoofing

- Login con password rubata
- Phishing con dominio simile
- DNS spoofing
- Certificato contraffatto

> Difese: MFA, mutual TLS, DNSSEC

## T — Tampering

- Modifica cookie
- Modifica importo POST
- Supply chain (codice modificato)
- Modifica file su disco

> Difese: HMAC, integrity check, validation server-side

## R — Repudiation

- "Non ho fatto io quel bonifico"
- "Non ho cancellato io"
- Modifica log per nascondere tracce

> Difese: audit log immutabile, firme digitali

## I — Information Disclosure

- SQL Injection esfiltrazione
- Stack trace su errore
- Endpoint API con campi sensibili
- Backup esposto pubblicamente

> Difese: TLS, error handling generico, least privilege dati

## D — DoS

- DDoS volumetrico
- Slowloris
- Algoritmo O(n²) su input grande
- Fill filesystem

> Difese: rate limit, WAF, timeout, quote

## E — Elevation of Privilege

- IDOR (utente normale → admin)
- Bypass authz
- SQLi → privilege escalation
- Vuln nel kernel

> Difese: least privilege, authz su ogni endpoint

## STRIDE per elemento (DFD)

| Elemento | S | T | R | I | D | E |
|----------|---|---|---|---|---|---|
| Entità esterna | ✅ | | ✅ | | | |
| Processo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Datastore | | ✅ | | ✅ | ✅ | |
| Flusso | | ✅ | | ✅ | ✅ | |

## Data Flow Diagram — i 4 simboli

| Simbolo | Cosa rappresenta |
|---------|------------------|
| □ Rettangolo | Entità esterna |
| ○ Cerchio | Processo |
| ═ Doppia linea | Datastore |
| → Freccia | Flusso |

## Trust Boundary

> Linea immaginaria che separa zone con livelli di fiducia diversi

Esempi:
- Internet ↔ tuo server
- Webapp ↔ DB
- Browser ↔ JavaScript (untrusted!)
- Container ↔ host

> Ogni boundary attraversato = opportunità di attacco.

## DFD esempio — login

```
[Utente] ──HTTP──► [Login] ──SQL──► [DB users]
                      │
══ Boundary: Internet ══
                      │
                      ▼
                 [Auth check] ──► [DB sessions]
                                  ══ Boundary: server↔DB ══
```

## Privacy by Design — Ann Cavoukian (2009)

7 principi → recepiti da GDPR Art. 25.

1. Proactive not Reactive
2. Privacy as Default
3. Embedded into Design
4. Full Functionality (no zero-sum)
5. End-to-End Security
6. Visibility / Transparency
7. User-Centric

## I 7 principi spiegati (1-3)

1. **Anticipare** problemi privacy invece di reagire
2. Default **più protettivi** (utente non fa nulla → protetto al massimo)
3. Privacy **dentro** l'architettura (non aggiunta dopo)

## I 7 principi (4-7)

4. **Non zero-sum**: privacy + funzionalità insieme
5. **Tutto il ciclo**: raccolta → uso → archivio → cancellazione
6. **Trasparenza**: utente capisce cosa fai con i suoi dati
7. **User-centric**: dati dell'utente, controllo dell'utente

## Data Minimization

GDPR Art. 5(1)(c): solo i dati **necessari**.

Form maximalist (sbagliato):
- Nome, cognome, email, telefono, indirizzo, data di nascita, sesso, professione, reddito...

Form minimalist (giusto):
- Email
- (opzionale) Nome

## Domande a design time

Per ogni campo:
1. Mi serve davvero?
2. Mi serve in chiaro o basta hash?
3. Mi serve per quanto tempo?
4. A chi serve?

## Tecniche di minimizzazione

- Email → hash dell'email
- Data di nascita → fascia d'età
- Indirizzo → CAP
- Foto → embedding ML

## Pseudonimizzazione

- Identità sostituita da pseudonimo
- **Mappa di reidentificazione** separata
- **Reversibile**
- ⚠️ **GDPR si applica ancora**

Esempio: tabella ordini con `user_id=7438`, mappa `(user_id, email)` separata.

## Anonimizzazione

- **Irreversibile** anche con dati esterni
- ✅ GDPR **non** si applica
- 🔥 Molto più difficile di quanto sembri

## La trappola "credo di aver anonimizzato"

- **Netflix Prize 2006**: dataset "anonimizzato" reidentificato incrociando con IMDb
- `hash(email)` **non** è anonimizzazione (dizionario)
- k-anonymity: ogni individuo simile ad almeno k-1 altri

## Pseudo vs Anon

| | Pseudo | Anon |
|---|--------|------|
| Reversibile? | Sì | No |
| GDPR? | Sì | No |
| Difficoltà | Bassa | Alta |
| Casi tipici | Riduzione rischio | Pubblicazione stat |

> Nel 90% dei casi quello che ti serve è **pseudo**.

## DPIA — quando è obbligatoria

GDPR Art. 35:
- Profilazione automatizzata con effetti giuridici
- Categorie particolari su **larga scala**
- Sorveglianza sistematica spazi pubblici
- Lista nera del Garante (es. riconoscimento facciale)

> In dubbio? Falla.

## DPIA — template minimo

1. Descrizione trattamento
2. Necessità e proporzionalità
3. Rischi per gli interessati (probabilità × impatto)
4. Misure di sicurezza
5. Conclusione + firma DPO

## Workshop — STRIDE su BancaPiccola

A gruppi di 3, su BancaPiccola:

1. Disegnate DFD (15 min)
2. Almeno 15 minacce STRIDE (25 min)
3. Top 3 per rischio (5 min)
4. Discussione collettiva (15 min)

## Esempio minacce attese

| Elemento | STRIDE | Difesa |
|----------|--------|--------|
| Login | S | MFA |
| Login | E | SQLi → query parametrizzata |
| Lista fatture | E | IDOR → ownership check |
| DB | I | Backup non cifrato → cifrare |
| Flusso | I | Sniffing → TLS |

## Verifica intermedia V2

> Alla fine di M5 — 50 minuti, 100 punti
> Copre M4 + M5

Cosa entra:
- GDPR articoli, NIS 2 obblighi, CRA
- STRIDE applicato a scenario
- Pseudonimizzazione/anonimizzazione
- Caso DPIA (riconoscimento facciale)

## Errori da evitare

- ❌ Threat modeling come "esercizio di nomenclatura"
- ❌ Confondere security e privacy
- ❌ "MD5 sull'email" = anonimizzazione (no)
- ❌ Saltare DPIA pensando "burocrazia"

## Prossimo modulo

**M6 — Sicurezza delle Applicazioni Web (9h)**

Adesso che sai **pensare** sicuro, scriviamo codice sicuro.
