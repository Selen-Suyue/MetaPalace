import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from langchain_qdrant import QdrantVectorStore
from RAG.models.bge_embedding import MetaPalaceEmbedding
from RAG.models.qdrant_db_manager import QdrantManager

client = QdrantManager().client
embedding_model = MetaPalaceEmbedding()

qdrant_db = QdrantVectorStore(
    client=client,
    collection_name='test_collection',
    embedding=embedding_model
)

qdrant_db.add_texts(
    texts=[
        '你好',
        '你好，世界'
    ]
)
print('Added texts to Qdrant DB.')

docs = qdrant_db.similarity_search(
    query='你好',
    k=2
)
print('Similarity search results:', docs)