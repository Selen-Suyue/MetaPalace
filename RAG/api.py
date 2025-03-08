from fastapi import FastAPI, UploadFile, Cookie, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from langchain_gemini import GeminiLLMChain
import uuid, os

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "https://metapalace.xj63.fun"
            ],  # 仅允许来自 metapalace.xj63.fun 的访问
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


# --- 实用函数 ---
def build_config(session_id: UUID):
    return {"configurable": {"thread_id": session_id}}


# --- 辅助函数：创建会话 ---
async def create_session_helper(artifact_name: str, k: int = 5) -> UUID:
    config = chain.create_session(artifact_name, k)
    return config["configurable"]["thread_id"]


# --- API 端点 ---


@app.post("/aichat/{artifact_name}")
async def chat_with_artifact(
    artifact_name: str,
    file: UploadFile,
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
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())

        response = chain.chat_with_audio(config, file.filename)

        if os.path.exists(file.filename):
            os.remove(file.filename)
        content = {"response": response}
        response = JSONResponse(content=content)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # 3. 设置 Cookie 以便后续调用
    expires = datetime.utcnow() + timedelta(hours=SESSION_EXPIRY_HOURS)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        value=str(session_uuid),
        httponly=True,
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        domain="api.metapalace.xj63.fun",
        secure=True,  # 只有在HTTPS下才发送cookie
        samesite="strict",  # 阻止跨站请求伪造(CSRF)攻击
    )
    return response


@app.get("/chat/create_session/")
async def create_session(artifact_name: str, k: int = 5):
    session_uuid = await create_session_helper(artifact_name, k)
    return {"session_id": str(session_uuid)}


@app.post("/chat_with_audio/")
async def get_response(session_id: str, file: UploadFile):
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    config = build_config(uuid.UUID(session_id))
    response = chain.chat_with_audio(config, file.filename)

    if os.path.exists(file.filename):
        os.remove(file.filename)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
