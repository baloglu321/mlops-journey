from fastapi import FastAPI, Depends  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama  # type: ignore
import os  # type: ignore
import asyncio


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Şimdilik tüm kaynaklara izin verelim
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)


@app.get("/api")
def idea(creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]  # User ID from JWT - available for future use
    # 1. Ortam Değişkeni Kontrolü
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "...")

    # 2. LLM Ayarları
    llm = ChatOllama(
        model="gemma3:27b",
        base_url=ollama_base_url,
        temperature=0.7,
    )

    prompt = "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"

    async def event_stream():
        try:
            async for chunk in llm.astream(prompt):
                content = chunk.content
                if content:
                    safe_content = content.replace("\n", "\\n")
                    # JSON formatına uygun gönderim
                    yield f"data: {safe_content}\n\n"
                    # İşlemciye nefes aldır (Flush işlemini tetikler)
                    await asyncio.sleep(0)

            yield "data: [DONE]\n\n"
        except Exception as e:
            error_msg = str(e).replace("\n", " ")
            yield f"data: Error: {error_msg}\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream",
        "X-Accel-Buffering": "no",  # Bu satır çok önemli, Vercel'e 'bekletme yapma' der
    }

    return StreamingResponse(
        event_stream(), headers=headers, media_type="text/event-stream"
    )
