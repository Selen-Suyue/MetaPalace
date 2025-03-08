import requests

# 创建会话
response = requests.get("http://localhost:8101/chat/create_session/", params={"artifact_name": "莲鹤方壶", "k": 5})
session_id = response.json()["session_id"]

# 发送音频
file_path = "RAG\\audio\\hello.wav"
with open(file_path, "rb") as file:
    response = requests.post(
        f"http://localhost:8101/chat_with_audio?session_id={session_id}", 
        files={"file": ('hello.wav', file.read(), 'audio/wav')}
    )
    print(response.json())
