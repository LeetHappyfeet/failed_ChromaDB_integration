# embedding.py

import os
from sentence_transformers import SentenceTransformer

model_name = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
model = SentenceTransformer(model_name)

def embed_text(text):
    """
    Embed the input text string using SentenceTransformer.
    Returns a list of floats representing the vector.
    """
    try:
        return model.encode(text).tolist()
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}")
        return None
