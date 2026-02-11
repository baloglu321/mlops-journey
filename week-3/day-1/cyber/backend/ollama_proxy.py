"""
Simple proxy server to translate OpenAI API calls to Ollama format.
This allows openai-agents library to work with Ollama.
"""
import asyncio
import json
from typing import AsyncIterator
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import httpx
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")

timeout = httpx.Timeout(60.0, connect=30.0)


@app.get("/v1/models")
async def list_models():
    """Translate OpenAI models endpoint to Ollama /api/tags."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
        ollama_models = response.json()

        # Convert Ollama format to OpenAI format
        openai_models = {
            "object": "list",
            "data": [
                {
                    "id": model["name"],
                    "object": "model",
                    "created": 1234567890,
                    "owned_by": "ollama",
                }
                for model in ollama_models.get("models", [])
            ],
        }
        return openai_models


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """Translate OpenAI chat completions to Ollama /api/chat."""
    body = await request.json()

    # Convert OpenAI format to Ollama format
    ollama_request = {
        "model": body.get("model", "gemma3:27b"),
        "messages": body.get("messages", []),
        "stream": body.get("stream", False),
        "options": {
            "temperature": body.get("temperature", 0.7),
            "top_p": body.get("top_p", 1.0),
        },
    }

    async with httpx.AsyncClient(timeout=300.0) as client:
        if ollama_request["stream"]:
            # Handle streaming
            async def stream_response():
                async with client.stream(
                    "POST", f"{OLLAMA_BASE_URL}/api/chat", json=ollama_request
                ) as response:
                    async for line in response.aiter_lines():
                        if line.strip():
                            ollama_chunk = json.loads(line)
                            # Convert to OpenAI format
                            openai_chunk = {
                                "id": "chatcmpl-123",
                                "object": "chat.completion.chunk",
                                "created": 1234567890,
                                "model": ollama_request["model"],
                                "choices": [
                                    {
                                        "index": 0,
                                        "delta": {
                                            "content": ollama_chunk.get(
                                                "message", {}
                                            ).get("content", "")
                                        },
                                        "finish_reason": "stop"
                                        if ollama_chunk.get("done")
                                        else None,
                                    }
                                ],
                            }
                            yield f"data: {json.dumps(openai_chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(stream_response(), media_type="text/event-stream")
        else:
            # Handle non-streaming
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat", json=ollama_request
            )
            ollama_response = response.json()

            # Convert to OpenAI format
            openai_response = {
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1234567890,
                "model": ollama_request["model"],
                "choices": [
                    {
                        "index": 0,
                        "message": ollama_response.get("message", {}),
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
            return openai_response


@app.post("/v1/responses/create")
async def responses_create(request: Request):
    """
    Translate OpenAI Agents SDK responses.create to Ollama /api/chat.
    This is the endpoint used by the openai-agents library.
    """
    body = await request.json()
    print(f"📥 Received request to /v1/responses/create: {json.dumps(body, indent=2)}")

    # The SDK sends "input" instead of "messages"
    # Extract messages from input field or fall back to messages field
    input_messages = body.get("input", [])
    messages = body.get("messages", [])

    # Use input if it exists, otherwise fall back to messages
    actual_messages = input_messages if input_messages else messages

    # Combine with instructions if provided
    instructions = body.get("instructions", "")
    if instructions and actual_messages:
        # Prepend instructions as a system message
        actual_messages = [
            {"role": "system", "content": instructions}
        ] + actual_messages

    model = body.get("model", "gemma3:27b")

    print(f"🔍 Processing {len(actual_messages)} messages")

    # NOTE: We're NOT forwarding tools to Ollama because:
    # 1. Ollama expects a different tool format
    # 2. The OpenAI Agents SDK handles tool calling on its own
    # 3. We just need the text response from Ollama

    # Convert to Ollama format
    ollama_request = {
        "model": model,
        "messages": actual_messages,
        "stream": False,
        "options": {
            "temperature": body.get("temperature", 0.7),
        },
    }

    print(f"🔄 Forwarding to Ollama: {OLLAMA_BASE_URL}/api/chat")

    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=ollama_request)
        ollama_response = response.json()

        print(f"✅ Got response from Ollama")
        print(f"🔍 Ollama response keys: {ollama_response.keys()}")
        print(
            f"🔍 Full response: {json.dumps(ollama_response, indent=2)[:500]}"
        )  # First 500 chars

        # Extract the content from Ollama response
        content = ollama_response.get("message", {}).get("content", "")
        print(f"🔍 Message content length: {len(content)}")

        # Convert to OpenAI Agents SDK format
        # The agents SDK expects a specific response format with "output" field
        openai_response = {
            "id": "resp-123",
            "object": "response",
            "created": 1234567890,
            "model": model,
            "output": [  # This is the key field the SDK expects
                {"type": "message", "role": "assistant", "content": content}
            ],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 100,  # Dummy value - Ollama doesn't provide this
                "completion_tokens": 100,  # Dummy value
                "total_tokens": 200,  # Dummy value
                "input_tokens": 100,  # Required by newer SDK versions
                "output_tokens": 100,  # Required by newer SDK versions
            },
        }

        return openai_response


@app.post("/v1/traces")
async def create_trace(request: Request):
    """Handle trace requests from OpenAI Agents SDK (no-op)."""
    # Just return success, we don't need traces for local development
    return {"id": "trace-123", "status": "ok"}


@app.post("/responses")
async def responses_create_no_prefix(request: Request):
    """
    Alias for /v1/responses/create without the /v1 prefix.
    Some SDK versions POST directly to /responses.
    """
    return await responses_create(request)


@app.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path: str, request: Request):
    """Catch-all for other OpenAI API endpoints."""
    print(f"⚠️  Unhandled endpoint: /v1/{path}")
    # For now, just return a simple response
    return {
        "error": f"Endpoint /v1/{path} not yet implemented",
        "status": "not_implemented",
    }


if __name__ == "__main__":
    print("🚀 Starting Ollama-OpenAI compatibility proxy on http://localhost:4000")
    print(f"📡 Forwarding requests to: {OLLAMA_BASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="info")
