from langchain_core.documents import Document
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os, re
class DataHandler():
    def __init__(self, folder_path: str = None, texts: list[str] = None,chunk_size: int = 200, overlap_size: int = 50):
        self.folder_path = folder_path
        self.texts = texts
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
    
    def convert_texts_to_docs(self) -> list[Document]:
        """
        将`texts`转换为`Document`对象。
        """
        docs = []
        for text in self.texts:
            doc = Document(page_content=text)
            doc = self.clean_data(doc)
            docs.append(doc)
        return docs
    
    def load_docs(self):
        texts = []
        if self.texts:
            texts = self.convert_texts_to_docs()
        else:
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

        return texts
    
    def data_process(self):
        """
        加载`folder_path`路径下所有文件（或从给定的文本构造`Document`对象），并使用`text_splitter`进行文本分割。
        """

        texts = self.load_docs()
    
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap  = self.overlap_size
        )
        split_docs = text_splitter.split_documents(texts)
        return split_docs
    
if __name__ == "__main__":
    # folder = 'RAG\\data'
    # processor = DataHandler(folder, chunk_size=100, overlap_size=20)
    # docs = processor.data_process()
    # print(f"文本被分割为{len(docs)}个文本块")
    # for doc in docs:
    #     print(doc.page_content)
    #     print('-' * 20)

    texts = ['明黄色缎地平金银彩绣五毒活计，清同治，清宫旧藏。清代满族习俗，特别喜爱在腰带或领襟之间的钮扣上佩挂各类日常随手可用的小杂品，如荷包、扇套、表套、搬指套、香囊、眼镜盒、褡裢、槟榔袋、钥匙袋、靴掖等，通称“活计”。这些活计既很实用，装饰性也很强，并往往根据节庆时令的变化而佩挂纹样形制不同的活计。这套活计是端午节佩戴之物，共9件，其中荷包3件、烟荷包1件、表套1件、扇套1件、镜子1件、粉盒1件、名姓片套1件。每件的颜色和纹样相同，均为明黄色，通体以金线、银线和五彩丝线绣五毒和“大吉”葫芦纹。“五毒”为蛇、蟾蜍、蝎子、壁虎和蜈蚣五种有毒动物，配以“大吉”字样和葫芦纹样相组合，寓意以毒攻毒，以恶镇恶，驱邪免灾。整套活计用色明快华丽，纹样生动逼真，绣工精美细巧，为佩挂者平添仪态之美，同时也寄托了佩挂者希冀籍此避邪趋吉的美好愿望。',
             '清文竹镂空两层海棠式盒高：14.5cm，纵：22cm，宽：15.5cm。清文竹镂空两层海棠式盒【文物现状】现藏北京故宫博物院【简介】盒呈长圆海棠式，分两层，其上层与盖子母口扣合，平底，圈足较浅。木胎，贴黄达三重，通体饰变形夔纹，阳起较明显。此盒不同凡响之处在其罩架。罩架为随形海棠式，以紫檀镂空而成。罩面图案及架缘均镶以竹黄，而竹黄边沿所起阳线及花牙则保留紫檀本色，紫檀凝重，竹黄柔和，二者相辅相成，增其雅洁之气。此盒包镶技术精湛，尤其是罩架应用大面积镂空，难度高，耗工巨，足见当时工艺之发达。清代宫廷工艺技术是我国古代工艺技术史上集大成的时期，既有继承又有创新，达到了一个空前的高度，但由于过分重视技巧，往往流于卖弄，格调欠高。此件海棠式盒则不仅技巧高超，而且气质不俗，在清代工艺品中是罕见的。']
    processor = DataHandler(texts=texts, chunk_size=100, overlap_size=20)
    docs = processor.data_process()
    print(f"文本被分割为{len(docs)}个文本块")
    for doc in docs:
        print(doc.page_content)
        print('-' * 20)