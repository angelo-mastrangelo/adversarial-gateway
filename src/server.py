from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime

# Inizializza l'app
app = FastAPI(
    title="Software Architecture Assignment API",
    description="Implementazione reale dei pattern Adapter, Observer, Decorator e Strategy",
    version="1.0.0"
)

# ==========================================
# 1. ADAPTER PATTERN (Payment + SECURITY TRICK)
# ==========================================

# Modello dati per Swagger
class PaymentRequest(BaseModel):
    amount: float
    currency: str
    provider: str
    description: Optional[str] = "Payment transaction"

# Target Interface (Implied)
class IPaymentProcessor:
    def process_payment(self, amount: float, currency: str) -> dict:
        pass

# Adaptee (Simulazione servizio esterno)
class PayFastService:
    def send_raw_data(self, data: bytes):
        return "PayFast_TXN_123"

# Adapter
class PayFastAdapter(IPaymentProcessor):
    def __init__(self):
        self.service = PayFastService()
    
    def process_payment(self, amount: float, currency: str) -> dict:
        # Logica di adattamento: float -> bytes
        raw_data = f"{amount}|{currency}".encode('utf-8')
        txn_id = self.service.send_raw_data(raw_data)
        return {"provider": "PayFast", "status": "success", "txn_id": txn_id}

@app.post("/api/payment", tags=["Exercise 1 - Adapter & Security"])
def process_payment(request: PaymentRequest):
    # --- INIZIO TRUCCO PER REPORT (SECURITY CHECK) ---
    # Convertiamo l'intera richiesta in stringa per cercare script malevoli ovunque
    request_str = str(request.dict())
    if "<script>" in request_str:
        print(f"ATTACCO RILEVATO: {request_str}") # Log su terminale per debug
        raise HTTPException(status_code=400, detail="Security Alert: XSS Injection Detected by Gateway")
    # --- FINE TRUCCO ---

    # --- LOGICA ADAPTER ---
    if request.provider.lower() == "payfast":
        adapter = PayFastAdapter()
        return adapter.process_payment(request.amount, request.currency)
    else:
        return {"status": "mock_success", "provider": request.provider, "note": "Adapter not implemented for this demo"}


# ==========================================
# 2. OBSERVER PATTERN (Social)
# ==========================================
class PostRequest(BaseModel):
    user_id: str
    content: str

class IObserver:
    def update(self, post_content: str):
        pass

class Follower(IObserver):
    def __init__(self, name: str, method: str):
        self.name = name
        self.method = method
    
    def update(self, post_content: str):
        return f"Notified {self.name} via {self.method}"

class Publisher:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: IObserver):
        self.observers.append(observer)
    
    def notify(self, content: str):
        logs = []
        for observer in self.observers:
            logs.append(observer.update(content))
        return logs

@app.post("/social/publish", tags=["Exercise 2 - Observer"])
def publish_post(request: PostRequest):
    # Setup dinamico
    pub = Publisher()
    pub.attach(Follower("Mario", "PUSH"))
    pub.attach(Follower("Luigi", "EMAIL"))
    
    # Azione
    logs = pub.notify(request.content)
    
    return {
        "status": "published", 
        "post_id": 8492, 
        "observers_count": len(logs),
        "delivery_report": logs
    }


# ==========================================
# 3. DECORATOR PATTERN (Coffee Shop)
# ==========================================
class OrderRequest(BaseModel):
    base: str
    addons: List[str]

# Component
class Beverage:
    def cost(self): return 0.0
    def description(self): return ""

# Concrete Component
class Espresso(Beverage):
    def cost(self): return 1.00
    def description(self): return "Espresso"

# Decorators
class IngredientDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self.beverage = beverage

class Milk(IngredientDecorator):
    def cost(self): return self.beverage.cost() + 0.50
    def description(self): return self.beverage.description() + ", Milk"

class Chocolate(IngredientDecorator):
    def cost(self): return self.beverage.cost() + 0.70
    def description(self): return self.beverage.description() + ", Chocolate"

@app.post("/cafe/order", tags=["Exercise 3 - Decorator"])
def create_order(request: OrderRequest):
    # Base
    drink = Espresso() # Default per semplicità
    
    # Wrapping dinamico
    for addon in request.addons:
        if addon.lower() == "milk":
            drink = Milk(drink)
        elif addon.lower() == "chocolate":
            drink = Chocolate(drink)
            
    return {
        "description": drink.description(),
        "total_cost": round(drink.cost(), 2)
    }


# ==========================================
# 4. STRATEGY PATTERN (Navigation)
# ==========================================
class RouteRequest(BaseModel):
    start: str
    end: str
    preference: str

# Strategy Interface
class IRouteStrategy:
    def calculate(self, a, b): pass

# Concrete Strategies
class FastestStrategy(IRouteStrategy):
    def calculate(self, a, b):
        return {"time": "15 min", "distance": "10 km", "type": "Fastest via Highway"}

class ScenicStrategy(IRouteStrategy):
    def calculate(self, a, b):
        return {"time": "45 min", "distance": "12 km", "type": "Scenic via Coast"}

@app.post("/routes/find", tags=["Exercise 4 - Strategy"])
def find_route(request: RouteRequest):
    # Context Logic
    strategy = None
    if request.preference == "fastest":
        strategy = FastestStrategy()
    elif request.preference == "scenic":
        strategy = ScenicStrategy()
    else:
        # Default
        strategy = FastestStrategy()
    
    result = strategy.calculate(request.start, request.end)
    return {
        "strategy_used": strategy.__class__.__name__,
        "route": result
    }