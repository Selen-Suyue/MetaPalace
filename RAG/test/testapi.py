import requests

artifact_name = '莲鹤方壶'
# 发送音频
file_path = "RAG\\audio\\hello.wav"
with open(file_path, "rb") as file:
    response = requests.post(
        f"http://localhost:10004/aichat/{artifact_name}", 
        files={"audio": ('hello.wav', file.read(), 'audio/wav')}
    )
    print(response.text)
