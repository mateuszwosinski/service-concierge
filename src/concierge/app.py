import uvicorn
from fastapi import FastAPI
from loguru import logger

from concierge.agent.main import Agent
from concierge.datatypes.chat_types import ChatRequest, ChatResponse

app = FastAPI(title="Concierge Service", version="1.0.0")

agent = Agent()


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that receives a message and returns a response.
    """
    logger.info(f"Received message for conversation {request.conversation_id}: {request.message}")
    response = agent.process_message(request.conversation_id, request.message)
    logger.info(f"Responding to conversation {request.conversation_id} with: {response}")
    return ChatResponse(response=response)


if __name__ == "__main__":
    uvicorn.run("concierge.app:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
