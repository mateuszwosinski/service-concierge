import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from openai import APIError, AuthenticationError, RateLimitError
from pydantic import ValidationError

from concierge.agent.main import Agent
from concierge.datatypes.chat_types import ChatRequest

load_dotenv()

app = FastAPI(title="Concierge Service", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "Validation error",
            "detail": exc.errors(),
            "message": "Invalid request data. Please check your input.",
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.error(f"Pydantic validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Configuration error",
            "message": "Server configuration error. Please contact support.",
        },
    )


@app.exception_handler(AuthenticationError)
async def openai_auth_exception_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    """Handle OpenAI authentication errors."""
    logger.error(f"OpenAI authentication error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "API authentication failed",
            "message": "Unable to authenticate with the AI service. Please contact support.",
        },
    )


@app.exception_handler(RateLimitError)
async def openai_ratelimit_exception_handler(request: Request, exc: RateLimitError) -> JSONResponse:
    """Handle OpenAI rate limit errors."""
    logger.error(f"OpenAI rate limit error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again in a moment.",
        },
    )


@app.exception_handler(APIError)
async def openai_api_exception_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle OpenAI API errors."""
    logger.error(f"OpenAI API error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "AI service error",
            "message": "The AI service is temporarily unavailable. Please try again later.",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other uncaught exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


# Initialize agent with proper error handling
try:
    agent = Agent()
    logger.info("Agent initialized successfully")
except ValidationError as e:
    logger.error(f"Failed to initialize agent due to configuration error: {e}")
    raise
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    raise


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/v1/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    """
    Chat endpoint that receives a message and returns a response.

    Args:
        request: Chat request containing conversation_id and message

    Returns:
        Agent's response

    Raises:
        HTTPException: If request validation fails or processing encounters an error
    """
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    if not request.conversation_id or not request.conversation_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conversation ID cannot be empty",
        )

    try:
        logger.info(f"Processing chat request for conversation {request.conversation_id}")
        response = agent.process_message(request.conversation_id, request.message)
        return {"message": response}
    except AuthenticationError:
        # Re-raise to be handled by exception handler
        raise
    except RateLimitError:
        # Re-raise to be handled by exception handler
        raise
    except APIError:
        # Re-raise to be handled by exception handler
        raise
    except Exception as e:
        logger.exception(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process your message. Please try again.",
        ) from e


if __name__ == "__main__":
    uvicorn.run("concierge.app:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
