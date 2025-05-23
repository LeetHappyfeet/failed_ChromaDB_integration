# main.py

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="Worker.env")
from datetime import datetime
from chroma_client import get_or_create_agent_collection, insert_memory_to_chroma
from embedding import embed_text
from db import get_unindexed_memories, mark_as_indexed, connect_db

# Load environment variables
load_dotenv()

def main():
    print("[INFO] Starting Chroma Indexing Worker...")

    conn, cursor = connect_db()

    # Fetch unindexed memories
    records = get_unindexed_memories(cursor, limit=100)
    if not records:
        print("[INFO] No unindexed memory records found.")
        return

    print(f"[INFO] Found {len(records)} unindexed records.")

    for rec in records:
        rec_id, character_id, user_id, timestamp, rdf_blob = rec

        # Validate input
        if not rdf_blob or not character_id:
            print(f"[WARN] Skipping record {rec_id} due to missing data.")
            continue

        agent_id = character_id
        memory_id = f"mem_{rec_id}"
        memory_text = rdf_blob.strip()

        embedding = embed_text(memory_text)
        if embedding is None:
            print(f"[ERROR] Embedding failed for record {rec_id}")
            continue

        # Build memory document
        memory_doc = {
            "id": memory_id,
            "text": memory_text,
            "agent_id": agent_id,
            "user_ids": [user_id] if user_id else [],
            "conversation_id": "default",  # Optional: replace later
            "timestamp": timestamp.isoformat(),
            "tags": ["indexed", "rdf_blob"]
        }

        try:
            collection = get_or_create_agent_collection(agent_id)
            insert_memory_to_chroma(collection, memory_doc, embedding)
            mark_as_indexed(cursor, conn, rec_id)
            print(f"[OK] Indexed record {rec_id} into Chroma for {agent_id}")
        except Exception as e:
            print(f"[ERROR] Failed to index record {rec_id}: {e}")

    cursor.close()
    conn.close()
    print("[INFO] Chroma Indexing Worker completed.")

if __name__ == "__main__":
    main()
