# M1 — Fondamenti di Cybersecurity (4h)

## Obiettivo

Al termine del modulo il discente sa:

1. Definire cosa significa "sicurezza" in informatica e illustrare la **CIA Triad** (Confidentiality, Integrity, Availability) con esempi.
2. Distinguere **sicurezza informatica** (perimetrale, infrastrutturale) da **sicurezza del codice** (applicazioni, dati, API).
3. Riconoscere e classificare le principali categorie di **minacce**: malware, phishing/ingegneria sociale, MITM, DoS/DDoS, ransomware, supply chain attack, insider threat.
4. Spiegare i **5 principi del Secure Coding**: Least Privilege, Defense in Depth, Fail Secure, KISS, Separazione dei Compiti.
5. Adottare la **mentalità avversaria** ("come romperei questo sistema?") quando legge o scrive codice.
6. Citare almeno 3 incidenti reali e indicare per ognuno la causa tecnica e il principio violato.

## Materiale di riferimento

- `dispensa-sviluppo-sicuro-software.docx` → **Capitolo 1** (Perché la sicurezza riguarda chi scrive codice)
- Materiale nuovo: `01_materiali/M1_fondamenti_cybersecurity.md` (integra CIA triad e tassonomia minacce, mancanti nel Cap 1)

## Articolazione oraria

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:30 | **1.1 Perché un programmatore deve sapere di sicurezza** — Differenza tra sicurezza informatica e sicurezza del software. La sicurezza non è un add-on, è una proprietà. | Frontale |
| 0:30 – 1:00 | **1.2 La CIA Triad** — Confidentiality, Integrity, Availability. Esempi concreti per ogni proprietà. Aggiungiamo Authenticity, Non-repudiation, Accountability. | Frontale + esempi |
| 1:00 – 1:45 | **1.3 Tassonomia delle minacce** — Malware (virus/worm/trojan/ransomware), phishing, MITM, DoS/DDoS, supply chain, zero-day, insider. Per ognuna: cos'è, esempio reale, chi protegge. | Frontale |
| 1:45 – 2:15 | **1.4 Cinque casi reali** raccontati come storie: Equifax 2017 (Apache Struts), Heartbleed 2014 (OpenSSL), Target 2013 (HVAC vendor), SolarWinds 2020 (supply chain), Log4Shell 2021. Per ognuno: cos'è successo, cosa si poteva fare. | Storytelling |
| 2:15 – 2:30 | **PAUSA** | |
| 2:30 – 3:00 | **1.5 La mentalità avversaria** — Come pensa un attaccante. Differenza tra "fa quello che deve fare" e "non fa nulla che non deve fare". Esercitazione di brainstorming su un form di login. | Frontale + Q&A |
| 3:00 – 3:30 | **1.6 I 5 Principi del Secure Coding** — Least Privilege, Defense in Depth, Fail Secure, KISS, Separation of Duties. Esempi positivi e negativi per ognuno. | Frontale |
| 3:30 – 4:00 | **Lab M1** — Analisi guidata di un breach reale a scelta del discente (a coppie), 20 min preparazione + 10 min discussione collettiva. | Lab a coppie |

## Lab del modulo (1h)

### Lab M1 — "Cosa è andato storto?"

**Obiettivo**: applicare CIA + 5 principi a un caso reale.

**Setup**: ogni coppia sceglie uno dei 5 casi visti (o ne propone uno nuovo).

**Consegna scritta breve** (10 minuti, 1 pagina):

1. Riassunto in 3-4 righe dell'incidente.
2. Quale proprietà CIA è stata violata?
3. Quale principio del Secure Coding è stato ignorato?
4. Una misura tecnica concreta che avrebbe evitato (o limitato) l'incidente.

**Discussione collettiva** (20 minuti): ogni coppia espone in 2 minuti. Il docente sintetizza alla lavagna i pattern ricorrenti.

## Verifica

Domande di autovalutazione (non valutate, fanno parte di V1 a fine M3):

- Definisci la CIA Triad con un esempio per ogni proprietà.
- Cita 3 differenze tra sicurezza informatica e sicurezza del software.
- Cosa significa "Fail Secure"? Fai un esempio negativo (Fail Open) e uno positivo.
- In Equifax 2017, quale principio è stato violato?

## Errori da evitare in classe

- **Non confondere sicurezza con cifratura**. La cifratura è uno strumento, la sicurezza è una proprietà del sistema.
- **Non dire "tanto a noi non capita"**. Tutti i breach raccontati sono iniziati con quella convinzione.
- **Non iniziare dal codice**. M1 è teorico per scelta — dopo i discenti capiranno **perché** una query parametrizzata non è "una pignoleria".
