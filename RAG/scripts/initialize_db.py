import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from langchain_vector_store import LangchainVectorStoreManager

from RAG.models.data_handler import DataHandler

DATA_PATH = './RAG/data'
COLLECTION_NAME = 'Relics'

def initialize_db(collection_name: str = COLLECTION_NAME):
    """
        Initialize the database with the collection name. Please be careful when using this function.\
        The default data path is 'RAG\\data', and the default collection name is 'Relics'.
    """
    manager = LangchainVectorStoreManager()
    qdrant_manager = manager.get_qdrant_manager()
    if qdrant_manager.is_collection_exists(collection_name):
        qdrant_manager.delete_collection(collection_name)

    qdrant_manager.create_collection(collection_name, 512)

    vector_db = manager.get_vector_db_from_collection(collection_name)

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

def identify_to_initialize_db(collection_name: str = COLLECTION_NAME):
    print(f'Do you want to initialize the database with the collection name "{collection_name}"? (y/n)')
    answer = input()
    if answer == 'y':
        initialize_db(collection_name)
    else:
        print('Database initialization cancelled.')

if __name__ == '__main__':
    identify_to_initialize_db(collection_name='Relics')