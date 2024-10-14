from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from typing import List
from RagHelpers.IngestionHelper import load_text_documents, load_pdf_documents, load_pdf_document, split_documents
from RagHelpers.EmbeddingHelper import create_vectors, add_vectors, similarity_search, load_vectors
from RagHelpers.Retreiver import get_response
from os import path
import os

router = APIRouter()

class QueryRequest(BaseModel):
    user_type: str
    query: str

class QueryResponse(BaseModel):
    response: str
    context: List

@router.post("/rag-query", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    # Placeholder for RAG implementation
    # You would replace this with your actual RAG logic
    query = request.query
    user_type = request.user_type
    response = get_response(query, user_type)
    results = response  # Dummy results
    return QueryResponse(response=results["response"], context=results["context"])

@router.post("/add-files-to-docstore")
async def uploadfile(file: UploadFile):
    # Read files and save it in Docs folder
    doc_folder = path.join(path.dirname(__file__), "../Docs")
    try:
        with open(path.join(doc_folder, file.filename), "wb") as f:
            f.write(file.file.read())
        if file.filename.endswith(".pdf"):
            documents = load_pdf_document(path.join(doc_folder, file.filename))     
          
        return {"status": "success", "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/load-documents")
async def load_documents():
    # Load all documents from the Docs folder
    doc_folder = path.join(path.dirname(__file__), "..Docs")
    try:
        text_docs = load_text_documents()
        pdf_docs = load_pdf_documents()
        text_docs.extend(pdf_docs)
        create_vectors(text_docs)
        return {"status": "success", "message": "Documents loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health-check")
async def health_check():
    return {"status": "ok"}