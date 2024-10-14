from fastapi import FastAPI
import uvicorn
from Routers.RagEndpoints import router as rag_router
import dotenv

dotenv.load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API for ProviTax Assistant"}

app.include_router(rag_router, prefix="/rag", tags=["rag"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)