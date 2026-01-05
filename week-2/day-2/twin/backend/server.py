from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import uuid
from datetime import datetime
from pathlib import Path
from resources import facts

# S3 Kütüphaneleri
import boto3
from botocore.exceptions import ClientError

# Bizim hazırladığımız context (System Prompt)
from context import prompt

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

# --- KONFIGURASYON ---
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
S3_BUCKET = os.getenv("S3_BUCKET", "")
MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "../memory"))

# S3 Client Başlatma
if USE_S3:
    s3_client = boto3.client(
        "s3",
    )
else:
    # Yerel klasörü oluştur
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# LLM Ayarları (Senin Ollama Sunucun)
llm = ChatOllama(
    model="gemma3:27b",
    base_url=os.getenv("OLLAMA_BASE_URL"),
)

# --- VERİ MODELLERİ ---
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# --- HAFIZA YÖNETİM FONKSİYONLARI ---

def get_memory_path(session_id: str) -> str:
    """Dosya adını veya S3 key'ini döndürür"""
    return f"{session_id}.json"

def load_conversation(session_id: str) -> List[Dict]:
    """Geçmiş konuşmaları S3'ten veya yerelden yükler"""
    if USE_S3:
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=get_memory_path(session_id))
            return json.loads(response["Body"].read().decode("utf-8"))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return []
            print(f"S3 Read Error: {e}")
            return []
    else:
        # Yerel Dosya
        file_path = MEMORY_DIR / get_memory_path(session_id)
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Local Read Error: {e}")
                return []
        return []

def save_conversation(session_id: str, messages: List[Dict]):
    """Konuşmayı S3'e veya yerele kaydeder"""
    if USE_S3:
        try:
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=get_memory_path(session_id),
                Body=json.dumps(messages, indent=2, ensure_ascii=False),
                ContentType="application/json",
            )
        except Exception as e:
            print(f"S3 Write Error: {e}")
    else:
        # Yerel Dosya
        file_path = MEMORY_DIR / get_memory_path(session_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

# --- ENDPOINTLER ---

@app.get("/")
async def root():
    return {
        "message": "Mehmet Emin Baloğlu Digital Twin API",
        "model": "gemma3:27b",
        "storage": "S3" if USE_S3 else "Local Filesystem"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "use_s3": USE_S3}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Session ID oluşturma
        session_id = request.session_id or str(uuid.uuid4())
        
        # 1. Geçmişi EN BAŞTA yükle (Kod tekrarını önlemek için)
        conversation_history = load_conversation(session_id)
        
        # --- EASTER EGG KONTROLÜ (INTERCEPTOR) ---
        user_msg_clean = request.message.lower().strip()
        easter_eggs = facts.get("easter_eggs", {})
        
        if user_msg_clean in easter_eggs:
            egg_response = easter_eggs[user_msg_clean]
            
            # Hafızaya kaydet
            timestamp = datetime.now().isoformat()
            conversation_history.append({"role": "user", "content": request.message, "timestamp": timestamp})
            conversation_history.append({"role": "assistant", "content": egg_response, "timestamp": timestamp})
            save_conversation(session_id, conversation_history)
            
            # LLM'e gitmeden dön! 🚀
            return ChatResponse(response=egg_response, session_id=session_id)
        # ----------------------------------------

        # 2. LangChain Mesajlarını Hazırla
        current_system_prompt = prompt() 
        langchain_messages = [SystemMessage(content=current_system_prompt)]

        # --- KRİTİK DÜZELTME: Sadece son 10 mesajı al ---
        # Eski kodun: for msg in conversation_history: (Hafızayı patlatır)
        # Yeni kodun: conversation_history[-10:] (Güvenli)
        for msg in conversation_history[-10:]:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        # 3. Yeni kullanıcı mesajını ekle
        langchain_messages.append(HumanMessage(content=request.message))

        # 4. LLM'e Gönder (Ollama)
        response = llm.invoke(langchain_messages)
        assistant_response = response.content

        # 5. Hafızayı Güncelle
        timestamp = datetime.now().isoformat()
        conversation_history.append({
            "role": "user", 
            "content": request.message, 
            "timestamp": timestamp
        })
        conversation_history.append({
            "role": "assistant", 
            "content": assistant_response, 
            "timestamp": timestamp
        })

        # 6. Kaydet
        save_conversation(session_id, conversation_history)

        return ChatResponse(response=assistant_response, session_id=session_id)

    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def list_sessions():
    """Tüm oturumları listeler (Admin paneli için)"""
    sessions = []
    
    try:
        if USE_S3:
            # S3'teki dosyaları listele
            response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
            if "Contents" in response:
                for obj in response["Contents"]:
                    session_id = obj["Key"].replace(".json", "")
                    # Detayları çekmek maliyetli olabilir, sadece ID dönüyoruz
                    # İstersen burada her dosyayı okuyup özet de çıkarabilirsin
                    sessions.append({"session_id": session_id, "last_modified": obj["LastModified"]})
        else:
            # Yerel dosyaları listele
            for file_path in MEMORY_DIR.glob("*.json"):
                session_id = file_path.stem
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        last_msg = data[-1]["content"] if data else ""
                        sessions.append({
                            "session_id": session_id,
                            "message_count": len(data),
                            "last_message_snippet": last_msg[:50] + "..."
                        })
                except:
                    continue
                    
        return sessions

    except Exception as e:
        print(f"List Sessions Error: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)