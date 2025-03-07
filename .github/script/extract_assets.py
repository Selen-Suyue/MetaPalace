import os
import shutil
import json
from pathlib import Path

FIG_DIR = "Fig"
GLB_DIR = "GLB"
DESC_DIR = "RAG/output"
OUTPUT_DIR = "build"
RELEASE_FILE = "release.txt"


def find_common_assets():
    """Finds assets that exist in all required directories."""
    fig_files = {Path(f).stem for f in os.listdir(FIG_DIR) if f.endswith(".png")}
    glb_files = {Path(f).stem for f in os.listdir(GLB_DIR) if f.endswith(".glb")}
    desc_files = {Path(f).stem for f in os.listdir(DESC_DIR) if f.endswith(".txt")}
    return fig_files & glb_files & desc_files


def prepare_build_directory(assets, release_list):
    """Prepares the build directory by copying assets and creating metadata."""

    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(
        parents=True, exist_ok=True
    )  # Create the directory and any missing parents.
    (output_path / "fig").mkdir(exist_ok=True)
    (output_path / "glb").mkdir(exist_ok=True)
    (output_path / "desc").mkdir(exist_ok=True)

    for asset in assets:
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
    with open(output_path / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def load_release_list():
    """Loads the release list from the release file."""
    release_file_path = Path(RELEASE_FILE)
    if not release_file_path.exists():
        print(f"Warning: {RELEASE_FILE} not found. Using empty release list.")
        return []

    try:
        with open(release_file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading {RELEASE_FILE}: {e}")  # More informative error message
        return []


def main():
    """Main function to find common assets, load release list, and prepare the build directory."""

    required_dirs = [FIG_DIR, GLB_DIR, DESC_DIR]
    if not all(os.path.exists(d) for d in required_dirs):
        raise FileNotFoundError(
            f"Missing one or more required directories: {required_dirs}"
        )

    common_assets = find_common_assets()
    release_list = load_release_list()

    # Filter release_list to only include items that are in common_assets
    filtered_release_list = [item for item in release_list if item in common_assets]

    if not common_assets:
        print("No common assets found.")
        return

    prepare_build_directory(common_assets, filtered_release_list)
    print(f"Prepared build directory with {len(common_assets)} matched assets.")


if __name__ == "__main__":
    main()
