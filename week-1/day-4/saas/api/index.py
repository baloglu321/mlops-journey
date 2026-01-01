from fastapi import FastAPI, Depends  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama  # type: ignore
from langchain_core.messages import SystemMessage, HumanMessage
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


class Visit(BaseModel):
    patient_name: str
    date_of_visit: str
    notes: str


system_prompt = """
                        You are provided with notes written by a doctor from a patient's visit.
                        Your job is to summarize the visit for the doctor and provide an email.
                        Ensure that the 'Next steps' section is formatted as a markdown list using bullet points.
                        Reply with exactly three sections with the headings:
                        ### Summary of visit for the doctor's records
                        ### Next steps for the doctor
                        ### Draft of email to patient in patient-friendly language
                    """

def user_prompt_for(visit: Visit) -> str:
    return f"""Create the summary, next steps and draft email for:
Patient Name: {visit.patient_name}
Date of Visit: {visit.date_of_visit}
Notes:
{visit.notes}"""




@app.post("/api")
def consultation_summary(visit: Visit,creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]  # User ID from JWT - available for future use
    # 1. Ortam Değişkeni Kontrolü
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "...")

    # 2. LLM Ayarları
    llm = ChatOllama(
        model="gemma3:27b",
        base_url=ollama_base_url,
        temperature=0.7,
    )

    
    user_prompt = user_prompt_for(visit)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]


    async def event_stream():
        try:
           
            async for chunk in llm.astream(messages):
                content = chunk.content
                if content:
                   
                    safe_content = content.replace("\n", "\\n")
                    yield f"data: {safe_content}\n\n"
                    await asyncio.sleep(0)

            yield "data: [DONE]\n\n"
        except Exception as e:
            error_msg = str(e).replace("\n", " ")
            yield f"data: Error: {error_msg}\n\n"

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream",
        "X-Accel-Buffering": "no",
    }

    return StreamingResponse(
        event_stream(), headers=headers, media_type="text/event-stream"
    )
