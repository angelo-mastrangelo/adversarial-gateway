import json
import importlib
import re
from typing import Optional
from src.handlers.abstract_handler import Handler

class ChainFactory:
    """
    Questa classe è responsabile della creazione dell'intera catena di sicurezza.
    Utilizza la REFLECTION per istanziare le classi dinamicamente basandosi sul file JSON.
    
    Vantaggio Architetturale:
    - Rispetta l'Open/Closed Principle: Possiamo aggiungere nuovi Handler creando 
      solo il nuovo file, senza dover modificare il codice di questa Factory.
    """

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Utility per convertire CamelCase (NomeClasse) in snake_case (nome_file)."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    @staticmethod
    def load_config(config_path: str) -> dict:
        """Carica la configurazione deserializzando il JSON."""
        with open(config_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def create_chain(config_path: str) -> Optional[Handler]:
        config = ChainFactory.load_config(config_path)
        chain_conf = config.get("security_chain", [])
        
        first_handler = None
        current_handler = None

        print(f" [FACTORY] Initializing Security Chain from {config_path}...")

        for h_conf in chain_conf:
            # Skip degli handler disabilitati da configurazione
            if not h_conf.get("enabled", True):
                print(f"   Original -> Skipping {h_conf['name']} (Disabled)")
                continue

            class_name = h_conf["name"]
            # Calcolo dinamico del percorso del modulo
            module_name = f"src.handlers.{ChainFactory._to_snake_case(class_name)}"

            try:
                # [REFLECTION] Importazione dinamica del modulo e della classe
                module = importlib.import_module(module_name)
                handler_class = getattr(module, class_name)
                
                # Istanziazione con Dependency Injection della configurazione
                new_handler = handler_class(h_conf.get("parameters", {}))
                print(f"   Link -> Added {class_name}")

                # Costruzione della lista linkata (Linked List)
                if first_handler is None:
                    first_handler = new_handler
                else:
                    current_handler.set_next(new_handler)
                
                current_handler = new_handler

            except Exception as e:
                print(f" [FACTORY ERROR] Loading handler {class_name}: {e}")
                raise e
        
        print("✅ Chain Built Successfully.\n")
        return first_handler