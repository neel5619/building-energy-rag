import os
import chromadb


def create_vector_store(chunks, db_dir="data/chroma_db", collection_name="building_energy"):
    """Create a ChromaDB vector store from document chunks."""

    # Create ChromaDB client (uses built-in default embeddings)
    client = chromadb.PersistentClient(path=db_dir)

    # Delete old collection if exists
    try:
        client.delete_collection(collection_name)
        print("Deleted old collection.")
    except:
        pass

    # Create new collection (ChromaDB default embedding handles multilingual)
    collection = client.get_or_create_collection(
        name=collection_name,
    )

    # Add chunks in batches
    batch_size = 100
    total = len(chunks)

    print(f"Embedding {total} chunks into vector database...")
    print(f"This may take a few minutes on first run...\n")

    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]

        collection.add(
            documents=[c["content"] for c in batch],
            metadatas=[{"source_file": c["source_file"], "page": c["page"]} for c in batch],
            ids=[f"chunk_{i + j}" for j in range(len(batch))],
        )

        progress = min(i + batch_size, total)
        print(f"  Progress: {progress}/{total} chunks ({int(progress / total * 100)}%)")

    print(f"\nDone! Vector database saved to: {db_dir}/")
    print(f"Collection '{collection_name}' has {collection.count()} chunks")
    return collection


def load_vector_store(db_dir="data/chroma_db", collection_name="building_energy"):
    """Load an existing vector store."""
    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_collection(name=collection_name)
    print(f"Loaded vector store: {collection.count()} chunks")
    return collection


def search(collection, query, n_results=5):
    """Search the vector store."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )
    return results


if __name__ == "__main__":
    from src.ingestion.pdf_loader import load_pdfs, chunk_documents

    docs = load_pdfs()
    chunks = chunk_documents(docs)

    # Create vector store
    collection = create_vector_store(chunks)

    # Test search
    print("\n--- Test Search ---")
    test_queries = [
        "What is the maximum U-value for exterior walls?",
        "Welche Förderung gibt es für Wärmepumpen?",
        "What are the requirements for zero-emission buildings?",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = search(collection, query, n_results=2)

        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            print(f"  Result {i + 1}: [{meta['source_file']} p.{meta['page']}]")
            print(f"    {doc[:150]}...")