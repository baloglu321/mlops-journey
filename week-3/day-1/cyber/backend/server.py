import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List
from agents import Agent, Runner, trace
import openai
from context import SECURITY_RESEARCHER_INSTRUCTIONS, get_analysis_prompt, enhance_summary
from mcp_servers import create_semgrep_server


openai.api_key = os.getenv("OPENAI_API_KEY", "ollama")
openai.base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")

load_dotenv()

app = FastAPI(title="Cybersecurity Analyzer API")

# Configure CORS for development and production
cors_origins = [
    "http://localhost:3000",    # Local development
    "http://frontend:3000",     # Docker development
]

# In production, allow same-origin requests (static files served from same domain)
if os.getenv("ENVIRONMENT") == "production":
    cors_origins.append("*")  # Allow all origins in production since we serve frontend from same domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    code: str


class SecurityIssue(BaseModel):
    title: str = Field(description="Brief title of the security vulnerability")
    description: str = Field(
        description="Detailed description of the security issue and its potential impact"
    )
    code: str = Field(
        description="The specific vulnerable code snippet that demonstrates the issue"
    )
    fix: str = Field(description="Recommended code fix or mitigation strategy")
    cvss_score: float = Field(description="CVSS score from 0.0 to 10.0 representing severity")
    severity: str = Field(description="Severity level: critical, high, medium, or low")


class SecurityReport(BaseModel):
    summary: str = Field(description="Executive summary of the security analysis")
    issues: List[SecurityIssue] = Field(description="List of identified security vulnerabilities")


def validate_request(request: AnalyzeRequest) -> None:
    """Validate the analysis request."""
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="No code provided for analysis")





def create_security_agent(semgrep_server) -> Agent:
    """Create and configure the security analysis agent."""
    return Agent(
        name="Security Researcher",
        instructions=SECURITY_RESEARCHER_INSTRUCTIONS,
        
        # Sadece model ismini string olarak veriyoruz.
        # Kütüphane URL ve Key'i .env dosyasından alacak.
        model="gemma3:27b",
        
        mcp_servers=[semgrep_server],
        #output_type=SecurityReport,
    )

def check_api_keys() -> None:
    """Verify required configuration."""
    # Ollama kullanırken key zorunlu değildir ama URL zorunludur.
    if not os.getenv("OLLAMA_API_URL"):
         # Varsayılan olarak localhost'a fallback yapabilir veya hata fırlatabilirsiniz
         print("Warning: OLLAMA_API_URL not set, defaulting to localhost")


async def run_security_analysis(code: str) -> SecurityReport:
    """Execute the security analysis workflow."""
    
    # 'trace' bloğunu kaldırdık (401 hatası gitmesi için)
    async with create_semgrep_server() as semgrep:
        agent = create_security_agent(semgrep)
        
        # Prompt'a JSON zorunluluğunu metin olarak ekliyoruz
        prompt = f"""
        {get_analysis_prompt(code)}
        
        IMPORTANT: You must return the result strictly in valid JSON format.
        Do not include markdown formatting (like ```json). 
        The JSON must match this structure:
        {{
            "summary": "Executive summary here...",
            "issues": [
                {{
                    "title": "Issue title",
                    "description": "Details...",
                    "code": "Vulnerable code snippet",
                    "fix": "Fixed code",
                    "cvss_score": 7.5,
                    "severity": "high"
                }}
            ]
        }}
        """
        
        # Agent'ı çalıştır
        result = await Runner.run(agent, input=prompt)
        
        # Extract response from raw_responses since final_output is empty with Ollama
        response_text = ""
        if result.raw_responses and len(result.raw_responses) > 0:
            response = result.raw_responses[0]
            if hasattr(response, 'output') and response.output:
                # output is a list of ResponseOutputMessage objects
                if len(response.output) > 0 and hasattr(response.output[0], 'content'):
                    response_text = response.output[0].content
                    print(f"✅ Extracted {len(response_text)} characters from raw_responses")
        
        if not response_text:
            print("⚠️ No response text found, falling back to final_output")
            response_text = result.final_output
        
        # Bazen modeller ```json ... ``` içinde verir, temizleyelim
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        print(f"🔍 Final response_text length: {len(response_text)}")
        print(f"🔍 First 200 chars: {response_text[:200]}")
            
        try:
            import json
            data = json.loads(response_text)
            # JSON verisini Pydantic modeline çevir
            return SecurityReport(**data)
        except Exception as e:
            print(f"JSON Parse Hatası. Gelen Veri: {response_text}")
            print(f"Hata detayı: {str(e)}")
            # Hata durumunda boş rapor dön
            return SecurityReport(summary="Analiz sonucu işlenemedi.", issues=[])


def format_analysis_response(code: str, report: SecurityReport) -> SecurityReport:
    """Format the final analysis response."""
    enhanced_summary = enhance_summary(len(code), report.summary)
    return SecurityReport(summary=enhanced_summary, issues=report.issues)


@app.post("/api/analyze", response_model=SecurityReport)
async def analyze_code(request: AnalyzeRequest) -> SecurityReport:
    """
    Analyze Python code for security vulnerabilities using OpenAI Agents and Semgrep.

    This endpoint combines static analysis via Semgrep with AI-powered security analysis
    to provide comprehensive vulnerability detection and remediation guidance.
    """
    validate_request(request)
    check_api_keys()

    try:
        report = await run_security_analysis(request.code)
        return format_analysis_response(request.code, report)
    except Exception as e:
        # BU SATIRI EKLE: Hatayı terminale yazdır
        import traceback
        traceback.print_exc() 
        print(f"KRİTİK HATA DETAYI: {str(e)}")
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"message": "Cybersecurity Analyzer API"}

@app.get("/network-test")
async def network_test():
    """Test network connectivity to Semgrep API."""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://semgrep.dev/api/v1/")
            return {
                "semgrep_api_reachable": True,
                "status_code": response.status_code,
                "response_size": len(response.content)
            }
    except Exception as e:
        return {
            "semgrep_api_reachable": False,
            "error": str(e)
        }

@app.get("/semgrep-test")
async def semgrep_test():
    """Test if semgrep CLI can be installed and run."""
    import subprocess
    import tempfile
    import os
    
    try:
        # Test if we can install semgrep via pip
        result = subprocess.run(
            ["pip", "install", "semgrep"], 
            capture_output=True, 
            text=True, 
            timeout=60
        )
        
        if result.returncode != 0:
            return {
                "semgrep_install": False,
                "error": f"Install failed: {result.stderr}"
            }
        
        # Test if semgrep --version works
        version_result = subprocess.run(
            ["semgrep", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        return {
            "semgrep_install": True,
            "version_check": version_result.returncode == 0,
            "version_output": version_result.stdout,
            "version_error": version_result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            "semgrep_install": False,
            "error": "Timeout during semgrep installation or version check"
        }
    except Exception as e:
        return {
            "semgrep_install": False,
            "error": str(e)
        }

# Mount static files for frontend
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
