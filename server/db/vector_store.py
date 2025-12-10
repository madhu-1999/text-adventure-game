from datetime import timezone, datetime
import os
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from typing import Any, Dict, Optional

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
        self.chat_collection = self.client.get_or_create_collection(name="chat_history")
        self.embedding_fn = DefaultEmbeddingFunction()


    def add_story_settings(self, story_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Store generated story settings for later retrieval"""
        metadata = metadata or {}
        metadata = {**metadata, "story_id": story_id, "created_at": datetime.now(timezone.utc).isoformat()}
        emb = self.embedding_fn([text])
        try:
            self.story_collection.add(ids=[story_id], documents=[text], metadatas=[metadata], embeddings=emb)
        except Exception:
            raise DatabaseError("Could not save to vector store!")
    
    def add_chat_message(self, message_id: str, story_id: str, content:str, role: str, session_id: str, metadata: Optional[Dict[str, Any]] = None):
        """Store chat messages for context retrieval"""
        metadata = metadata or {}
        metadata = {**metadata, "story_id": story_id, "role": role, "session_id": session_id, "created_at": datetime.now(timezone.utc).isoformat()}
        emb = self.embedding_fn([content])
        self.chat_collection.add(ids=[message_id], documents=[content], metadatas=[metadata], embeddings=emb)

    def retrieve_context(self, story_id: str, session_id: str, query: str, n_results: int = 3) -> Dict[str, Any]:
        """RAG: Retrieve relevant settings + chat history for context"""
        # Get relevant story settings
        settings_results = self.story_collection.query(
            query_texts=[query],
            n_results=min(n_results, 2),
            where={"story_id": story_id}
        )
        
        # Get relevant chat history
        chat_results = self.chat_collection.query(
            query_texts=[query],
            n_results=n_results,
            where={
                "$and": [
                    {"story_id": story_id},
                    {"session_id": session_id}
                ]
            }
        )
        
        return {
            "settings": settings_results.get("documents", [[]]),
            "chat_history": chat_results.get("documents", [[]]),
            "settings_metadata": settings_results.get("metadatas", [[]]),
            "chat_metadata": chat_results.get("metadatas", [[]])
        }
