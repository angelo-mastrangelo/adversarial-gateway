# Usa un'immagine Python leggera ufficiale
FROM python:3.9-slim

# Imposta la cartella di lavoro dentro il container
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice sorgente nel container
COPY . .

# porta 8000
EXPOSE 8000

# Il comando per avviare il server
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]