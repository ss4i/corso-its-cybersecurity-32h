# M7 — Lab Integrato + Chiusura (2h)

## Obiettivo

Verifica trasversale **applicata**: il discente, su un'app reale (BancaPiccola completa), deve:

1. Identificare **almeno 3 vulnerabilità** tra quelle viste nel corso.
2. Per ognuna, produrre:
   - Una **descrizione** (cos'è, dove si trova, cosa permette di fare)
   - Un **Proof of Concept** funzionante (uno screenshot o un comando)
   - Una **proposta di fix** in codice Python/Flask
   - Un **livello di severity** giustificato in stile CVSS (anche solo Low/Medium/High/Critical)
3. Consegnare un **mini-report** scritto (1-2 pagine).

## Modello mentale

> Il discente non sta più "imparando una vulnerabilità alla volta". Deve **scegliere quale cercare**, **come testarla**, **come scriverla**. È il momento più simile al lavoro reale.

## Materiale di riferimento

- `BancaPiccola-repo/BancaPiccola-vuln/` — l'app vulnerabile (versione completa, non più la `mini`)
- `BancaPiccola-repo/BancaPiccola-secure/` — la versione corretta (consultabile **solo a fine consegna** come riferimento)
- Cheat-sheet riassuntivo: `02_lab/M7_cheatsheet.md` (da produrre — lo aggiungo se serve)

## Articolazione oraria

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:15 | **Briefing** — Spiegazione consegna, regole, cosa è permesso e cosa no. | Frontale |
| 0:15 – 1:30 | **Lavoro individuale o a coppie** — il discente esplora BancaPiccola-vuln cercando vulnerabilità. Il docente passa tra i banchi e sblocca chi è fermo. | **Lab attivo** |
| 1:30 – 1:50 | **Discussione collettiva** — ogni discente/coppia condivide UNA vulnerabilità trovata e la sua proposta di fix. Il docente confronta con BancaPiccola-secure. | Discussione |
| 1:50 – 2:00 | **Chiusura corso** — ricapitolazione, prossimi passi (anno 2 ITS), risorse di approfondimento (PortSwigger Web Academy, OWASP, HackTheBox). | Frontale |

## Regole del lab

✅ **Permesso**:

- Leggere il codice sorgente di BancaPiccola-vuln (è un lab didattico, non un CTF).
- Usare DevTools, curl, requests, sqlite3, qualunque tool visto nel corso.
- Lavorare a coppie.
- Chiedere hint al docente (ne riceverai uno costoso: -10% sul voto se chiedi più di 1 hint).

🚫 **Non permesso**:

- Aprire BancaPiccola-secure prima della consegna.
- Cercare la soluzione su Google con la query "BancaPiccola vulnerabilities".
- Copiare il report da un compagno (ovvio).

## Cheat-sheet rapido (da consegnare in aula)

Questo è il "kit minimo" per non bloccarsi. Non dà la soluzione, ma indica dove cercare.

```
Vuoi cercare SQL Injection?
   → Form di login, ricerca, qualunque parametro che finisce in WHERE.
   → Test rapidi: '  '' " ' OR '1'='1  ' OR 1=1 --

Vuoi cercare IDOR?
   → URL con ID numerici (es. /fattura/42, /utente/3).
   → Test: cambia l'ID e vedi se accedi.

Vuoi cercare XSS?
   → Campi di testo che vengono "rivisualizzati" (commenti, profilo, search).
   → Test rapidi: <script>alert(1)</script>  <img src=x onerror=alert(1)>

Vuoi cercare Crypto Failures?
   → Apri il DB con DB Browser. Le password sono in chiaro? In MD5? In bcrypt?

Vuoi cercare Path Traversal?
   → Endpoint che servono/scaricano file. Param "filename" o simile.
   → Test rapidi: ../etc/passwd  ../../app.py
```

## Output e valutazione

### Output del discente

Un file `cognome_nome_M7_report.md` (o `.docx` o `.pdf`) con:

```markdown
# Mini-PT Report — BancaPiccola

## Findings

### F-01 — [titolo vulnerabilità]
- **Severity**: Low / Medium / High / Critical
- **Localizzazione**: file/endpoint
- **Descrizione**: cos'è, perché è una vulnerabilità
- **PoC**: comando o screenshot
- **Fix proposto**: codice Python corretto
- **Norma violata**: GDPR Art. ?, NIS 2, ecc.

### F-02 — ...
### F-03 — ...
```

### Griglia di valutazione (su 100 punti)

| Voce | Peso |
|------|------|
| Numero vulnerabilità trovate (≥3) | 20 |
| Correttezza tecnica delle PoC | 30 |
| Qualità dei fix proposti | 30 |
| Severity giustificata | 10 |
| Norma violata identificata | 10 |

**Soglia di sufficienza**: 60/100.

## Vulnerabilità presenti in BancaPiccola-vuln

> **Per il docente** (non distribuire al discente prima della consegna). Lista delle vuln che dovrebbero essere trovate.

1. **SQL Injection** nel form di login (`/login`).
2. **IDOR** nell'endpoint `/fattura/<id>` (manca controllo ownership).
3. **Stored XSS** nei commenti del profilo (manca escape).
4. **Crypto Failures**: password salvate in SHA-1 senza salt.
5. **Path Traversal** nell'endpoint `/download?file=...`.
6. (Bonus) **Supply chain**: `requirements.txt` con Flask 2.0.0 (CVE nota).
7. (Bonus) **Cookie senza HttpOnly/Secure/SameSite**.

> **Confronto con il modulo**: 5 vulnerabilità sono direttamente quelle viste in M6, 2 sono "bonus" che premiano lo studente attento. Trovare 3 di queste è la sufficienza, trovarne 5+ con fix corretto è eccellenza.

## Errori da evitare in classe

- **Non lasciare nessuno a vuoto i primi 30 min**: chi non sa da dove iniziare blocca tutto. Distribuire il cheat-sheet alla T+15 se serve.
- **Non fare uscire la versione secure prima**: vanifica il lab.
- **Non valutare solo il numero di vuln trovate**: la qualità del fix conta più del numero.
- **Lasciare 10 min reali per la chiusura del corso**: i discenti hanno bisogno di sentire "siete arrivati alla fine, ora sapete molto più di quanto pensiate". È un momento didatticamente importante.
