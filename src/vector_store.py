import json
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize ChromaDB client with persistent local storage
chroma_client = chromadb.PersistentClient(path="data/chroma_db")

# 2. Load a fast, local embedding model (downloads automatically on first run)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Create or access the database collection
collection = chroma_client.get_or_create_collection(
    name="clinvar_knowledge",
    embedding_function=sentence_transformer_ef
)

def load_knowledge_base(json_path="data/clinvar_kb.json"):
    """Reads the JSON and embeds the clinical text into the vector database."""
    with open(json_path, 'r') as f:
        kb_data = json.load(f)
    
    ids = []
    documents = []
    metadatas = []
    
    for item in kb_data:
        ids.append(item["id"])
        documents.append(item["evidence"])
        metadatas.append({"gene": item["gene"], "classification": item["classification"]})
        
    # Upsert inserts new records or updates existing ones
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Successfully embedded and loaded {len(kb_data)} clinical records into ChromaDB.")

def query_variant_evidence(variant_id):
    """Retrieves the most clinically relevant text for a variant coordinate."""
    results = collection.query(
        query_texts=[variant_id], 
        n_results=1
    )
    
    # If the database finds a matching document, return it
    if results['documents'] and results['documents'][0]:
        return {
            "evidence": results['documents'][0][0],
            "metadata": results['metadatas'][0][0]
        }
    return None

if __name__ == "__main__":
    # When you run this script directly, it will build the database
    load_knowledge_base()
