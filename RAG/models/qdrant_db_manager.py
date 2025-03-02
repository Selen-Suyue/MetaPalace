from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Initialize the Qdrant database with the given path locally.
DB_PERSISTENCE_PATH = "RAG\\db\\qdrant"
class QdrantManager:
    def __init__(self, db_persistence_path: str = DB_PERSISTENCE_PATH):
        self.db_persistence_path = db_persistence_path
        self.client = QdrantClient(path=self.db_persistence_path)

    def create_collection(self, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE):
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name, 
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance
                )
            )
        else:
            print(f"Collection {collection_name} already exists.")

    def upsert_points(self, collection_name: str, points: list[PointStruct]):
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

if __name__ == '__main__':
    import numpy as np
    manager = QdrantManager()
    manager.create_collection("test_collection", 512)

    vectors = np.random.rand(10, 512)
    manager.upsert_points(
        collection_name='test_collection',
        points=[
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload={"title": f"Title {idx}"}
            )
            for idx, vector in enumerate(vectors)
        ]
    )

    query_vector = np.random.rand(512)
    search_results = manager.client.query_points(
        collection_name='test_collection',
        query=query_vector,
        limit=3
    )
    print(search_results)