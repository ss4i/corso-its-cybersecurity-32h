---
title: "M0 — Setup ambiente di lavoro"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M0 — Setup ambiente
## 2 ore — 0,5h teoria + 1,5h lab

## Obiettivi del modulo

- Avere Python 3.12 funzionante
- Saper aprire e usare il terminale
- VS Code con estensione Python
- Ambiente virtuale attivo
- Prima app Flask in browser

> "Senza ambiente, niente sicurezza."

## Cosa installeremo

- Python 3.12+
- Visual Studio Code
- Git (a casa)
- DB Browser for SQLite (a casa)
- Browser moderno (già lo hai)

Tutto **gratuito**, multipiattaforma.

## Perché Python

1. Sintassi pulita (zero prerequisiti)
2. Standard nel mondo cybersecurity
3. Flask: framework minimal per BancaPiccola

I concetti di sicurezza sono **universali** — Python è solo lo strumento.

## Step 1 — Python 3.12

- python.org → Download Python 3.12.x
- ⚠️ **CRUCIALE su Windows**: spunta *"Add Python to PATH"*
- Verifica: `python --version` → deve dire `Python 3.12.x`

## Step 2 — VS Code

- code.visualstudio.com
- Estensioni: **Python** (Microsoft) + **Pylance**
- Niente altro per ora — KISS

## Il terminale: comandi base

| Windows | macOS/Linux | Cosa fa |
|---------|--------------|---------|
| `cd ...` | `cd ...` | Cambia cartella |
| `dir` | `ls` | Lista file |
| `mkdir nome` | `mkdir nome` | Crea cartella |
| `python file.py` | `python3 file.py` | Esegue script |

## Hello World

```python
# hello.py
print("Pronto per il corso ITS di cybersec.")
```

Esecuzione:
```
python hello.py
```

Se vedi il messaggio → 50% pronto.

## Ambienti virtuali — `venv`

> Cartella isolata che contiene una copia di Python e le sue librerie.
> Pensa al "tuo studio di lavoro": gli attrezzi non si mescolano con altri progetti.

## Creazione e attivazione

```
python -m venv .venv
```

Attivazione:

| OS | Comando |
|----|---------|
| Windows PS | `.\.venv\Scripts\Activate.ps1` |
| macOS/Linux | `source .venv/bin/activate` |

✅ Verifica: nel prompt vedi `(.venv)`.

## Errore PowerShell comune

```
File cannot be loaded — running scripts is disabled
```

Soluzione (una tantum):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Hello Flask

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Ciao, sono BancaPiccola.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```

## Avvio del server

```
pip install flask
python hello_flask.py
```

Browser: http://127.0.0.1:5000

✅ Vedi il messaggio? **100% pronto**.

## Compito a casa

1. Installa Git → `git --version`
2. Installa DB Browser for SQLite
3. Clone BancaPiccola: `git clone <repo>`
4. `cd BancaPiccola-vuln && pip install -r requirements.txt && python app.py`

## Routine quotidiana

```
1. cd cybersec-its
2. .\.venv\Scripts\Activate.ps1
3. code .
```

Sempre questi 3 passi all'inizio.

## Verifica all'inizio di M1

- [ ] `python --version` ✅
- [ ] `(.venv)` visibile ✅
- [ ] Flask installato ✅
- [ ] hello_flask.py funziona ✅
- [ ] Browser vede 127.0.0.1:5000 ✅

## Prossimo modulo

**M1 — Fondamenti di Cybersecurity (4h)**

Hai l'ambiente. Adesso parliamo davvero di sicurezza.
