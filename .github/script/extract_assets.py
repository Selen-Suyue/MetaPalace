import os
import shutil
import json

FIG_DIR = 'Fig'
GLB_DIR = 'GLB'
DESC_DIR = 'RAG/output'
OUTPUT_DIR = 'build'

def find_common_assets():
    fig_files = {os.path.splitext(f)[0] for f in os.listdir(FIG_DIR) if f.endswith('.png')}
    glb_files = {os.path.splitext(f)[0] for f in os.listdir(GLB_DIR) if f.endswith('.glb')}
    desc_files = {os.path.splitext(f)[0] for f in os.listdir(DESC_DIR) if f.endswith('.txt')}
    return fig_files & glb_files & desc_files

def prepare_build_directory(assets):
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(f'{OUTPUT_DIR}/fig', exist_ok=True)
    os.makedirs(f'{OUTPUT_DIR}/glb', exist_ok=True)
    os.makedirs(f'{OUTPUT_DIR}/desc', exist_ok=True)

    for asset in assets:
        shutil.copy(f'{FIG_DIR}/{asset}.png', f'{OUTPUT_DIR}/fig/{asset}.png')
        shutil.copy(f'{GLB_DIR}/{asset}.glb', f'{OUTPUT_DIR}/glb/{asset}.glb')
        shutil.copy(f'{DESC_DIR}/{asset}.txt', f'{OUTPUT_DIR}/desc/{asset}.txt')

    meta = {"support": sorted(assets)}
    with open(f'{OUTPUT_DIR}/meta.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def main():
    if not os.path.exists(FIG_DIR) or not os.path.exists(GLB_DIR) or not os.path.exists(DESC_DIR):
        raise FileNotFoundError(f"Missing '{FIG_DIR}' or '{GLB_DIR}' or '{DESC_DIR}' directory.")

    common_assets = find_common_assets()

    if not common_assets:
        print("No common assets found.")
        return

    prepare_build_directory(common_assets)
    print(f"Prepared build directory with {len(common_assets)} matched assets.")

if __name__ == '__main__':
    main()
