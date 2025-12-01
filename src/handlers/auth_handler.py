from typing import Any, Dict
from src.handlers.abstract_handler import Handler

class AuthHandler(Handler):
    """
    Authentication & Access Control.
    Verifica l'identità del client tramite Bearer Token.
    Questo controllo avviene all'inizio della catena per evitare di processare
    dati (es. immagini pesanti) provenienti da fonti non attendibili.
    
    Principio: Fail-Fast (Fallire prima possibile per risparmiare risorse).
    """
    
    def handle(self, request: Dict[str, Any]) -> Any:
        # Estrazione Headers dal Context
        headers = request.get("headers", {})
        token = headers.get("authorization") 
        
        # Recupero del segreto dalla configurazione iniettata dalla Factory
        secret = self.config.get("token_secret", "")
        expected_token = f"Bearer {secret}"
        
        # Validazione formale del token
        if not token or token != expected_token:
            print(f"[Auth] ⛔ Invalid Token")
            return {"error": "Unauthorized: Invalid or missing token", "status_code": 401}
        
        print(f"[Auth] ✅ Identity Verified")
        
        # Delegazione al prossimo anello della catena
        return super().handle(request)