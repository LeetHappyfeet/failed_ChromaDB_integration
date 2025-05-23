# db.py

import os
import psycopg2
from datetime import datetime

def connect_db():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        database=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )
    cursor = conn.cursor()
    return conn, cursor

def get_unindexed_memories(cursor, limit=100):
    query = """
        SELECT id, character_id, user_id, timestamp, rdf_blob
        FROM memory_log
        WHERE is_indexed_chroma = FALSE
        ORDER BY timestamp ASC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def mark_as_indexed(cursor, conn, record_id):
    now = datetime.utcnow()
    update = """
        UPDATE memory_log
        SET is_indexed_chroma = TRUE,
            chroma_pass_time = %s
        WHERE id = %s;
    """
    cursor.execute(update, (now, record_id))
    conn.commit()
