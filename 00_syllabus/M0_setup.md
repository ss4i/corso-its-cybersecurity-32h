# M0 — Setup ambiente di lavoro (2h)

## Obiettivo

Al termine del modulo il discente ha sul proprio computer un ambiente di lavoro funzionante e sa:

- Aprire un terminale (PowerShell su Windows, Terminal su macOS/Linux).
- Eseguire un programma Python e capire cos'è un "interprete".
- Usare Visual Studio Code per scrivere codice.
- Creare e attivare un ambiente virtuale Python (`venv`).
- Avviare una mini-app Flask e visitarla nel browser.
- Clonare il repository BancaPiccola con Git.
- Aprire un database SQLite con DB Browser.

> Questo modulo non parla di sicurezza. Parla di come **predisporre** l'ambiente che ci servirà per fare sicurezza nei moduli successivi. È un investimento di 2 ore che fa risparmiare 20 ore di problemi tecnici nei moduli seguenti.

## Materiale di riferimento

- `dispensa-sviluppo-sicuro-software.docx` → **Capitolo 0** (riusato integralmente)
- Screenshot già pronti in `DispenseCodiceSicuro/screenshots/`

## Articolazione oraria

| Tempo | Attività | Modalità |
|-------|----------|----------|
| 0:00 – 0:15 | Presentazione del corso e di M0. Cosa installeremo e perché. | Frontale |
| 0:15 – 0:35 | **Lab 1** — Installazione Python 3.12 + verifica `python --version` | Lab guidato |
| 0:35 – 0:50 | **Lab 2** — Installazione VS Code + estensioni Python e Pylance | Lab guidato |
| 0:50 – 1:05 | Il terminale: cos'è, come si apre, comandi base (`cd`, `dir/ls`, `mkdir`) | Frontale + lab |
| 1:05 – 1:25 | **Lab 3** — Prima cartella di lavoro, primo `hello.py`, esecuzione | Lab guidato |
| 1:25 – 1:40 | Ambienti virtuali: cosa sono, perché sono obbligatori | Frontale |
| 1:40 – 2:00 | **Lab 4** — `python -m venv .venv`, attivazione, `pip install flask`, hello-flask | Lab guidato |

> Le installazioni di **Git**, **DB Browser** e il **clone di BancaPiccola** vengono fatte come "compito a casa" tra G1 e G2 (con istruzioni dal Cap 0). Si verifica all'inizio di M1.

## Lab del modulo

### Lab M0.1 — Hello, Python
File: `lab_m0_1_hello.py` (un solo `print`).
Verifica: l'output appare nel terminale dopo `python lab_m0_1_hello.py`.

### Lab M0.2 — Hello, Flask
File: `lab_m0_2_hello_flask.py`. Una rotta `/` che restituisce "Ciao, sono BancaPiccola".
Verifica: il browser su `http://127.0.0.1:5000/` mostra il messaggio.

## Verifica

Nessuna verifica scritta. **Verifica pratica** all'inizio di M1: il discente deve mostrare l'app Flask attiva. Se non funziona, problema risolto in classe (5-10 min) prima di iniziare M1.

## Output atteso

Al termine, ogni discente ha:

```
~/cybersec-its/
  ├── .venv/             ← ambiente virtuale attivato
  ├── hello.py
  └── hello_flask.py
```

E al prompt vede `(.venv)` prima del path. Da qui in avanti tutto il corso lavora dentro `~/cybersec-its/`.
