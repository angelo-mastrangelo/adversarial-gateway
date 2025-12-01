# Usa un'immagine Python leggera ufficiale
FROM python:3.9-slim

# Imposta la cartella di lavoro dentro il container
WORKDIR /app

# Copia il file dei requisiti e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice sorgente nel container
COPY . .

# Esponi la porta 8000 (quella di FastAPI)
EXPOSE 8000

# Il comando per avviare il server (lo stesso che hai usato tu)
CMD ["python", "-m", "src.server"]