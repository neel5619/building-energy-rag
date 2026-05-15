# 🏢 Building Energy Code RAG Assistant

An AI-powered search assistant that answers questions about German building energy regulations (GEG), EU directives (EPBD), and KfW subsidies — with source citations from the actual legal documents.

Built as a Retrieval-Augmented Generation (RAG) system that searches across 9 multilingual PDF documents (German + English) and generates accurate, cited answers using Google Gemini.

## 🎯 Why This Exists

Energy consultants and building engineers spend hours searching through hundreds of pages of regulations. This tool gives them the answer in seconds, with proof of where it came from.

## 🔧 Architecture
User Question
│
▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Streamlit   │───▶│  ChromaDB    │───▶│  Google      │
│  Frontend    │    │  Vector DB   │    │  Gemini API  │
│              │◀───│  (2844 chunks│◀───│  (Answer +   │
│  Display     │    │   from 9 PDFs│    │   Citations) │
└─────────────┘    └──────────────┘    └─────────────┘

## 📄 Documents Indexed

| Document | Language | Pages | Description |
|----------|----------|-------|-------------|
| GEG (Gebäudeenergiegesetz) | German | 89 | German Building Energy Act |
| GEG Novelle (Entwurf) | German | 172 | GEG Amendment Draft (65% renewables) |
| EU EPBD 2024/1275 | English | 68 | EU Energy Performance of Buildings Directive |
| KfW BEG Merkblatt | German | 32 | KfW Subsidy Guidelines |
| KfW BEG Förderfähige Maßnahmen | German | 39 | Eligible Renovation Measures |
| KfW BEG Technische FAQ | German | 113 | Technical FAQ for Efficient Buildings |
| EPBD Implementation Guide | English | 97 | Practical EPBD Implementation Guide |
| BEG Audit Report | German | 32 | Federal Audit of Building Subsidies |
| EPBD Factsheet | English | 8 | Summary of EPBD Requirements |

**Total: 649 pages → 2,844 searchable chunks**

## 🚀 Features

- **Bilingual search**: Ask in English or German — finds relevant chunks across both languages
- **Source citations**: Every answer includes document name and page number
- **9 PDF knowledge base**: Covers GEG, EPBD, KfW subsidies
- **Adjustable search depth**: Control how many sources to search (3-10)
- **Expandable sources**: View the original text chunks used for each answer
- **Dockerized**: Ready for deployment

## 🛠 Tech Stack

- **Python** — Core language
- **ChromaDB** — Vector database for semantic search
- **Google Gemini API** — LLM for answer generation
- **Streamlit** — Web frontend
- **PyPDF** — PDF text extraction
- **Docker** — Containerization

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/neel5619/building-energy-rag.git
cd building-energy-rag

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Build vector database (first time only)
python -m src.retrieval.vector_store

# Run the app
streamlit run frontend/app.py
```

## 📸 Screenshots

_Add screenshots of your app here_

## 📁 Project Structure

building-energy-rag/
├── data/
│   ├── raw/              # 9 PDF documents
│   └── chroma_db/        # Vector database (auto-generated)
├── src/
│   ├── ingestion/        # PDF loading and chunking
│   ├── retrieval/        # Vector store and search
│   ├── generation/       # Gemini LLM integration
│   └── api/              # FastAPI backend (optional)
├── frontend/             # Streamlit web app
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md