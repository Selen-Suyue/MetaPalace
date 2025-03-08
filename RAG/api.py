from fastapi import FastAPI, UploadFile

from langchain_gemini import GeminiLLMChain
import uuid, os

app = FastAPI()

chain = GeminiLLMChain()

def build_config(string_id: str):
    id = uuid.UUID(string_id)
    return {
        "configurable": {
            "thread_id": id
        }
    }

@app.get("/chat/create_session/")
async def create_session(artifact_name: str, k: int = 5):
    config = chain.create_session(artifact_name, k)
    return {'session_id': str(config["configurable"]["thread_id"])}

@app.post("/chat_with_audio/")
async def get_response(session_id: str, file: UploadFile):
    with open(file.filename, 'wb') as buffer:
        buffer.write(await file.read())
    config = build_config(session_id)
    response = chain.chat_with_audio(config, file.filename)

    if os.path.exists(file.filename):
        os.remove(file.filename)
    return {"response": response}

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8101

    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)