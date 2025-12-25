from fastapi import FastAPI  # type: ignore
from fastapi.responses import PlainTextResponse  # type: ignore
from langchain_ollama import ChatOllama  # type: ignore
import os  # type: ignore

app = FastAPI()


@app.get("/api", response_class=PlainTextResponse)
def idea():
    # Uzak Ollama sunucusu URL'i (ortam değişkeninden veya varsayılan olarak)
    ollama_base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "...",
    )

    # Uzak Ollama sunucusuna bağlan
    llm = ChatOllama(
        model="gemma3:27b",  # Ollama'da yüklü olan model adını kullanın
        base_url=ollama_base_url,
    )

    prompt = "Come up with a new business idea for AI Agents"

    # LangChain Ollama ile mesaj gönder
    response = llm.invoke(prompt)
    return response.content
