import os
from pypdf import PdfReader


def load_pdfs(data_dir="data/raw"):
    """Load all PDFs from the data directory."""
    documents = []
    pdf_files = [f for f in os.listdir(data_dir) if f.endswith(".pdf")]

    print(f"Found {len(pdf_files)} PDF files:")
    for pdf_file in sorted(pdf_files):
        filepath = os.path.join(data_dir, pdf_file)
        print(f"  Loading: {pdf_file}...")
        try:
            reader = PdfReader(filepath)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    documents.append({
                        "content": text,
                        "source_file": pdf_file,
                        "page": i + 1,
                    })
            print(f"    → {len(reader.pages)} pages loaded")
        except Exception as e:
            print(f"    → ERROR: {e}")

    print(f"\nTotal: {len(documents)} pages from {len(pdf_files)} PDFs")
    return documents


def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks."""
    chunks = []

    for doc in documents:
        text = doc["content"]
        # Split text into chunks with overlap
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "content": chunk_text,
                    "source_file": doc["source_file"],
                    "page": doc["page"],
                })

            start += chunk_size - chunk_overlap

    print(f"Split {len(documents)} pages into {len(chunks)} chunks")
    print(f"  Chunk size: {chunk_size} characters")
    print(f"  Overlap: {chunk_overlap} characters")
    return chunks


if __name__ == "__main__":
    docs = load_pdfs()
    chunks = chunk_documents(docs)

    if chunks:
        print("\n--- Sample Chunk ---")
        print(f"Source: {chunks[0]['source_file']}")
        print(f"Page: {chunks[0]['page']}")
        print(f"Content: {chunks[0]['content'][:300]}...")