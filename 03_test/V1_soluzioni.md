# Verifica V1 — SOLUZIONI

**Punteggio totale:** 100
**Soglia di sufficienza:** 60

---

## Sezione A — Scelta multipla (20 × 1 = 20)

| # | Risposta | Note |
|---|----------|------|
| A1 | **b** | Confidentiality |
| A2 | **c** | Authenticity è un'estensione, NON nella CIA classica |
| A3 | **c** | DDoS = Availability |
| A4 | **b** | Least Privilege violato (root = privilegi massimi) |
| A5 | **b** | Default deny in caso di errore |
| A6 | **c** | 7 livelli (TCP/IP è il modello a 4) |
| A7 | **c** | Livello 4 — Transport |
| A8 | **b** | MAC = livello 2 (data link) |
| A9 | **c** | ARP = Address Resolution Protocol |
| A10 | **b** | SYN, SYN-ACK, ACK |
| A11 | **c** | DNS usa UDP (TCP solo per zone transfer e risposte grandi) |
| A12 | **b** | MITM in rete locale |
| A13 | **b** | 443 |
| A14 | **c** | "FETCH" non è un metodo HTTP standard |
| A15 | **c** | 403 = autenticato ma non autorizzato (vs 401 = non autenticato) |
| A16 | **b** | HSTS forza HTTPS dopo prima visita |
| A17 | **b** | HttpOnly = JS non può leggere il cookie (anti-XSS) |
| A18 | **b** | 401 Unauthorized = "non autenticato" (nome storico fuorviante) |
| A19 | **a** | Header che identifica il browser/client |
| A20 | **c** | Reato (Art. 617-quater c.p.) |

---

## Sezione B — Risposta breve (5 × 4 = 20)

### B1. Sicurezza informatica vs sicurezza del software

**Sicurezza informatica** (perimetrale, infrastrutturale): protegge la rete, i server, i sistemi operativi. L'attaccante "entra dalla rete". Esempio: un firewall che blocca SSH dall'esterno, un sistemista che applica patch al kernel, MFA su VPN.

**Sicurezza del software** (codice, applicazioni): protegge dall'interno della logica applicativa. L'attaccante manda richieste legittime con dati malevoli. Esempio: query SQL parametrizzata che impedisce SQL injection nel form di login.

> Punteggio: 2 punti per ogni esempio corretto e ben spiegato. Mezzo punto bonus se collega "il firewall non protegge da SQLi".

### B2. TCP vs UDP — 3 differenze

| Differenza | TCP | UDP | Caso d'uso |
|------------|-----|-----|-----------|
| Connessione | con handshake | senza | TCP per HTTP/SSH/FTP, UDP per DNS/VoIP |
| Affidabilità | sì (rispedisce pacchetti persi) | no | TCP per email/file, UDP per streaming |
| Ordine | sì | no | TCP per dati strutturati, UDP per gioco online |

> 1 punto per ogni differenza corretta + 1 punto per casi d'uso pertinenti.

### B3. ARP spoofing

**Cos'è**: l'attaccante manda risposte ARP non richieste sostenendo "l'IP X è il mio MAC", ingannando la vittima nella stessa rete locale. La vittima aggiorna la sua cache ARP e indirizza il traffico verso l'attaccante invece che al gateway/server vero.

**Livello OSI**: livello 2 (Data Link).

**Difese**: ARP statici per host critici, Dynamic ARP Inspection (DAI) sugli switch enterprise, monitoring della cache ARP, **HTTPS ovunque** (anche con MITM, l'attaccante vede solo dati cifrati).

> 1.5 punti definizione + 0.5 livello + 2 difese.

### B4. Cookie attributes

- **`Secure`**: il browser invia il cookie **solo su HTTPS**. Senza, il cookie può viaggiare in chiaro su HTTP e essere sniffato.
- **`HttpOnly`**: il cookie **non è leggibile da JavaScript** (`document.cookie`). Difesa contro XSS che vogliono rubare il session token.
- **`SameSite`**: controlla quando il browser invia il cookie in richieste cross-site. Valori: `Strict` (mai cross-site), `Lax` (default moderno: solo navigazione top-level), `None` (sempre, **richiede `Secure`**). Difesa contro CSRF.

> 1.3 punti per ognuno (rounding to 4).

### B5. Tre dei 5 principi del Secure Coding

(Ne basta citare 3 — ognuno con 1 esempio + 1 violazione.)

- **Least Privilege**: ✅ user DB con permessi solo SELECT/INSERT su tabelle proprie. ❌ webapp che gira come root.
- **Defense in Depth**: ✅ HTTPS + bcrypt + MFA + monitoring. ❌ "Abbiamo HTTPS, basta così".
- **Fail Secure**: ✅ se auth check lancia eccezione → 503. ❌ try/except che ritorna risorsa "per non bloccare".
- **KISS**: ✅ libreria di logging che fa solo logging. ❌ Log4Shell — feature JNDI non necessaria.
- **Separation of Duties**: ✅ chi scrive codice ≠ chi fa deploy. ❌ stesso DB user per dev/staging/prod.

> 1.3 punti per ogni principio con esempio + violazione.

---

## Sezione C — Esercizi (5 × 10 = 50)

### C1. Livelli OSI (10 pt)

| # | Termine | Livello |
|---|---------|---------|
| 1 | Frame Ethernet | **2** (Data Link) |
| 2 | Pacchetto IP | **3** (Network) |
| 3 | Segmento TCP | **4** (Transport) |
| 4 | Cookie HTTP | **7** (Application) |
| 5 | Cifratura TLS | **6** (Presentation) (o 5/6 — accettabile entrambi) |

### C2. Three-way handshake (10 pt)

```
Client                                   Server
  |                                         |
  | ───── SYN (seq=X, flag SYN=1) ────►     |   (Client: voglio connettermi)
  |                                         |
  |     ◄── SYN-ACK (seq=Y, ack=X+1, ──────┤   (Server: ok, ti rispondo)
  |          flag SYN=1, ACK=1)             |
  |                                         |
  | ───── ACK (ack=Y+1, flag ACK=1) ───►    |   (Client: ricevuto, partiamo)
  |                                         |
  |  ═════ Connessione stabilita ══════     |
```

> Punteggio: 3 pt direzione + 4 pt flag corretti + 3 pt sequenza.

### C3. Header di sicurezza mancanti (10 pt)

| Header mancante | A cosa serve / Perché manca è grave |
|-----------------|-------------------------------------|
| 1. `Strict-Transport-Security` (HSTS) | Forza HTTPS. Senza, possibile downgrade attack a HTTP. |
| 2. `Content-Security-Policy` (CSP) | Limita risorse caricabili. Senza, XSS più facile. |
| 3. `X-Frame-Options` | Blocca framing della pagina. Senza, vulnerabile a clickjacking. |
| 4. `X-Content-Type-Options: nosniff` | Blocca MIME sniffing. Senza, possibile esecuzione di file impropriamente serviti. |

(Accettabili anche `Referrer-Policy`, `Permissions-Policy`.)

**Cookie mancanze**:
- `Secure` (deve viaggiare solo su HTTPS).
- `HttpOnly` (non leggibile da JS).
- `SameSite=Lax` o `Strict` (anti-CSRF).

> 2 pt per header (max 4) + 2 pt cookie.

### C4. Equifax 2017 (10 pt)

1. **Confidentiality** (esfiltrazione dati personali).
2. **Web Application Attacks** o **Vulnerable/Outdated Components** (entrambi accettabili).
3. **Defense in Depth** (mancava layer dietro Struts) o **Least Privilege** (network segmentation insufficiente). Entrambi accettabili.
4. Esempi accettabili:
   - Patching SLA per CVE critiche (es. ≤7 giorni per CVSS ≥9).
   - SBOM e dependency scanning automatico.
   - Network segmentation tra front-end e DB.
   - Monitoring di esfiltrazione dati.

### C5. Scenario di rete (10 pt)

1. **GET** (2 pt).
2. **IDOR — Insecure Direct Object Reference**: cambiando l'id si accede al profilo di un altro utente senza controllo di autorizzazione (2 pt).
3. **SSN** (Social Security Number) — dato personale **sensibile**: non dovrebbe MAI essere restituito in un endpoint di profilo. Anche `email` può esserlo a seconda del contesto. Idealmente solo dati strettamente necessari (data minimization) (2 pt).
4. **No, mancano `Secure`, `HttpOnly`, `SameSite`**. Senza `Secure` il cookie può viaggiare su HTTP. Senza `HttpOnly` JS può leggerlo (XSS). Senza `SameSite` vulnerabile a CSRF (2 pt).
5. **Tutto in chiaro**: URL completo, headers (incluso il cookie), body con username/email/SSN/saldo. Sniffing banale su HTTP plain (2 pt).

---

## Griglia di valutazione

| Voto | Range punti |
|------|-------------|
| Eccellente | 90-100 |
| Buono | 75-89 |
| Sufficiente | 60-74 |
| Insufficiente | < 60 (recupero richiesto) |
