from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# OpenAI yerine LangChain ve Ollama importları
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import uuid
from pathlib import Path

# Load environment variables
load_dotenv(override=True)

app = FastAPI()

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LLM AYARLARI ---

llm = ChatOllama(
    model="gemma3:27b",
    base_url=os.getenv("OLLAMA_BASE_URL"),
)

# Memory directory
MEMORY_DIR = Path("../memory")
MEMORY_DIR.mkdir(exist_ok=True)


# Load personality details
def load_personality():
    try:
        with open("me.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "You are a helpful AI assistant."


PERSONALITY = load_personality()


# --- HAFIZA FONKSİYONLARI ---
def load_conversation(session_id: str) -> List[Dict]:
    """Geçmiş konuşmayı dosyadan yükler"""
    file_path = MEMORY_DIR / f"{session_id}.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_conversation(session_id: str, messages: List[Dict]):
    """Konuşmayı dosyaya kaydeder"""
    file_path = MEMORY_DIR / f"{session_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
async def root():
    return {"message": "AI Digital Twin API with Persistent Memory (Ollama)"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 1. Session ID oluştur veya al
        session_id = request.session_id or str(uuid.uuid4())

        # 2. Geçmiş konuşmayı dosyadan yükle
        conversation_history = load_conversation(session_id)

        # 3. LangChain Mesaj Listesini Hazırla
        # En başa System Prompt (Kişilik) ekle
        langchain_messages = [SystemMessage(content=PERSONALITY)]

        # --- WINDOW MEMORY MANTIĞI BURADA ---
        # Senin k=10 mantığını burada manuel yapıyoruz.
        # Sadece son 10 mesajı modele veriyoruz ki context dolmasın.
        recent_history = conversation_history[-10:]

        # Dosyadaki JSON formatını (dict) LangChain formatına (Message Object) çevir
        for msg in recent_history:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        # En sona yeni gelen kullanıcı mesajını ekle
        langchain_messages.append(HumanMessage(content=request.message))

        # 4. Modeli Çağır (Invoke)
        response = llm.invoke(langchain_messages)
        assistant_response = response.content

        # 5. Hafızayı Güncelle (Dosya için JSON formatında)
        # Buraya tüm geçmişi ekliyoruz (kısıtlama yapmadan), böylece dosya tam arşiv olur.
        conversation_history.append({"role": "user", "content": request.message})
        conversation_history.append(
            {"role": "assistant", "content": assistant_response}
        )

        # 6. Dosyaya Kaydet
        save_conversation(session_id, conversation_history)

        return ChatResponse(response=assistant_response, session_id=session_id)

    except Exception as e:
        print(f"Hata: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def list_sessions():
    """Tüm oturumları listele"""
    sessions = []
    for file_path in MEMORY_DIR.glob("*.json"):
        session_id = file_path.stem
        with open(file_path, "r", encoding="utf-8") as f:
            conversation = json.load(f)
            sessions.append(
                {
                    "session_id": session_id,
                    "message_count": len(conversation),
                    "last_message": conversation[-1]["content"]
                    if conversation
                    else None,
                }
            )
    return {"sessions": sessions}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
