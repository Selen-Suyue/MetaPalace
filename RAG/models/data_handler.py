from langchain_core.documents import Document
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, re, sys

class DataHandler():
    def __init__(self, folder_path: str, chunk_size: int = 200, overlap_size: int = 50):
        self.folder_path = folder_path
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def get_file_paths(self):
        """
        获取`folder_path`路径下所有文件的路径。
        """

        file_paths = []
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        return file_paths
    
    def clean_data(self, single_doc: Document = None):
        """
        清洗文本数据。
        """
        content = single_doc.page_content
        default_pattern = re.compile(r'[^\u4e00-\u9fff](\n)[^\u4e00-\u9fff]', re.DOTALL)
        new_content = re.sub(default_pattern, lambda match: match.group(0).replace('\n', ''), content)
        single_doc.page_content = new_content
        return single_doc
    
    def data_process(self):
        """
        加载`folder_path`路径下所有文件，并使用`text_splitter`进行文本分割。
        """

        file_paths = self.get_file_paths()

        loaders = []
        for file_path in file_paths:
            filetype = file_path.split('.')[-1]
            if filetype == 'pdf':
                loader = PyMuPDFLoader(file_path)
            elif filetype == 'txt':
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                return ValueError(f"Unsupported file type: {filetype}")
            loaders.append(loader)
        
        texts = []
        for loader in loaders:
            text = []
            for page in loader.load():
                page_content = self.clean_data(page)
                text.append(page_content)
            texts.extend(text)

    
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap  = self.overlap_size
        )
        split_docs = text_splitter.split_documents(texts)
        return split_docs
    
if __name__ == "__main__":
    folder = 'RAG\\data'
    processor = DataHandler(folder, chunk_size=100, overlap_size=20)
    docs = processor.data_process()
    print(f"文本被分割为{len(docs)}个文本块")
    for doc in docs:
        print(doc.page_content)
        print('-' * 20)