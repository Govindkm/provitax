from fastapi import FastAPI
from Routers.RagEndpoints import router as rag_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API for ProviTax Assistant"}

app.include_router(rag_router, prefix="/rag", tags=["rag"])