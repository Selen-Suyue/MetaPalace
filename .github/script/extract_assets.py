import os
import shutil
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

FIG_DIR = "Fig"
GLB_DIR = "GLB"
DESC_DIR = "RAG/output"
OUTPUT_DIR = "build"
RELEASE_FILE = "release.txt"


def find_common_assets():
    """Finds assets that exist in all required directories."""
    logging.info("Finding common assets...")
    fig_files = {Path(f).stem for f in os.listdir(FIG_DIR) if f.endswith(".png")}
    glb_files = {Path(f).stem for f in os.listdir(GLB_DIR) if f.endswith(".glb")}
    desc_files = {Path(f).stem for f in os.listdir(DESC_DIR) if f.endswith(".txt")}
    common_assets = fig_files & glb_files & desc_files
    logging.info(f"Found {len(common_assets)} common assets.")
    return common_assets


def prepare_build_directory(assets, release_list):
    """Prepares the build directory by copying assets and creating metadata."""
    logging.info(f"Preparing build directory: {OUTPUT_DIR}")
    output_path = Path(OUTPUT_DIR)

    if output_path.exists():
        logging.info(f"Removing existing build directory: {OUTPUT_DIR}")
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "fig").mkdir(exist_ok=True)
    (output_path / "glb").mkdir(exist_ok=True)
    (output_path / "desc").mkdir(exist_ok=True)

    for asset in assets:
        logging.info(f"Copying asset: {asset}")
        shutil.copy(
            Path(FIG_DIR) / f"{asset}.png", output_path / "fig" / f"{asset}.png"
        )
        shutil.copy(
            Path(GLB_DIR) / f"{asset}.glb", output_path / "glb" / f"{asset}.glb"
        )
        shutil.copy(
            Path(DESC_DIR) / f"{asset}.txt", output_path / "desc" / f"{asset}.txt"
        )

    meta = {"support": sorted(assets), "release": release_list}
    logging.info(
        f"Creating meta.json with support: {len(assets)} and release: {len(release_list)}"
    )
    with open(output_path / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    logging.info("meta.json created successfully.")


def load_release_list():
    """Loads the release list from the release file."""
    release_file_path = Path(RELEASE_FILE)
    if not release_file_path.exists():
        logging.warning(f"{RELEASE_FILE} not found. Using empty release list.")
        return []

    try:
        with open(release_file_path, "r", encoding="utf-8") as f:
            release_list = [line.strip() for line in f if line.strip()]
        logging.info(f"Loaded {len(release_list)} release items from {RELEASE_FILE}.")
        return release_list
    except Exception as e:
        logging.error(f"Error reading {RELEASE_FILE}: {e}")
        return []


def main():
    """Main function to find common assets, load release list, and prepare the build directory."""
    logging.info("Starting asset extraction process.")

    required_dirs = [FIG_DIR, GLB_DIR, DESC_DIR]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            logging.error(f"Missing required directory: {dir_path}")
            raise FileNotFoundError(f"Missing required directory: {dir_path}")

    common_assets = find_common_assets()
    release_list = load_release_list()

    # Filter release_list to only include items that are in common_assets
    filtered_release_list = [item for item in release_list if item in common_assets]

    if not common_assets:
        logging.warning("No common assets found.")
        return

    prepare_build_directory(common_assets, filtered_release_list)
    logging.info("Asset extraction process completed successfully.")


if __name__ == "__main__":
    main()
