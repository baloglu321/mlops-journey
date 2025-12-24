from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from langchain_ollama import ChatOllama
import os

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def instant():
    # Uzak Ollama sunucusu URL'i (ortam değişkeninden veya varsayılan olarak)
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", ".../")

    # Uzak Ollama sunucusuna bağlan
    llm = ChatOllama(
        model="gemma3:27b",  # Ollama'da yüklü olan model adını kullanın
        base_url=ollama_base_url,
    )

    message = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""

    # LangChain Ollama ile mesaj gönder
    response = llm.invoke(message)
    reply = response.content.replace("\n", "<br/>")

    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return html
