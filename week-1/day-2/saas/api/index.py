from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from langchain_ollama import ChatOllama  # type: ignore
import os  # type: ignore
import json


app = FastAPI()


@app.get("/api")
async def idea():
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
            # yield "data: [BAĞLANTI BAŞLADI]\n\n" # İstersen bunu açıp test edebilirsin

            async for chunk in llm.astream(prompt):
                content = chunk.content
                if content:
                    # Satır sonlarını bozmadan JSON string'i gibi kaçış karakteri ekle
                    safe_content = content.replace("\n", "\\n")
                    yield f"data: {safe_content}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            error_msg = str(e).replace("\n", " ")
            yield f"data: Error: {error_msg}\n\n"

    # 3. KRİTİK KISIM: Header Ayarları
    # Bu headerlar Vercel'e "Veriyi saklama, hemen yolla" der.
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream",
        "X-Accel-Buffering": "no",  # Nginx/Vercel proxy buffering'i kapatır
    }

    return StreamingResponse(
        event_stream(), headers=headers, media_type="text/event-stream"
    )
