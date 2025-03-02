import os
import shutil
import time
import sys
from collections import deque

from gradio_client import Client, handle_file
from PIL import Image

client = Client("JeffreyXiang/TRELLIS")

# 确保目标目录存在
os.makedirs("./GLB", exist_ok=True)
os.makedirs("./Video", exist_ok=True)

FIG_DIR = "./Fig"
VIDEO_DIR = "./Video"
GBL_DIR = "./GLB"

# 记录最近 60 秒内的请求时间戳
request_timestamps = deque()

# 设定窗口时长和最大请求次数
RATE_LIMIT_WINDOW = 60  # 秒
MAX_REQUESTS_PER_WINDOW = 1


def rate_limit():
    """检查并等待直到符合速率限制"""
    now = time.time()

    # 清理超过窗口期的时间戳
    while request_timestamps and now - request_timestamps[0] >= RATE_LIMIT_WINDOW:
        request_timestamps.popleft()

    # 如果当前请求数已经满了，等待下一个时间点
    if len(request_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        earliest = request_timestamps[0]
        sleep_time = RATE_LIMIT_WINDOW - (now - earliest)
        print(f"达到 API 限制，等待 {sleep_time:.2f} 秒...")
        time.sleep(max(0, sleep_time))

        # 重新清理并确认
        now = time.time()
        while request_timestamps and now - request_timestamps[0] >= RATE_LIMIT_WINDOW:
            request_timestamps.popleft()

    # 记录当前请求时间戳
    request_timestamps.append(time.time())


def handle_api_failure(message: str):
    print(f"[ERROR] {message}")
    sys.exit(1)  # 立刻终止整个程序


def compress_image(input_path: str, output_path: str = "compressed.png"):
    image = Image.open(input_path)
    image.thumbnail((512, 512))
    image.save(output_path)
    return output_path


def call_start_session():
    try:
        return client.predict(api_name="/start_session")
    except Exception as e:
        handle_api_failure(f"调用 start_session 失败: {e}")


def call_image_to_3d(image_file):
    try:
        return client.predict(
            image=image_file,
            multiimages=[],
            seed=0,
            ss_guidance_strength=7.5,
            ss_sampling_steps=12,
            slat_guidance_strength=3,
            slat_sampling_steps=12,
            multiimage_algo="stochastic",
            api_name="/image_to_3d",
        )
    except Exception as e:
        handle_api_failure(f"调用 image_to_3d 失败: {e}")


def call_extract_glb():
    try:
        return client.predict(
            mesh_simplify=0.95, texture_size=1024, api_name="/extract_glb"
        )
    except Exception as e:
        handle_api_failure(f"调用 extract_glb 失败: {e}")


for filename in os.listdir(FIG_DIR):
    if not filename.lower().endswith(".png"):
        continue

    base_name = os.path.splitext(filename)[0]
    fig_path = os.path.join(FIG_DIR, filename)
    video_path = os.path.join(VIDEO_DIR, f"{base_name}.mp4")
    glb_path = os.path.join(GBL_DIR, f"{base_name}.glb")

    if os.path.exists(video_path):
        print(f"跳过: {video_path} 已存在")
        continue

    print(f"处理文件: {fig_path}")

    # 速率限制
    rate_limit()

    # 压缩图片
    try:
        compressed_image_path = compress_image(fig_path)
        image_file = handle_file(compressed_image_path)
    except Exception as e:
        print(f"压缩图片失败: {e}")
        continue

    # Start Session
    session_result = call_start_session()
    print(session_result)

    # Image to 3D
    image_to_3d_result = call_image_to_3d(image_file)
    print(image_to_3d_result)

    generated_video_path = image_to_3d_result.get("video")
    if not generated_video_path:
        handle_api_failure("image_to_3d 返回结果中没有找到视频文件路径")

    # Extract GLB
    extract_glb_result = call_extract_glb()
    print(extract_glb_result)

    if not extract_glb_result or len(extract_glb_result) < 1:
        handle_api_failure("extract_glb 返回结果无效")

    generated_glb_path = extract_glb_result[0]

    # 保存结果文件
    shutil.move(generated_video_path, video_path)
    print(f"视频文件已保存: {video_path}")

    shutil.move(generated_glb_path, glb_path)
    print(f"GLB 文件已保存: {glb_path}")

print("所有文件处理完毕。")
