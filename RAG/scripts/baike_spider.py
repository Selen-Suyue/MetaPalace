from urllib import request,parse
from bs4 import BeautifulSoup
import ssl, time
import re

from get_proxy import get_proxy
from glob_assets_name import _get_assets_name
from file_handler import FileHandler, RestoreHandlerType
# The default restore policy for the spider.
DEFAULT_RESTORE_POLICY = RestoreHandlerType.SUPERADD

# Base url for the spider to crawl.
BASE_URL = 'https://baike.baidu.com/item/'

CALL_BACK_BASE_URL = 'https://www.baidu.com/s?wd='
# The folder path where the assets are stored.
ASSETS_PATH = 'Fig/*'
# Default encoding style for the html.
HTML_ECODE_STYLE = 'utf-8'
# Default user agent for the spider.
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
# Sleep time for the spider to avoid being blocked.
SLEEP_TIME = 1
# Retry times for the spider to search.
RETEY_TIMES = 3
# The depth of the spider to retrive the data.
RETRIVE_DEPTH = 1
# Time out for the spider to open the url.
TIME_OUT = 5
def url_builder(baseurl: str, keyname: str) -> str:
    return f'{baseurl}{parse.quote(keyname)}'

def headers_builder():
    return {
        'User-Agent': USER_AGENT
    }

def context_builder() -> ssl.SSLContext:
    return ssl._create_unverified_context()

def spider_use_request(keyname: str):
    rurl = url_builder(baseurl=BASE_URL, keyname=keyname)
    rheaders = headers_builder()
    context = context_builder()

    opener = request.build_opener(request.ProxyHandler({'http': get_proxy()}))
    req = request.Request(url=rurl, headers=rheaders, method='GET')
    try:
        r = opener.open(req, timeout=TIME_OUT)
        #r = request.urlopen(req, context=context)
        return r
    except Exception as e:
        print(f"\nWarning: faild to find {keyname} in Baidu Baike, unable to open the url.\n", e)
        return None

def build_bs4_matcher(html) -> BeautifulSoup:
    return BeautifulSoup(html, 'lxml')

def clean_text(text: str) -> str:
    cleaned_text = re.sub(r'\(.*', '', text)
    cleaned_text = re.sub(r'\[', '', cleaned_text)
    cleaned_text = re.sub(r'\]', '', cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


class SearchCallBackForNewNameProvider():
    """
    This class is used to get the supported name of the relic.
    """
    base_url = CALL_BACK_BASE_URL
    def __init__(self):
        self.r = None
        pass

    def headers_builder_google(self):
        return {
            'User-Agent': USER_AGENT
        }

    def get_relative_names(self, unsupported_name: str): 
        """
            Search for the relativave names Baidu Baike obtained.
        """
        self.block_texts = None
        print(f'\nSearching for {unsupported_name}...')
        time.sleep(SLEEP_TIME)
        url = url_builder(self.base_url, unsupported_name)
        headers = self.headers_builder_google()
        context = context_builder()

        opener = request.build_opener(request.ProxyHandler({'http': get_proxy()}))
        req = request.Request(url=url, headers=headers, method='GET')
        try:
            self.r = opener.open(req, timeout=TIME_OUT)
            #self.r = request.urlopen(req, context=context)
        except Exception as e:
            print(f"\nWarning: faild to get relative names of {unsupported_name} from Baidu Baike, unable to open the url.\n", e)
            return None
        try:
            self.soup = build_bs4_matcher(self.r.read().decode(HTML_ECODE_STYLE))
        except Exception as e:
            print("\nWarning: quit the too long reading of the html.\n", e)
            return None
        self.block_texts = self.soup.find_all(class_='c-title t')
        self.block_texts.extend(self.soup.find_all(class_='t kg-title_jwHUX tts-b-hl'))
        return self.convert_to_text()

    def convert_to_text(self) -> list:
        block_texts = build_bs4_matcher(str(self.block_texts)).text
        pattern = r'(\S+)\s?-\s?百度百科'
        matches = re.findall(pattern, block_texts)
        cleaned_matches = [clean_text(match) for match in matches]
        return cleaned_matches

class RelicsBaikeTextProvider():
    """
    This class is used to export all relative texts of the relics from the baike.baidu.com.
    """
    def __init__(self):
        self.r = None
        self.ecode_style = HTML_ECODE_STYLE
        self.soup = None
        self.block_texts = None
        self.text = None

    def get_relics_text(self, keyname: str) -> str:
        """
            Get the target html block from the web page.
            Args:
                `keyname`: The name of the relic.
            Returns:
                `text`: The target text block. 
        """
        self.r = spider_use_request(keyname)
        try:
            self.soup = build_bs4_matcher(self.r.read().decode(self.ecode_style))
        except Exception as e:
            print("\nWarning: quit the too long reading of the html.\n", e)
            return ''
        self.block_texts = self.soup.find_all(class_='para_gLUIg summary_By2fs MARK_MODULE')

        self.block_texts.extend(self.soup.find_all(class_='para_gLUIg content_hDxHU MARK_MODULE'))
        self.text = ''
        self.convert_to_text()
        return self.text
    
    def convert_to_text(self) -> str:
        for block_text in self.block_texts:
            self.text += block_text.text

# Initialize the search engine provider.
CALL_BACK_PROVIDER = SearchCallBackForNewNameProvider()
SINGLE_TEXT_PROVIDER = RelicsBaikeTextProvider()
# Initialize the file handler.
FILE_HANDLER = FileHandler()

class BaiduBaikeSpider():
    """
        This class is used to manage the baike.baidu.com spider to work.
    """
    def __init__(self, 
                 retry_times: int = RETEY_TIMES,
                 sleep_time: int = SLEEP_TIME,
                 retrive_depth: int = RETRIVE_DEPTH,
                 asset_names: list = _get_assets_name(ASSETS_PATH),
                 file_handler: FileHandler = FILE_HANDLER,
                 names_provider: SearchCallBackForNewNameProvider = CALL_BACK_PROVIDER, 
                 text_provider: RelicsBaikeTextProvider = SINGLE_TEXT_PROVIDER):
        self.retry_times = retry_times
        self.sleep_time = sleep_time
        self.retrive_depth = retrive_depth
        self.alias_names = None
        self.asset_names = asset_names
        self.file_handler = file_handler
        self.names_provider = names_provider
        self.text_provider = text_provider

    def get_alias_names(self, asset_name: str) -> list:
        """
            Get the alias names of the asset.
        """
        retry = 0
        alias_names = None
        while alias_names is None or len(alias_names) == 0:
            time.sleep(self.sleep_time)
            alias_names = self.names_provider.get_relative_names(asset_name)
            retry += 1
            if retry >= self.retry_times:
                break
        return alias_names if alias_names is not None else []
    
    def _run(self):
        i = 0
        for asset_name in self.asset_names:
            print(f"\n{i + 1}. Processing {asset_name}...")
            alias_names =  self.get_alias_names(asset_name)
            if len(alias_names) == 0:
                print(f"Failed to get data for {asset_name} in baidu.com.")
                self.file_handler._archive_unloaded_asset(asset_name)
                i += 1
                continue
            j = 0
            for alias_name in alias_names:
                if j >= self.retrive_depth:
                    break
                print(f"\n{i + 1}.{j + 1}. Processing {alias_name}...")
                time.sleep(self.sleep_time)
                text = self.text_provider.get_relics_text(alias_name)
                if text == '':
                    j -= 1
                    continue
                self.file_handler._restore_loaded_asset_data(asset_name, text, DEFAULT_RESTORE_POLICY)
                print(text)
                j += 1
            i += 1

if __name__ == '__main__':
    spider = BaiduBaikeSpider()
    spider._run()