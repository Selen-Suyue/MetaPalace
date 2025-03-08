import glob, os

ASSETS_PATH = 'Fig/*'
TXT_PATH = 'release.txt'

def _get_assets_name(assets_dir: str = ASSETS_PATH):
    asset_path_list = glob.glob(assets_dir)
    asset_name_list = [os.path.basename(path).rsplit('.', 1)[0] for path in asset_path_list]
    return asset_name_list

def _get_assets_name_from_txt(txt_path: str = TXT_PATH):
    with open(txt_path, 'r', encoding='utf-8') as f:
        asset_name_list = [line.strip() for line in f.readlines()]
    return asset_name_list

if __name__ == '__main__':
    asset_name_list = _get_assets_name_from_txt()
    print(asset_name_list)