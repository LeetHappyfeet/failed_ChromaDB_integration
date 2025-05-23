# chroma_client.py

import os
import chromadb
from chromadb.config import Settings

# Create Chroma client with REST interface
chroma = chromadb.Client(
    Settings(
        chroma_api_impl="rest",
        chroma_server_host=os.getenv("CHROMA_HOST").replace("http://", "").replace("https://", ""),
        chroma_server_http_port=int(os.getenv("CHROMA_PORT", 8001))
    )
)

def get_or_create_agent_collection(agent_id):
    """
    Get or create a ChromaDB collection for a specific agent.
    """
    collection_name = f"{agent_id}_memories"
    existing = [col.name for col in chroma.list_collections()]
    if collection_name not in existing:
        print(f"[INFO] Creating new Chroma collection: {collection_name}")
        chroma.create_collection(name=collection_name)
    return chroma.get_collection(collection_name)

def insert_memory_to_chroma(collection, memory_doc, embedding):
    """
    Add a memory vector and metadata to the given collection.
    """
    collection.add(
        embeddings=[embedding],
        documents=[memory_doc["text"]],
        metadatas=[{
            "user_ids": memory_doc["user_ids"],
            "conversation_id": memory_doc["conversation_id"],
            "timestamp": memory_doc["timestamp"],
            "tags": memory_doc["tags"]
        }],
        ids=[memory_doc["id"]]
    )
