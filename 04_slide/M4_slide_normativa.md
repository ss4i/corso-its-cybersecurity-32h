---
title: "M4 — Quadro Normativo Europeo"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M4 — Quadro Normativo
## 2 ore — solo teoria

## Obiettivi

- Conoscere **GDPR**, **NIS 2**, **CRA**
- Articoli che riguardano il codice
- Sanzioni e obblighi di notifica
- Casi italiani reali
- "Errore di codice → norma violata"

## Perché un programmatore deve sapere di leggi

❌ "Le leggi sono cose da avvocati"
❌ "Se sbaglio io, paga l'azienda"
❌ "Tanto in Italia non ti beccano"

> Tutte sbagliate. Le norme parlano di **codice**.

## GDPR in 3 righe

- Reg. (UE) 2016/679
- In vigore dal **25 maggio 2018**
- Si applica a chiunque tratti dati di residenti UE

## Cos'è un dato personale

> «Qualsiasi informazione riguardante una persona fisica identificata o identificabile»

- Sì: nome, email, IP fisso, foto, comportamento online
- No: statistiche aggregate anonime, codice sorgente

## Categorie particolari (Art. 9)

Protezione rinforzata:
- Salute
- Etnia, opinioni politiche/religiose
- Dati biometrici, genetici
- Vita / orientamento sessuale
- Dati giudiziari

## GDPR Art. 5 — i 6 principi

1. Liceità, correttezza, trasparenza
2. Limitazione delle finalità
3. **Minimizzazione**
4. Esattezza
5. Limitazione conservazione
6. **Integrità e riservatezza**

## GDPR Art. 25 — Privacy by Design

> «Misure tecniche e organizzative al momento di determinare i mezzi del trattamento»

→ Si **progetta** prima di scrivere codice (M5).

## GDPR Art. 32 — Sicurezza del trattamento

L'articolo che tocca direttamente il codice:

- (a) Pseudonimizzazione e **cifratura**
- (b) Riservatezza, integrità, disponibilità
- (c) Capacità di **ripristino** (backup)
- (d) Test e verifica regolare

## GDPR Art. 33-34 — Notifica breach

- **Art. 33**: notifica al Garante entro **72 ore**
- **Art. 34**: comunicazione agli interessati se rischio elevato
- Eccezione: dati cifrati con chiave al sicuro

## GDPR — sanzioni

| Categoria | Massimo |
|-----------|---------|
| Violazioni "minori" (no DPO, no DPIA) | 10M€ o 2% fatturato |
| Violazioni "maggiori" (principi base, diritti) | **20M€ o 4% fatturato** |

> Si applica **il maggiore**.

## NIS 2 in 3 righe

- Direttiva (UE) 2022/2555
- Recepita in Italia con D.Lgs. 138/2024
- Sostituisce NIS 1 (2016) — ambito molto più ampio

## NIS 2 — chi è "soggetto"

**Settori essenziali (All. I)**:
- Energia, trasporti, sanità, banche
- DNS, cloud, datacenter
- PA centrali e regionali

**Settori importanti (All. II)**:
- Servizi postali, gestione rifiuti
- Manifattura ICT, alimentare
- Servizi digitali (social, marketplace)

## NIS 2 — soglie

- Almeno 50 dipendenti **OPPURE** 10M€ fatturato
- Eccezione: soggetti critici (DNS, telco, ecc.) **a prescindere** dalle dimensioni

## NIS 2 Art. 21 — 10 misure obbligatorie

1. Politiche e analisi rischi
2. **Gestione incidenti**
3. Continuità operativa
4. Sicurezza supply chain
5. **SDLC sicuro, gestione vulnerabilità**
6. Valutazione efficacia
7. Igiene cyber e formazione
8. Politiche di **cifratura**
9. Sicurezza personale, controllo accessi
10. **MFA**, comunicazioni sicure

## NIS 2 Art. 23 — notifica (3 fasi)

| Tempo | Cosa |
|-------|------|
| **24h** | Early warning preliminare |
| **72h** | Notifica completa |
| **30gg** | Report finale |

⚠️ 24h sono strette → serve incident response plan.

## NIS 2 — sanzioni

| Categoria | Massimo |
|-----------|---------|
| Soggetti **essenziali** | 10M€ o 2% fatturato |
| Soggetti **importanti** | 7M€ o 1,4% fatturato |

> + **sospensione** del management dalla carica

## Cyber Resilience Act (CRA)

- Reg. (UE) 2024/2847
- **Piena applicazione: dicembre 2027**
- Per **prodotti con elementi digitali** in UE

## CRA — cosa cambia per gli sviluppatori

- Cybersecurity by design e by default
- **Niente vulnerabilità note** alla vendita
- Patching durante "supporto previsto" (≥5 anni)
- **SBOM obbligatorio**
- Notifica vulnerabilità sfruttate **24h** a ENISA
- Marcatura CE estesa al cyber

## CRA — categorie

| Categoria | Esempio | Conformità |
|-----------|---------|-----------|
| Default | App generiche | Auto |
| Importanti Classe I | Browser, antivirus | Standard armonizzati |
| Importanti Classe II | OS, hypervisor, firewall | Terza parte |
| Critici | HSM, smart card | Certificazione cyber |

## CRA — sanzioni

| Violazione | Massimo |
|-----------|---------|
| Requisiti essenziali non rispettati | 15M€ o 2,5% |
| Altre violazioni | 10M€ o 2% |
| Info false alle autorità | 5M€ o 1% |

## Tabella errore → norma (estratto)

| Errore | Norma | Sanzione |
|--------|-------|---------|
| SQL Injection con dati personali | GDPR Art. 32 | 20M€ |
| Password in MD5 | GDPR Art. 32(1)(a) | 20M€ |
| No HTTPS | GDPR Art. 32 | 20M€ |
| No notifica 72h | GDPR Art. 33 | 10M€ |
| No SBOM (CRA) | CRA Art. 13 | 15M€ |
| No MFA (NIS 2) | NIS 2 Art. 21 | 10M€ |

## Caso italiano — banca password chiaro

- 2023: piccola banca italiana
- DB con password in chiaro
- Sanzione: ~600.000€
- Art. 32(1)(a)
- **Era prevenibile con bcrypt**

## Caso italiano — comune

- 2023: graduatoria con dati ISEE pubblica online
- Sanzione: ~80.000€
- Art. 5(1)(f), 32

## Caso italiano — IDOR e-commerce

- 2022: URL `/ordine/<id>` non protetti
- Sanzione: ~100.000€
- **Ownership check sarebbe bastato**

## Caso italiano — token API su GitHub

- 2024: app delivery espone API token
- Sanzione: ~250.000€
- **Secrets management + pre-commit hook**

## Diagramma post-breach

```
Scoperta breach
    ↓
T+0:    STOP, documenta, avvisa CSO/DPO
    ↓
T+1h:   Contenimento (isola, blocca, ruota)
    ↓
NIS 2?  → Early warning 24h
    ↓
Dati personali? → Notifica Garante 72h
    ↓
Rischio alto? → Comunica anche interessati
    ↓
T+30gg: Report finale (NIS 2)
    ↓
Post-mortem + threat model update
```

## Quando si applicano insieme

Banca italiana → breach con dati personali:

- **GDPR**: notifica 72h, fino a 20M€
- **NIS 2**: 24h + 72h + 30gg, fino a 10M€

> Sanzioni si **cumulano** + management sospeso

## Mini quiz

Q1. Notifica breach al Garante? **72h**
Q2. Articolo Privacy by Design? **Art. 25**
Q3. Sanzione massima GDPR? **20M€ o 4%**
Q4. CRA in vigore pieno? **Dicembre 2027**
Q5. NIS 2 prevede MFA? **Sì (Art. 21)**

## Prossimo modulo

**M5 — Security & Privacy by Design (3h)**

Sai cosa la legge richiede. Ora come si applica **a progetto**?
