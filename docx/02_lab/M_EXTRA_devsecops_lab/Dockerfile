FROM python:3.12-slim

# Best practice: utente non-root
RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 5000

# Bind solo localhost in produzione (in dev a 0.0.0.0 per il container)
CMD ["python", "app.py"]
