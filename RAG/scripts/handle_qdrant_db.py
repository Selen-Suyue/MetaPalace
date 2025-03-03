import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from langchain_qdrant import QdrantVectorStore
from RAG.models.bge_embedding import MetaPalaceEmbedding
from RAG.models.qdrant_db_manager import QdrantManager
from RAG.models.data_handler import DataHandler

DATA_PATH = 'RAG\\data'
COLLECTION_NAME = 'Relics'
EMBEDDING_MODEL = MetaPalaceEmbedding()

qdrant_manager = QdrantManager()

def initialize_db():
    qdrant_manager.create_collection(COLLECTION_NAME, 512)

    client = qdrant_manager.client
    vector_db = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=EMBEDDING_MODEL
    )

    data_handler = DataHandler(
        folder_path=DATA_PATH,
        chunk_size=100,
        overlap_size=30
    )

    docs = data_handler.data_process()

    vector_db.add_texts(
        texts=[
            doc.page_content for doc in docs
        ]
    )

def get_vector_db():
    client = qdrant_manager.client
    vector_db = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=EMBEDDING_MODEL
    )
    return vector_db

if __name__ == '__main__':
    initialize_db()