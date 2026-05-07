# Verifica Intermedia 2 — Post M5 (19h)

**Corso:** Cybersecurity e Sicurezza delle Applicazioni — ITS
**Moduli coperti:** M4 + M5 (più richiami trasversali a M1-M3)
**Durata:** 50 minuti
**Punteggio totale:** 100

**Cognome e Nome:** _______________________________
**Data:** _________________________________________

---

## Istruzioni

- 25 domande totali: 15 a scelta multipla (2 punti), 5 a risposta breve (4 punti), 1 esercizio STRIDE (30 punti), 1 caso DPIA (20 punti). Tot: 100.
- La consegna del workshop M5 (tabella STRIDE su BancaPiccola) entra nella valutazione complessiva.

---

## Sezione A — Scelta multipla (15 × 2 = 30 punti)

**A1.** Quale articolo del GDPR introduce il concetto di "Privacy by Design"?
- [ ] a) Art. 5
- [ ] b) Art. 25
- [ ] c) Art. 32
- [ ] d) Art. 33

**A2.** Entro quante ore dalla scoperta di un data breach un titolare GDPR deve notificare al Garante?
- [ ] a) 24 ore
- [ ] b) 48 ore
- [ ] c) 72 ore
- [ ] d) 7 giorni

**A3.** Le sanzioni massime GDPR possono arrivare a:
- [ ] a) 10M€ o 2% fatturato annuo
- [ ] b) 20M€ o 4% fatturato annuo
- [ ] c) 50M€ o 5% fatturato annuo
- [ ] d) 100M€

**A4.** La direttiva NIS 2 si applica principalmente a:
- [ ] a) Tutti i siti web in UE
- [ ] b) Solo banche e assicurazioni
- [ ] c) Settori essenziali e importanti definiti negli allegati (energia, trasporti, sanità, finanza, ICT, ecc.)
- [ ] d) Solo enti pubblici

**A5.** Il Cyber Resilience Act (CRA) entrerà pienamente in vigore:
- [ ] a) Già applicabile dal 2024
- [ ] b) Dicembre 2027
- [ ] c) Solo dopo il 2030
- [ ] d) Non è ancora stato approvato

**A6.** STRIDE è un framework per:
- [ ] a) Crittografia
- [ ] b) Threat modeling
- [ ] c) Penetration testing
- [ ] d) Compliance audit

**A7.** Cosa rappresenta la "T" in STRIDE?
- [ ] a) Trust (fiducia)
- [ ] b) Tampering (manomissione)
- [ ] c) Throttling (rate limit)
- [ ] d) Tunneling (VPN)

**A8.** La "E" di STRIDE corrisponde a:
- [ ] a) Encryption
- [ ] b) Eavesdropping
- [ ] c) Elevation of Privilege
- [ ] d) Exfiltration

**A9.** "Shift Left" della sicurezza significa:
- [ ] a) Spostare la sicurezza in fasi più tardive del ciclo di sviluppo
- [ ] b) Spostare la sicurezza il più presto possibile (dal design)
- [ ] c) Centralizzare la sicurezza in un unico team
- [ ] d) Esternalizzare la sicurezza a un fornitore

**A10.** Un Data Flow Diagram (DFD) usa quale di questi simboli per un **datastore**?
- [ ] a) Cerchio
- [ ] b) Rettangolo
- [ ] c) Due linee parallele
- [ ] d) Triangolo

**A11.** Un **trust boundary** in un DFD è:
- [ ] a) Il perimetro fisico dell'azienda
- [ ] b) Una linea che separa due zone con livelli di fiducia diversi
- [ ] c) La rete di management
- [ ] d) Il firewall principale

**A12.** Quale di questi NON è uno dei 7 principi di Privacy by Design di Cavoukian?
- [ ] a) Privacy as Default
- [ ] b) Proactive not Reactive
- [ ] c) Encryption Everywhere
- [ ] d) End-to-End Security

**A13.** Per il GDPR, **dato pseudonimizzato**:
- [ ] a) È equivalente a dato anonimo, GDPR non si applica
- [ ] b) È ancora dato personale, GDPR si applica
- [ ] c) È vietato per default
- [ ] d) Richiede consenso esplicito sempre

**A14.** L'anonimizzazione vera è:
- [ ] a) Sostituire l'email con un ID numerico
- [ ] b) Cifrare i dati con chiave separata
- [ ] c) Rendere irreversibile il legame con la persona, anche con dati esterni
- [ ] d) Hashare l'email con MD5

**A15.** Una DPIA è obbligatoria quando:
- [ ] a) Sempre, per qualunque trattamento
- [ ] b) Solo per le banche
- [ ] c) Per trattamenti che presentano rischio elevato (profilazione automatizzata, dati sensibili su larga scala, sorveglianza sistematica)
- [ ] d) Solo se richiesto dal Garante dopo un'ispezione

---

## Sezione B — Risposta breve (5 × 4 = 20 punti)

**B1.** *(4 punti)* Spiega in 3-4 righe la differenza tra **pseudonimizzazione** e **anonimizzazione**, e indica quale delle due richiede ancora il rispetto del GDPR.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B2.** *(4 punti)* Un'app raccoglie dati di salute (battiti, sonno, attività fisica) di milioni di utenti. Cita **3 misure tecniche** specifiche per essere conforme a GDPR Art. 32 (sicurezza del trattamento).

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B3.** *(4 punti)* Qual è la differenza tra **Spoofing** e **Tampering** in STRIDE? Per ognuna fornisci un esempio in BancaPiccola.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B4.** *(4 punti)* Cosa sono le 4 domande di Adam Shostack per il threat modeling? Elencale.

1. _________________________________________________
2. _________________________________________________
3. _________________________________________________
4. _________________________________________________

**B5.** *(4 punti)* Per ognuna delle seguenti azioni in BancaPiccola, indica quale **proprietà CIA** è prioritariamente coinvolta:

| Azione | C / I / A |
|--------|-----------|
| Bonifico effettuato dall'utente | _______ |
| Lista password dei clienti | _______ |
| Accesso alla pagina di login durante un picco di traffico | _______ |
| Modifica del saldo del conto via SQL Injection | _______ |

---

## Sezione C — Esercizio STRIDE (30 punti)

### Scenario

Un piccolo e-commerce italiano vende prodotti alimentari biologici. Il sistema:

- Frontend: HTML + JS reso da un server Flask.
- Backend: Flask, gira su VPS.
- Database: PostgreSQL su un server separato (stesso datacenter, rete privata).
- Funzionalità: ricerca prodotti, registrazione utente, login, ordine, pagamento via API esterna (Stripe), email di conferma via SMTP esterno.

### Consegna

**1.** Disegna il DFD nello spazio sotto. Indica chiaramente i **trust boundary** (almeno 2). *(8 punti)*

```
[Spazio per disegno]






```

**2.** Compila la tabella STRIDE con **almeno 9 minacce** distribuite tra le 6 categorie. Per ognuna: descrizione e difesa. *(18 punti — 2 pt per ogni minaccia ben formulata con difesa pertinente)*

| # | Elemento DFD | STRIDE | Descrizione minaccia | Difesa |
|---|--------------|--------|------------------------|--------|
| 1 | _______ | _ | _________________________ | _________________________ |
| 2 | _______ | _ | _________________________ | _________________________ |
| 3 | _______ | _ | _________________________ | _________________________ |
| 4 | _______ | _ | _________________________ | _________________________ |
| 5 | _______ | _ | _________________________ | _________________________ |
| 6 | _______ | _ | _________________________ | _________________________ |
| 7 | _______ | _ | _________________________ | _________________________ |
| 8 | _______ | _ | _________________________ | _________________________ |
| 9 | _______ | _ | _________________________ | _________________________ |

**3.** Per la **minaccia più grave** che hai identificato, motiva perché lo è (probabilità × impatto). *(4 punti)*

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

---

## Sezione D — Caso DPIA (20 punti)

### Scenario

Una scuola ITS sta implementando un sistema di **riconoscimento facciale** all'ingresso delle aule per registrare la presenza degli studenti. Il sistema:

- Cattura un'immagine del volto al passaggio del lettore badge
- Confronta con un template biometrico salvato nel sistema
- Registra presenza/assenza nel registro elettronico
- Conserva le immagini per 30 giorni (per "verifiche")

### Domande

**D1.** *(5 punti)* La **DPIA è obbligatoria** in questo caso? **Sì o No**, e **perché**?

___________________________________________________

___________________________________________________

___________________________________________________

**D2.** *(5 punti)* Cita **almeno 3 rischi** per gli interessati che la DPIA dovrebbe analizzare.

1. _________________________________________________
2. _________________________________________________
3. _________________________________________________

**D3.** *(5 punti)* Applica il principio di **Data Minimization**: c'è un'alternativa al riconoscimento facciale che raggiunga lo stesso obiettivo (registrare presenze) con minore invasività? Proponi e spiega.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**D4.** *(5 punti)* Indica **2 misure tecniche** e **2 misure organizzative** che la scuola dovrebbe adottare se decidesse di procedere con il riconoscimento facciale.

**Tecniche**:
1. _________________________________________________
2. _________________________________________________

**Organizzative**:
1. _________________________________________________
2. _________________________________________________

---

**FINE — Buon lavoro.**
