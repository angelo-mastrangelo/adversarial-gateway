import time
from typing import Any, Dict
from src.handlers.abstract_handler import Handler

class RateLimitHandler(Handler):
    """
    Rate Limiting / Throttling.
    Questo handler implementa una protezione contro attacchi di tipo Denial of Service (DoS)
    e Brute Force. Utilizza un algoritmo 'Fixed Window' in memoria per limitare
    il numero di richieste per IP.
    
    Obiettivo Architetturale:
    - Garantire la disponibilità del servizio (Availability).
    - Prevenire il sovraccarico delle risorse a valle (Modello ML).
    """
    
    # Stato condiviso (in-memory) per tracciare le richieste.
    # In produzione, questo verrebbe sostituito da uno store distribuito come Redis.
    _request_history = {} 

    def handle(self, request: Dict[str, Any]) -> Any:
        client_ip = request.get("client_ip", "unknown")
        limit = self.config.get("limit", 5)
        window = self.config.get("window_seconds", 60)
        
        now = time.time()
        
        # Inizializzazione storico per il client corrente
        if client_ip not in self._request_history:
            self._request_history[client_ip] = []
        
        # [ALGORITMO] Pulizia della finestra temporale
        # Rimuove i timestamp più vecchi della finestra configurata.
        self._request_history[client_ip] = [
            t for t in self._request_history[client_ip] if now - t < window
        ]
        
        # Verifica della soglia
        if len(self._request_history[client_ip]) >= limit:
            print(f"[RateLimit] ⛔ Blocked IP {client_ip}: Too many requests")
            # [FAIL-FAST] Interruzione immediata della catena
            return {"error": "Too Many Requests", "status_code": 429}
        
        # Registrazione della nuova richiesta
        self._request_history[client_ip].append(now)
        
        print(f"[RateLimit] ✅ IP {client_ip} OK ({len(self._request_history[client_ip])}/{limit})")
        
        # Passaggio al prossimo handler
        return super().handle(request)