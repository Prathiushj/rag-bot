# 📚 RAG Bot — Personal Notes Assistant

A smart document assistant that lets you query your PDF notes 
using natural language. Built with FastAPI and ChromaDB.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn
- **AI/LLM:** OpenAI API
- **Vector Store:** ChromaDB (DuckDB)
- **PDF Parsing:** pdfplumber
- **Other:** python-dotenv, python-multipart

## ✨ Features
- Upload PDF notes and ask questions in plain English
- Uses Retrieval-Augmented Generation (RAG) for accurate answers
- Fast vector search with ChromaDB

## 🚀 Getting Started
1. Clone the repo
2. Create a `.env` file and add your `OPENAI_API_KEY`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`

## 💡 Use Case
Built to help students query academic notes efficiently 
without scrolling through lengthy PDFs.
