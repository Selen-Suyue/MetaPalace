from langchain.embeddings.base import Embeddings
from langchain.pydantic_v1 import BaseModel, root_validator

from typing import Dict, List
from FlagEmbedding import FlagModel

MODEL_PATH = 'RAG\\models\\bge-small-zh-v1.5'

class MetaPalaceEmbedding(BaseModel, Embeddings):
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        values['model'] = FlagModel(
            model_name_or_path=MODEL_PATH,
            query_instruction_for_retrieval='为这个句子生成表示以用于检索相关文章：',
            use_fp16=True
        )
        return values

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]
    
if __name__ == '__main__':
    embedding_model = MetaPalaceEmbedding()
    print(embedding_model.embed_query('龙泉窑青釉带盖执壶'))