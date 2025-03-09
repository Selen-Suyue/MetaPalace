import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from langchain_qdrant import QdrantVectorStore
from langchain.embeddings.base import Embeddings
from RAG.models.bge_embedding import MetaPalaceEmbedding
from RAG.models.qdrant_db_manager import QdrantManager

EMBEDDING_MODEL = MetaPalaceEmbedding()
DB_PERSISTENCE_PATH = "./RAG/db/qdrant"

class LangchainVectorStoreManager:
    """
        To implement the vector store manager for Langchain use.
    """
    def __init__(self, db_path: str = DB_PERSISTENCE_PATH):
        self.manager = QdrantManager(db_persistence_path=db_path)
        self.client = self.manager.client

    def get_qdrant_manager(self):
        return self.manager

    def get_vector_db_from_collection(self, collection_name: str, embedding: Embeddings = EMBEDDING_MODEL):
        """
            Get vector db from collection. The default embedding is MetaPalaceEmbedding(self-implemented).
        """
        vector_db = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=embedding
        )
        return vector_db
    
if __name__ == '__main__':
    manager = LangchainVectorStoreManager()
    try:
        vector_db = manager.get_vector_db_from_collection('Relics')
    except Exception as e:
        print(e)