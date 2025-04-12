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

def update_db(folder_path: str = None, texts: list[str] = None, collection_name: str = COLLECTION_NAME, manager: LangchainVectorStoreManager = None):
    if manager is None:
        print('Please initialize the database manager first.')

    vector_db = manager.get_vector_db_from_collection(collection_name)
    data_handler = DataHandler(
        folder_path=folder_path,
        texts=texts,
        chunk_size=100,
        overlap_size=30
    )

    docs = data_handler.data_process()

    vector_db.add_texts(
        texts=[
            doc.page_content for doc in docs
        ]
    )

if __name__ == '__main__':
    # identify_to_initialize_db(collection_name='Relics')
    texts = ['明黄色缎地平金银彩绣五毒活计，清同治，清宫旧藏。清代满族习俗，特别喜爱在腰带或领襟之间的钮扣上佩挂各类日常随手可用的小杂品，如荷包、扇套、表套、搬指套、香囊、眼镜盒、褡裢、槟榔袋、钥匙袋、靴掖等，通称“活计”。这些活计既很实用，装饰性也很强，并往往根据节庆时令的变化而佩挂纹样形制不同的活计。这套活计是端午节佩戴之物，共9件，其中荷包3件、烟荷包1件、表套1件、扇套1件、镜子1件、粉盒1件、名姓片套1件。每件的颜色和纹样相同，均为明黄色，通体以金线、银线和五彩丝线绣五毒和“大吉”葫芦纹。“五毒”为蛇、蟾蜍、蝎子、壁虎和蜈蚣五种有毒动物，配以“大吉”字样和葫芦纹样相组合，寓意以毒攻毒，以恶镇恶，驱邪免灾。整套活计用色明快华丽，纹样生动逼真，绣工精美细巧，为佩挂者平添仪态之美，同时也寄托了佩挂者希冀籍此避邪趋吉的美好愿望。']
    collection = 'test_collection'
    manager = LangchainVectorStoreManager()
    update_db(texts=texts, collection_name=collection, manager=manager)