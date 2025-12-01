import requests
import time
import os

"""
Adversarial Gateway Client.
Questo script funge da Client di integrazione per validare l'intero flusso architetturale.
Simula diversi scenari (Happy Path e Edge Cases) per verificare la robustezza della Chain of Responsibility.
"""

# Configurazione
URL = "http://localhost:8000/predict"
TOKEN = "my-super-secret-key"
IMG_NAME = "test_img.jpg"
BAD_FILE_NAME = "virus.exe.txt"

# 1. Creiamo un'immagine valida (Dummy)
if not os.path.exists(IMG_NAME):
    with open(IMG_NAME, "wb") as f:
        f.write(b'\xFF\xD8' + b'\x00' * 1000)

# 2. Creiamo un file NON valido (Testo semplice)
if not os.path.exists(BAD_FILE_NAME):
    with open(BAD_FILE_NAME, "w") as f:
        f.write("Questo non è una immagine, è un file di testo dannoso.")

def run_test(scenario_name, token=None, file_path=IMG_NAME, mime_type="image/jpeg", expect_code=200):
    print(f"\n🔹 --- {scenario_name} ---")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Prepariamo il file
    files = {"file": (file_path, open(file_path, "rb"), mime_type)}
    
    try:
        start = time.time()
        res = requests.post(URL, headers=headers, files=files)
        end = time.time()
        
        print(f"   Status Code: {res.status_code}")
        print(f"   Response: {res.json()}")
        
        if res.status_code == expect_code:
            print("   ✅ TEST PASSATO")
        else:
            print(f"   ❌ TEST FALLITO (Atteso {expect_code}, ricevuto {res.status_code})")
            
    except Exception as e:
        print(f"   Errore: {e}")

if __name__ == "__main__":
    print("AVVIO TEST AUTOMATIZZATI GATEWAY\n")

    # SCENARIO 1: Attacco senza Token
    # Deve essere bloccato da AuthHandler
    run_test("Scenario 1: Accesso senza Token", token=None, expect_code=401)

    # SCENARIO 2: File non valido (es. finto .exe o testo)
    # Deve essere bloccato da ValidationHandler
    run_test("Scenario 2: Upload file non valido (TXT)", token=TOKEN, file_path=BAD_FILE_NAME, mime_type="text/plain", expect_code=415)

    # SCENARIO 3: Utente Legittimo (Happy Path)
    # Deve passare e ricevere la predizione
    run_test("Scenario 3: Utente Legittimo", token=TOKEN, expect_code=200)

    # SCENARIO 4: Rate Limiting (DoS Attack Simulation)
    # Mandiamo 6 richieste. Il limite è 5. L'ultima deve fallire.
    print(f"\n🔹 --- Scenario 4: Stress Test (Rate Limit) ---")
    for i in range(1, 7):
        print(f"   Invio richiesta {i}...")
        # L'ultima richiesta (la sesta) ci aspettiamo che fallisca con 429
        expected = 429 if i > 5 else 200
        run_test(f"Richiesta rapida #{i}", token=TOKEN, expect_code=expected)
        # Niente sleep, andiamo veloci per triggerare il limite