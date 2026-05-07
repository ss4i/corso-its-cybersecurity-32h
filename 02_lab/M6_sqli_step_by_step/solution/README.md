# Soluzione — App SECURE

Versione corretta dell'app del lab. **Non aprirla prima** di aver completato gli step 1-4.

## Diff principali rispetto all'app vulnerabile

### 1. Login parametrizzato

```diff
-    sql = (
-        f"SELECT id, email, saldo FROM users "
-        f"WHERE email = '{email}' AND password = '{pwd}'"
-    )
-    row = conn.execute(sql).fetchone()
+    sql = "SELECT id, email, saldo FROM users WHERE email = ? AND password = ?"
+    row = conn.execute(sql, (email, pwd)).fetchone()
```

### 2. Cerca parametrizzato

```diff
-    sql = f"SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE '%{q}%'"
-    risultati = [r[0] for r in conn.execute(sql).fetchall()]
+    sql = "SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE ?"
+    risultati = [r[0] for r in conn.execute(sql, (f"%{q}%",)).fetchall()]
```

### 3. Errori generici al client

```diff
-    errore = f"Errore SQL: {e}"
+    log.exception("Errore DB durante login")
+    errore = "Errore interno del server"
```

### 4. Logging strutturato (anteprima M_EXTRA logging)

```python
log.info(f"login_success email={email}")
log.warning(f"login_failure email={email[:50]}")
```

## Come provarla

```bash
cd ../   # torna alla cartella del lab
python seed.py
# Sostituisci app.py con la versione corretta:
cp solution/app.py app.py
python app.py
```

Apri http://127.0.0.1:5000 e prova gli stessi attacchi degli step 2-4. Tutti **falliscono**.

```bash
# Verifica con i test
pytest test_app.py -v
```

Tutti i test passano (sulla vulnerabile, alcuni falliscono — ed è corretto così).

## Differenze residue rispetto a "production grade"

Questa versione è **secure** rispetto a SQLi, ma per essere production-grade mancano:

- ✗ Password hashing con bcrypt (vedi M6.4)
- ✗ Rate limiting sul login (vedi M_EXTRA strumenti)
- ✗ HTTPS (vedi M3)
- ✗ Cookie sicuri (vedi M3)
- ✗ CSRF protection (vedi M_EXTRA jwt_oauth_csrf)
- ✗ Input validation strutturata (vedi M_EXTRA input_validation)
- ✗ Audit log immutabile (vedi M_EXTRA logging)
- ✗ Session ID sicuro (Flask-Login o equivalente)

Tutti questi sono coperti da altri moduli del corso. Questa è la **base secure-by-default per SQLi**, da cui si costruisce il resto.
