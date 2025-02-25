import os
import shutil
import time
from gradio_client import Client, handle_file
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_fixed

client = Client("JeffreyXiang/TRELLIS")

# 确保目标目录存在
os.makedirs("./GLB", exist_ok=True)
os.makedirs("./Video", exist_ok=True)

fig_dir = "./Fig"
video_dir = "./Video"
glb_dir = "./GLB"

# API 速率限制：每 1 分钟最多 1 次
MAX_REQUESTS_PER_MIN = 1
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MIN  # 每次请求间隔（秒）

# 记录请求时间戳
request_timestamps = []

# 处理 PNG 文件
for filename in os.listdir(fig_dir):
    if filename.lower().endswith(".png"):  # 仅处理 PNG 文件
        base_name = os.path.splitext(filename)[0]
        fig_path = os.path.join(fig_dir, filename)
        video_path = os.path.join(video_dir, f"{base_name}.mp4")
        glb_path = os.path.join(glb_dir, f"{base_name}.glb")

        # 仅在视频文件不存在时执行
        if not os.path.exists(video_path):
            print(f"处理文件: {fig_path}")

            # 限制速率（检查时间戳）
            while len(request_timestamps) >= MAX_REQUESTS_PER_MIN:
                now = time.time()
                if now - request_timestamps[0] >= 60:
                    request_timestamps.pop(0)  # 移除旧请求
                else:
                    sleep_time = 60 - (now - request_timestamps[0])
                    print(f"达到 API 限制，等待 {sleep_time:.2f} 秒...")
                    time.sleep(sleep_time)

            # 记录请求时间
            request_timestamps.append(time.time())

            # 处理图片（压缩）
            image = Image.open(fig_path)
            image = image.resize((512, 512))
            compressed_image_path = "compressed.png"
            image.save(compressed_image_path)
            image_file = handle_file(compressed_image_path)

            # 运行 image_to_3d（加重试）
            @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
            def call_image_to_3d():
                return client.predict(
                    image=image_file,
                    multiimages=[],
                    seed=0,
                    ss_guidance_strength=7.5,
                    ss_sampling_steps=12,
                    slat_guidance_strength=3,
                    slat_sampling_steps=12,
                    multiimage_algo="stochastic",
                    api_name="/image_to_3d"
                )

            try:
                result = call_image_to_3d()
                print(result)
                generated_video_path = result.get("video")
            except Exception as e:
                print(f"调用 image_to_3d 失败: {e}")
                continue  # 跳过此文件

            # 运行 extract_glb（加重试）
            @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
            def call_extract_glb():
                return client.predict(
                    mesh_simplify=0.95,
                    texture_size=1024,
                    api_name="/extract_glb"
                )

            try:
                result = call_extract_glb()
                print(result)
                generated_glb_path = result[0]
            except Exception as e:
                print(f"调用 extract_glb 失败: {e}")
                continue  # 跳过此文件

            # 移动文件到目标目录
            if generated_video_path:
                shutil.move(generated_video_path, video_path)
                print(f"视频文件已移动至: {video_path}")

            if generated_glb_path:
                shutil.move(generated_glb_path, glb_path)
                print(f"GLB 文件已移动至: {glb_path}")

            # 等待下一次请求
            time.sleep(REQUEST_INTERVAL)

        else:
            print(f"跳过: {video_path} 已存在")
