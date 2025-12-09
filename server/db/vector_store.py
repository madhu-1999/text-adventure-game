from datetime import timezone, datetime
import os
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from typing import Any, List, Dict, Optional
import json

from server.src.exceptions import DatabaseError 

BASE_DIR = Path(__file__).resolve().parent.parent  # server/ directory
ENV_PATH = BASE_DIR / ".env"

# Read db url from .env file
DATABASE_URL = os.getenv("VECTOR_STORE_URL", '')

class VectorStore:
    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(path=DATABASE_URL)
        self.story_collection = self.client.get_or_create_collection(name="story_settings")
        self.embedding_fn = DefaultEmbeddingFunction()


    def add_story_settings(self, story_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        metadata = metadata or {}
        metadata = {**metadata, "story_id": story_id, "created_at": datetime.now(timezone.utc).isoformat()}
        emb = self.embedding_fn([text])
        try:
            self.story_collection.add(ids=[story_id], documents=[text], metadatas=[metadata], embeddings=emb)
        except Exception:
            raise DatabaseError("Could not save to vector store!")
        
    def query_similar(self, query_text: str, n_results: int = 5):
        emb = self.embedding_fn([query_text])
        return self.story_collection.query(query_embeddings=emb, n_results=n_results, include=["documents", "metadatas", "distances"])
    
