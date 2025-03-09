from enum import Enum, unique

DATA_PATH = './RAG/data/'
ARCHIVE_PATH = './RAG/archive/'
ARCHIVED_ASSETS_FILENAME = 'archived_assets.txt'

ECODING = 'utf-8'

@unique
class RestoreHandlerType(Enum):
    """
    Enum for handling the way an asset is restored.
        COVER: Overwrite the existing asset data.
        SUPERADD: Append the new asset data to the existing asset data.
    """
    COVER = 1
    SUPERADD = 2

class FileHandler():
    """
    File handler for the RAG project. To modify the policy of handing the data(the default is to overwrite the existing data when loading the data), you need import the `RestoreHandlerType` enum first.
    Parameters:
        `data_path`: str, default 'RAG/data/'
            The path for storing the data of the assets.
        `archive_path`: str, default 'RAG/archive/'
            The path for storing the names of the assets that failed to be loaded.
    """
    def __init__(self, data_path: str = DATA_PATH, archive_path: str = ARCHIVE_PATH):
        self.path_dict = {
            'data': data_path,
            'archive': archive_path
        }

    def _modify_path(self, path_name: str, path_value: str):
        """
        Modify the path of the data or archive.
        """
        self.path_dict[path_name] = path_value

    def _archive_unloaded_asset(self, asset_name: str, handler_type: RestoreHandlerType = RestoreHandlerType.COVER):
        if handler_type == RestoreHandlerType.COVER:
            with open(self.path_dict['archive'] + ARCHIVED_ASSETS_FILENAME, 'w', encoding=ECODING) as f:
                f.write(asset_name + '\n')
        elif handler_type == RestoreHandlerType.SUPERADD:
            with open(self.path_dict['archive'] + ARCHIVED_ASSETS_FILENAME, 'a', encoding=ECODING) as f:
                f.write(asset_name + '\n')
        else:
            raise ValueError('Invalid handler type')

    def _restore_loaded_asset_data(self, asset_name: str, asset_description: str, handler_type: RestoreHandlerType = RestoreHandlerType.COVER):
        if handler_type == RestoreHandlerType.COVER:
            with open(self.path_dict['data'] + asset_name + '.txt', 'w', encoding=ECODING) as f:
                f.write(asset_description)
        elif handler_type == RestoreHandlerType.SUPERADD:
            with open(self.path_dict['data'] + asset_name + '.txt', 'a', encoding=ECODING) as f:
                f.write(asset_description + '\n')
        else:
            raise ValueError('Invalid handler type')