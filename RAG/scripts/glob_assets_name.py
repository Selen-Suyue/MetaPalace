import glob, os

ASSETS_PATH = 'Fig/*'

def _get_assets_name(assets_dir):
    asset_path_list = glob.glob(assets_dir)
    asset_name_list = [os.path.basename(path).rsplit('.', 1)[0] for path in asset_path_list]
    return asset_name_list

if __name__ == '__main__':
    asset_name_list = _get_assets_name(ASSETS_PATH)
    print(asset_name_list)