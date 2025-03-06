import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from langchain_qdrant import QdrantVectorStore
from langchain.embeddings.base import Embeddings
from RAG.models.bge_embedding import MetaPalaceEmbedding
from RAG.models.qdrant_db_manager import QdrantManager

EMBEDDING_MODEL = MetaPalaceEmbedding()
# Max token limit for the conversation storage.
MAX_TOKEN_LIMIT = 1000

class LangchainVectorStoreManager:
    """
        To implement the vector store manager for Langchain use.
    """
    def __init__(self):
        self.manager = QdrantManager()
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