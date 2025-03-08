from fastapi import FastAPI

from langchain_gemini import GeminiLLMChain
import uuid

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
async def create_session_id(artifact_name: str, k: int = 5):
    config = chain.create_session(artifact_name, k)
    return {"session_id": str(config["configurable"]["thread_id"])}

@app.get("/chat/")
async def get_response(session_id: str, input: str):
    config = build_config(session_id)
    response = chain.chat(config, input)
    return {"question": input, "response": response}

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8101

    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
    '''
        URL example:
            "http://{HOST}:{PORT}/chat/create_session?artifact_name=xxx"
            "http://{HOST}:{PORT}/chat?session_id=xxx&input=xxx"
    '''