import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse
from src.core.chain_factory import ChainFactory

app = FastAPI(title="Adversarial Gateway")

CONFIG_PATH = "config/settings.json"
# Singleton instance della catena
security_chain = None

@app.on_event("startup")
async def startup_event():
    """
    Hook di avvio: Costruisce la catena una sola volta all'avvio del server.
    """
    global security_chain
    try:
        security_chain = ChainFactory.create_chain(CONFIG_PATH)
    except Exception as e:
        print(f"Critical Error: {e}")

@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    """
    Endpoint principale (Facade).
    Riceve la richiesta raw e la converte in un Context Object per la catena.
    """
    global security_chain
    if not security_chain:
        raise HTTPException(status_code=500, detail="Security chain down")

    content = await file.read()
    
    # [CONTEXT OBJECT]
    # Incapsuliamo tutti i dati necessari (header, ip, file) in un dizionario
    # che viaggerà attraverso tutti gli handler senza accoppiamento stretto.
    context = {
        "client_ip": request.client.host,
        "headers": request.headers,
        "file_metadata": {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        },
        "image_data": content
    }

    # Avvio esecuzione Chain of Responsibility
    result = security_chain.handle(context)

    if not result:
        return JSONResponse({"error": "No result"}, status_code=500)
    
    # Mapping dello status code in base alla risposta della catena
    status = result.get("status_code", 200)
    return JSONResponse(content=result, status_code=status)

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)