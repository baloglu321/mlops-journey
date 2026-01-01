# Week 1, Day 1: FastAPI + Ollama Remote Server Integration

## 📋 Overview

This project demonstrates how to create a FastAPI web application that connects to a remote Ollama server using LangChain. The application generates dynamic HTML responses using an LLM (Large Language Model) hosted on a remote server.

## 🎯 What This Project Does

- Creates a FastAPI web server
- Connects to a remote Ollama server via LangChain
- Sends a prompt to the LLM asking for an enthusiastic production deployment announcement
- Returns the LLM's response as formatted HTML
- Deploys to Vercel for public access

## 🏗️ Architecture

```mermaid
flowchart LR
    %% Nodes
    User([User])
    Vercel[Vercel Serverless Function]
    LC[LangChain Client]
    Ollama[("Remote Ollama Server")]

    %% Flow
    User -->|1. Request| Vercel
    Vercel -->|2. Invoke| LC
    
    subgraph "Remote / Cloud"
        LC <-->|3. HTTPS / LLM Response| Ollama
    end

    Vercel -.->|4. HTML Response| User
```

## 📁 Files

- **`instant.py`** - Main FastAPI application with Ollama integration
- **`requirements.txt`** - Python dependencies
- **`vercel.json`** - Vercel deployment configuration

## 🛠️ Technologies Used

- **FastAPI** - Modern Python web framework
- **LangChain Ollama** - LangChain integration for Ollama LLM
- **Ollama** - Local/remote LLM server (gemma3:27b model)
- **Vercel** - Serverless deployment platform

## ⚙️ Configuration

### Environment Variables

Set the `OLLAMA_BASE_URL` environment variable to point to your remote Ollama server:

```bash
export OLLAMA_BASE_URL="https://your-ollama-server.com"
```

## 🚀 Local Development

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Set Environment Variable

```bash
# Windows PowerShell
$env:OLLAMA_BASE_URL="https://your-ollama-server.com"

# Linux/Mac
export OLLAMA_BASE_URL="https://your-ollama-server.com"
```

### 3. Run Locally

```bash
uvicorn instant:app --reload
```

Access at: `http://localhost:8000`

## 🌐 Vercel Deployment

This project is configured for easy deployment on Vercel.

### Prerequisites

1.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2.  **Remote Ollama Server**: You need an Ollama server running and accessible via HTTPS (e.g., using Cloudflare Tunnel).

### Deployment Steps

1.  **Install Vercel CLI** (Optional but recommended)
    ```bash
    npm install -g vercel
    ```

2.  **Deploy via Terminal**
    Run the following command in the project directory:
    ```bash
    vercel
    ```
    - Follow the prompts (Keep default settings).
    - **Important**: When asked for environment variables, add:
        - Key: `OLLAMA_BASE_URL`
        - Value: `https://your-remote-ollama-url.com`

3.  **Deploy via Dashboard (Alternative)**
    - Push this code to a GitHub repository.
    - Import the repository in Vercel.
    - In "Environment Variables" section, add `OLLAMA_BASE_URL`.
    - Click "Deploy".

### `vercel.json` Configuration

The project includes a `vercel.json` file to configure the Python runtime:

```json
{
    "builds": [
        {
            "src": "instant.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "instant.py"
        }
    ]
}
```

## 🐛 Troubleshooting

### Connection Errors
- **Error: Connection refused**: Ensure your remote Ollama server is running and the `OLLAMA_BASE_URL` is correct.
- **Error: 504 Gateway Timeout**: Vercel Serverless Functions have a default timeout (10s on Hobby). If the LLM takes longer, you might need to optimize the prompt or use a faster model.

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [LangChain Ollama](https://python.langchain.com/docs/integrations/llms/ollama)
