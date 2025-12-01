from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Handler(ABC):
    """
    Questa classe astratta definisce l'interfaccia comune per tutti i nodi della catena.
    Gestisce il puntatore al prossimo handler (_next_handler) e la logica di propagazione.
    """

    def __init__(self, config: dict = None):
        # Mantiene il riferimento al prossimo anello della catena
        self._next_handler: Optional['Handler'] = None
        # Configurazione specifica per questo handler (es. soglie, token)
        self.config = config or {}

    def set_next(self, handler: 'Handler') -> 'Handler':
        """
        [FLUENT INTERFACE] Imposta il prossimo handler nella sequenza.
        Restituisce l'handler passato per permettere il chaining (h1.set_next(h2).set_next(h3)).
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Dict[str, Any]) -> Any:
        """
        Metodo template che ogni Handler concreto deve implementare.
        
        Logica di base:
        1. L'handler corrente prova a gestire la richiesta.
        2. Se la richiesta è valida, chiama super().handle(request) per passare al prossimo.
        3. Se la richiesta è invalida, interrompe la catena ritornando un errore.
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        
        # Se siamo arrivati qui, la catena è finita con successo
        return None