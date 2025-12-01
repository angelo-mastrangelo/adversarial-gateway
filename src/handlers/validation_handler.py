from typing import Any, Dict
from src.handlers.abstract_handler import Handler

class ValidationHandler(Handler):
    """
    Input Validation.
    Assicura che i dati in ingresso rispettino i vincoli formali (MIME Type, Size)
    prima di essere passati alla logica di business.
    Questo previene errori di parsing a valle e potenziali exploit (es. Buffer Overflow simulati).
    """
    
    def handle(self, request: Dict[str, Any]) -> Any:
        meta = request.get("file_metadata", {})
        size_bytes = meta.get("size", 0)
        content_type = meta.get("content_type", "")
        
        # Lettura parametri dinamici dal file JSON
        max_mb = self.config.get("max_size_mb", 5)
        allowed = self.config.get("allowed_types", [])
        
        # Check 1: Dimensione File
        if size_bytes > (max_mb * 1024 * 1024):
            print(f"[Validation] ⛔ File too large ({size_bytes} bytes)")
            return {"error": f"File exceeds {max_mb}MB limit", "status_code": 400}
            
        # Check 2: Media Type (Whitelist approach)
        if content_type not in allowed:
            print(f"[Validation] ⛔ Type {content_type} not allowed")
            return {"error": f"Unsupported media type: {content_type}", "status_code": 415}
            
        print(f"[Validation] ✅ File Integrity OK")
        return super().handle(request)