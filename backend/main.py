from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
from services import process_pdf, get_answer_from_pdf
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/documents/", response_model=List[schemas.Document])
async def get_documents(db: Session = Depends(get_db)):
    print("Fetching documents from database...")  # Debug log
    documents = db.query(models.Document).all()
    print(f"Found {len(documents)} documents")  # Debug log
    return documents

@app.post("/upload-pdf/", response_model=schemas.Document)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print(f"Uploading file: {file.filename}")  # Debug log
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    file_path = os.path.join("pdfs", file.filename)
    os.makedirs("pdfs", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    text_content = process_pdf(file_path)
    db_document = models.Document(
        filename=file.filename,
        filepath=file_path,
        content=text_content
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    print(f"Successfully uploaded document with ID: {db_document.id}")  # Debug log
    return db_document

@app.post("/ask-question/", response_model=schemas.Answer)
async def ask_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == question.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    answer = get_answer_from_pdf(document.content, question.question)
    
    db_answer = models.Answer(
        question=question.question,
        answer=answer,
        document_id=document.id
    )
    db.add(db_answer)
    db.commit()
    
    return db_answer

@app.get("/documents/{document_id}", response_model=schemas.Document)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if document:
        return document
    
    # Add logging to help diagnose
    print(f"Available documents: {[doc.id for doc in db.query(models.Document).all()]}")
    raise HTTPException(
        status_code=404, 
        detail=f"Document {document_id} not found. Please ensure the document was uploaded successfully."
    )
