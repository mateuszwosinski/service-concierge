import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from concierge.agent.main import Agent
from concierge.datatypes.chat_types import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="Concierge Service", version="1.0.0")

agent = Agent()


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that receives a message and returns a response.
    """
    response = agent.process_message(request.conversation_id, request.message)
    return ChatResponse(response=response)


if __name__ == "__main__":
    uvicorn.run("concierge.app:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
