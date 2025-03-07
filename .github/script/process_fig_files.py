import os
import shutil
import sys
import logging

from gradio_client import Client, handle_file
from PIL import Image

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 定义常量
FIG_DIR = "./Fig"
VIDEO_DIR = "./Video"
GBL_DIR = "./GLB"
TRELLIS_API_URL = "JeffreyXiang/TRELLIS"  # 替换为实际的 API URL

# 创建目录
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(GBL_DIR, exist_ok=True)


def initialize_client(api_url: str) -> Client:
    """初始化 Gradio 客户端."""
    try:
        client = Client(api_url)
        return client
    except Exception as e:
        logging.error(f"初始化 Gradio 客户端失败: {e}")
        sys.exit(1)


def compress_image(input_path: str, output_path: str = "compressed.png") -> str:
    """压缩图片并返回压缩后的路径."""
    try:
        image = Image.open(input_path)
        image.thumbnail((512, 512))
        image.save(output_path)
        return output_path
    except Exception as e:
        logging.error(f"压缩图片 {input_path} 失败: {e}")
        raise  # 重新抛出异常，让上层处理


def call_api(client: Client, api_name: str, **kwargs):
    """调用 Gradio API 并处理错误."""
    try:
        return client.predict(api_name=api_name, **kwargs)
    except Exception as e:
        logging.error(f"调用 API {api_name} 失败: {e}")
        raise  # 重新抛出异常，让上层处理


def process_image(client: Client, fig_path: str, base_name: str):
    """处理单个图片文件."""
    video_path = os.path.join(VIDEO_DIR, f"{base_name}.mp4")
    glb_path = os.path.join(GBL_DIR, f"{base_name}.glb")

    if os.path.exists(video_path):
        logging.info(f"跳过: {video_path} 已存在")
        return

    logging.info(f"处理文件: {fig_path}")

    try:
        # 压缩图片
        compressed_image_path = compress_image(fig_path)
        image_file = handle_file(compressed_image_path)

        # 调用 API
        session_result = call_api(client, "/start_session")
        logging.info(f"start_session result: {session_result}")

        image_to_3d_result = call_api(
            client,
            "/image_to_3d",
            image=image_file,
            multiimages=[],
            seed=0,
            ss_guidance_strength=7.5,
            ss_sampling_steps=12,
            slat_guidance_strength=3,
            slat_sampling_steps=12,
            multiimage_algo="stochastic",
        )
        logging.info(f"image_to_3d result: {image_to_3d_result}")

        generated_video_path = image_to_3d_result.get("video")
        if not generated_video_path:
            raise ValueError("image_to_3d 返回结果中没有找到视频文件路径")

        extract_glb_result = call_api(
            client, "/extract_glb", mesh_simplify=0.95, texture_size=1024
        )
        logging.info(f"extract_glb result: {extract_glb_result}")

        if not extract_glb_result or len(extract_glb_result) < 1:
            raise ValueError("extract_glb 返回结果无效")

        generated_glb_path = extract_glb_result[0]

        # 保存结果文件
        shutil.move(generated_video_path, video_path)
        logging.info(f"视频文件已保存: {video_path}")

        shutil.move(generated_glb_path, glb_path)
        logging.info(f"GLB 文件已保存: {glb_path}")

    except Exception as e:
        logging.error(f"处理文件 {fig_path} 失败: {e}")
        sys.exit(1)


def main():
    """主函数."""
    client = initialize_client(TRELLIS_API_URL)

    for filename in os.listdir(FIG_DIR):
        if not filename.lower().endswith(".png"):
            continue

        base_name = os.path.splitext(filename)[0]
        fig_path = os.path.join(FIG_DIR, filename)
        process_image(client, fig_path, base_name)

    logging.info("所有文件处理完毕。")


if __name__ == "__main__":
    main()
