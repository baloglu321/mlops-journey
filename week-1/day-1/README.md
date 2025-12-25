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

```
User Request → FastAPI → LangChain Ollama → Remote Ollama Server → LLM Response → HTML
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

Or in Vercel:
- Go to Project Settings → Environment Variables
- Add `OLLAMA_BASE_URL` with your server URL

### Model Configuration

The default model is `gemma3:27b`. To change it, modify line 16 in `instant.py`:

```python
model="your-model-name"
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

### Prerequisites

1. Vercel account
2. GitHub repository (optional, but recommended)
3. Remote Ollama server accessible via HTTPS

### Deployment Steps

1. **Push to GitHub** (if using Git integration)
   ```bash
   git add .
   git commit -m "Add FastAPI + Ollama integration"
   git push
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Or use Vercel CLI: `vercel`

3. **Set Environment Variable**
   - In Vercel Dashboard → Project Settings → Environment Variables
   - Add `OLLAMA_BASE_URL` with your remote Ollama server URL

4. **Deploy**
   - Vercel will automatically detect Python and deploy
   - Your app will be live at `your-project.vercel.app`

## 📝 Code Explanation

### Main Function Flow

```python
@app.get("/", response_class=HTMLResponse)
def instant():
    # 1. Get Ollama server URL from environment or use default
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", ".../")
    
    # 2. Initialize LangChain Ollama client
    llm = ChatOllama(
        model="gemma3:27b",
        base_url=ollama_base_url,
    )
    
    # 3. Create prompt
    message = "You are on a website that has just been deployed..."
    
    # 4. Invoke LLM
    response = llm.invoke(message)
    
    # 5. Format and return HTML
    reply = response.content.replace("\n", "<br/>")
    return html
```

## 🔍 Key Concepts Learned

1. **Serverless Deployment**: Deploying Python applications to Vercel
2. **Remote LLM Integration**: Connecting to external Ollama servers
3. **LangChain**: Using LangChain for LLM interactions
4. **FastAPI**: Creating simple web endpoints
5. **Environment Variables**: Managing configuration in serverless environments

## ⚠️ Important Notes

- **Remote Ollama Server**: This project requires a remote Ollama server. Local Ollama won't work on Vercel.
- **Timeout**: Vercel has timeout limits (60 seconds on free tier). LLM responses should be reasonably fast.
- **Cold Starts**: First request may be slower due to serverless cold starts.
- **Model Availability**: Ensure the specified model (`gemma3:27b`) is available on your remote Ollama server.

## 🐛 Troubleshooting

### Connection Errors

- Verify `OLLAMA_BASE_URL` is correctly set
- Ensure remote Ollama server is accessible
- Check if the server requires authentication

### Model Not Found

- Verify the model name is correct
- Ensure the model is pulled on the remote server: `ollama pull gemma3:27b`

### Timeout Issues

- LLM responses may take too long
- Consider using a faster/smaller model
- Optimize prompts for shorter responses

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Ollama](https://python.langchain.com/docs/integrations/llms/ollama)
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Ollama Documentation](https://ollama.ai/docs)

## 🎓 Learning Outcomes

After completing this project, you should understand:
- How to deploy FastAPI applications to Vercel
- How to integrate remote LLM services
- How to use LangChain for LLM interactions
- How to configure environment variables in serverless platforms
- Basic serverless architecture concepts

---

**Next Steps**: Consider adding error handling, multiple endpoints, or integrating with a database for more complex applications.

