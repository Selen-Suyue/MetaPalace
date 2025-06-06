from fastapi import FastAPI, UploadFile, Cookie, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from langchain_gemini import GeminiLLMChain, VECTOR_DB_MANAGER
from scripts.modify_db import update_db
import uuid, os, librosa, wave, torch
import numpy as np
from io import BytesIO

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 只允许这个源进行请求
            allow_credentials=True,
            allow_methods=["*"],  # 允许所有方法
            allow_headers=["*"],  # 允许所有头部
        )
    ]
)


chain = GeminiLLMChain()

# 常量
SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRY_HOURS = 1
HOST = "0.0.0.0"
PORT = 10004

COLLECTION = "Relics"


# --- 实用函数 ---
def build_config(session_id: UUID):
    return {"configurable": {"thread_id": session_id}}


# --- 辅助函数：创建会话 ---
async def create_session_helper(artifact_name: str, k: int = 5) -> UUID:
    config = chain.create_session(artifact_name, k)
    return config["configurable"]["thread_id"]

async def read_audio_file(audio_file: UploadFile):
    try:
        contents = await audio_file.read()
        audio_io = BytesIO(contents)
        wf = wave.open(audio_io, 'rb')

        # 读取音频数据
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()
        frames = wf.readframes(num_frames)

        waveform = np.frombuffer(frames, dtype=np.int16)
        waveform_tensor = torch.from_numpy(waveform).float()
        return waveform_tensor
    except wave.Error as e:
        raise HTTPException(status_code=400, detail=f"Invalid WAV file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading audio data: {str(e)}")

# --- API 端点 ---

@app.head("/")
async def health_check():
    return {"status": "OK"}

@app.post("/aichat/{artifact_name}")
async def chat_with_artifact(
    artifact_name: str,
    audio: UploadFile,
    session_id: Optional[str] = Cookie(None),
):
    """
    这个API端点接收一个音频文件，将其转录，并用它来生成响应，
    通过 httpOnly Cookie 持久化对话上下文。
    """

    session_uuid = None
    if session_id:
        try:
            session_uuid = uuid.UUID(session_id)  # 验证 Cookie 值是否为有效的 UUID
        except ValueError:
            session_uuid = None  # 如果 UUID 无效，则使其失效

    # 1. 如果不存在会话，则创建新的会话 ID 并返回配置
    if session_uuid is None:
        session_uuid = await create_session_helper(artifact_name)  # 创建新会话
        config = build_config(session_uuid)
    else:  # 如果用户存在，则返回配置
        config = build_config(session_uuid)

    # 2. 处理音频并获取响应
    try:
        waveform = await read_audio_file(audio)
        response = chain.chat_with_audio(config, waveform)
        '''
        audio_data = await audio.read()
        with BytesIO(audio_data) as audio_file:
            waveform, _ = librosa.load(audio_file, sr=None)
            response = chain.chat_with_audio(config, waveform)
        '''
        content = {"response": response}
        response = JSONResponse(content=content)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # 3. 设置 Cookie 以便后续调用
    expires = datetime.now() + timedelta(hours=SESSION_EXPIRY_HOURS)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        value=str(session_uuid),
        httponly=True,
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        # domain="api.metapalace.xj63.fun",
        # secure=True,  # 只有在HTTPS下才发送cookie
        # samesite="strict",  # 阻止跨站请求伪造(CSRF)攻击
    )
    return response

@app.post("/update_db")
async def update_database(
    folder_path: str = Query(None, description="The folder path to the documents"),
    texts: list[str] = Query(None, description="The texts to be added to the database"),
    collection_name: str = Query(COLLECTION, description="The name of the collection")
):
    """
        Update the database with the given texts or documents in the specified folder.\
        Make sure that you have the access to the admin permission.\
        `folder_path` and `texts` are mutually exclusive.
    """
    try: 
        update_db(folder_path, texts, collection_name, VECTOR_DB_MANAGER)
        return {"message": "Database updated successfully."}
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
