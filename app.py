import os
import pdfplumber
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def root():
    return FileResponse("static/index.html")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # API key pulled from .env
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("notes")

def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

@app.post("/upload")
async def upload(file: UploadFile):
    # save file temporarily
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    # parse text
    text = parse_pdf(path)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    # embed and store
    for i, chunk in enumerate(chunks):
        emb = client.embeddings.create(
            model="text-embedding-3-small", 
            input=chunk
        ).data[0].embedding
        collection.add(
            documents=[chunk], 
            embeddings=[emb], 
            ids=[f"{file.filename}_{i}"]
        )
    return {"status": "uploaded", "chunks": len(chunks)}

@app.post("/ask")
async def ask(question: str = Form(...)):
    # embed query
    q_emb = client.embeddings.create(
        model="text-embedding-3-small", 
        input=question
    ).data[0].embedding
    
    results = collection.query(query_embeddings=[q_emb], n_results=3)
    
    if not results["documents"][0]:
        return {"answer": "I could not find this in your notes."}
    
    context = "\n\n".join(results["documents"][0])
    
    prompt = f"""
    Answer the question using ONLY the context below.
    If the answer is not there, say: 'I could not find this in your notes.'

    Context:
    {context}

    Question: {question}
    Answer:
    """
    
    answer = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"answer": answer.choices[0].message.content}
