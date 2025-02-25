import google.generativeai as genai
from PIL import Image
import os
import re 
import warnings


def load_api_key_from_txt(filepath):
    try:
        with open(filepath, 'r') as f:
            api_key = f.readline().strip()
        if not api_key:
            raise ValueError("API 密钥文件为空。")
        os.environ['GOOGLE_API_KEY'] = api_key  
        return api_key
    except FileNotFoundError:
        raise FileNotFoundError(f"找不到 API 密钥文件: {filepath}")
    except Exception as e:
        raise Exception(f"读取 API 密钥时发生错误: {e}")

def generate_content_with_image_and_text(image_path, text_prompt):

    if 'GOOGLE_API_KEY' not in os.environ:
        raise ValueError("请先设置 GOOGLE_API_KEY 环境变量，或使用 load_api_key_from_txt 函数加载密钥。")

    try:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        model = genai.GenerativeModel('gemini-2.0-flash') # need vision model

        img = Image.open(image_path)

        # 构建提示
        prompt_parts = [
            text_prompt,  
            img          
        ]

        response = model.generate_content(prompt_parts)
        response.resolve() 
        return response.text

    except Exception as e:
        print(f"生成内容时发生错误: {e}")
        return None

def extract_artifact_name(image_path):
    filename = os.path.basename(image_path)  
    name, ext = os.path.splitext(filename)  

    match = re.search(r'[\u4e00-\u9fa5]+', name) 

    if match:
        return match.group(0)
    else:
        return None 

if __name__ == "__main__":

    api_key_file = "api_key.txt"  
    try:
        load_api_key_from_txt(api_key_file)
        print("API 密钥已成功加载。")
    except Exception as e:
        print(f"初始化失败: {e}")
        exit()


    image_file = "Fig\青玉浮雕青蛙荷叶洗.png"
    artifact_name = extract_artifact_name(image_file)

    if artifact_name:
        text_prompt = f"各位观众，大家好！今天，我将以故宫讲解员的身份，为大家介绍一件精美的文物：{artifact_name}。请根据这张图片，以及关于{artifact_name}的相关资料进行检索。我希望你能详细描述它的特点，历史背景，制作工艺，以及它在当时的文化和社会意义。请用生动的语言，让观众仿佛身临其境，感受这件文物的魅力。请记住，要以故宫讲解员的口吻进行讲解。"
    else:
        text_prompt = "各位观众，大家好！今天，我将以故宫讲解员的身份，为大家介绍一件精美的文物。请根据这张图片详细描述它的特点，历史背景，制作工艺，以及它在当时的文化和社会意义。请用生动的语言，让观众仿佛身临其境，感受这件文物的魅力。请记住，要以故宫讲解员的口吻进行讲解。"

    try:
        generated_text = generate_content_with_image_and_text(image_file, text_prompt)

        if generated_text:
            print("生成的内容:\n", generated_text)
        else:
            print("生成内容失败。")

    except Exception as e:
        print(f"主程序发生错误: {e}")