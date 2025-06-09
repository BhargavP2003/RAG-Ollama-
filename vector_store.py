from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self):
        # Using a smaller, faster model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.metadata = []
        self.embeddings = None

    def add_documents(self, documents: List[str], metadata: Dict[str, Any] = None):
        # Get embeddings
        self.embeddings = self.model.encode(documents)
        self.documents = documents
        # Store metadata for each document
        if metadata:
            self.metadata = [metadata] * len(documents)
        else:
            self.metadata = [{}] * len(documents)

    def similarity_search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        if not self.documents:
            return []
        
        # Get query embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k documents
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        # Return relevant documents with metadata
        return [{
            "text": self.documents[i],
            "metadata": self.metadata[i]
        } for i in top_k_indices] 