# Business Idea Generator - Week 1 Day 2

AI-powered business idea generator that uses LangChain to connect to a remote Ollama server and generate creative business ideas using the `gemma3:27b` model. Added streaming.

## 🚀 Features

- **Next.js Frontend**: Modern React-based UI with Tailwind CSS
- **FastAPI Backend**: Python API endpoint for AI model interactions
- **LangChain Integration**: Seamless connection to remote Ollama server
- **Remote Ollama Support**: Connect to Ollama instances via Cloudflare tunnel or any remote server
- **Vercel Deployment**: Zero-config deployment on Vercel platform

## 📋 Tech Stack

### Frontend
- **Next.js 16.1.1** - React framework
- **React 19.2.3** - UI library
- **Tailwind CSS 4** - Styling
- **TypeScript 5** - Type safety

### Backend
- **FastAPI** - Python web framework
- **LangChain** - LLM framework
- **langchain-ollama** - Ollama integration
- **Uvicorn** - ASGI server

### AI Model
- **Ollama** - Local LLM runtime
- **gemma3:27b** - Google's Gemma 3 model (27B parameters)

## 🏗️ Project Structure

```
week-1/day-2/
├── saas/
│   ├── api/
│   │   └── index.py          # FastAPI endpoint
│   ├── pages/
│   │   ├── index.tsx          # Main page component
│   │   ├── _app.tsx           # Next.js app wrapper
│   │   └── _document.tsx      # HTML document structure
│   ├── styles/
│   │   └── globals.css        # Global styles
│   ├── requirements.txt       # Python dependencies
│   ├── package.json           # Node.js dependencies
│   └── vercel.json            # Vercel configuration (optional)
└── README.md                  # This file
```

## 🛠️ Setup & Installation

### Prerequisites

- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.8+
- **Ollama** installed and running (local or remote)
- **Remote Ollama Server** accessible via URL (e.g., Cloudflare tunnel)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd week-1/day-2/saas
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env.local` file or set environment variables:
   ```bash
   OLLAMA_BASE_URL=https://your-remote-ollama-server.com
   ```
   
   Or use the default in code (update `api/index.py` line 12-14).

5. **Run the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Configuration

### Remote Ollama Server Setup

The application connects to a remote Ollama server. You can configure it in two ways:

1. **Environment Variable** (Recommended)
   ```bash
   export OLLAMA_BASE_URL="https://your-remote-server.com"
   ```

2. **Direct Code Edit**
   Edit `saas/api/index.py` and update the default URL:
   ```python
   ollama_base_url = os.getenv(
       "OLLAMA_BASE_URL",
       "https://your-remote-server.com",  # Update this
   )
   ```

### Using Cloudflare Tunnel

If you're using Cloudflare tunnel to expose your local Ollama server:

```bash
# Install cloudflared
# Then run:
cloudflared tunnel --url http://localhost:11434
```

Use the generated URL as your `OLLAMA_BASE_URL`.

## 📡 API Endpoints

### GET `/api`
 
 Generates a new business idea using the AI model via Server-Sent Events (SSE).
 
 **Response**: text/event-stream
 
 **Example Stream**:
 ```
 data: Business Idea: "Symbiotic
 
 data:  Storytellers"
 
 data: [DONE]
 ```

## 🚀 Deployment

### Vercel Deployment

This project is configured for automatic deployment on Vercel:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect to Vercel**
   - Import your GitHub repository
   - Vercel will auto-detect Next.js and Python
   - Set environment variables in Vercel dashboard:
     - `OLLAMA_BASE_URL`: Your remote Ollama server URL

3. **Deploy**
   - Vercel will automatically build and deploy
   - No `vercel.json` needed (auto-detection works)

### Manual Deployment

If you need custom configuration, create `vercel.json`:

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api",
      "dest": "api/index.py"
    }
  ]
}
```

## 🧪 Testing

### Test the API Endpoint

```bash
# Local development
curl http://localhost:3000/api

# Production
curl https://your-vercel-app.vercel.app/api
```

### Test Frontend

1. Start the dev server: `npm run dev`
2. Open [http://localhost:3000](http://localhost:3000)
3. The page should automatically fetch and display a business idea

## 📝 Code Overview

### Backend (`api/index.py`)

```python
@app.get("/api")
async def idea():
    # ... setup code ...
    
    async def event_stream():
        async for chunk in llm.astream(prompt):
            content = chunk.content
            if content:
                safe_content = content.replace("\n", "\\n")
                yield f"data: {safe_content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(), 
        media_type="text/event-stream"
    )
```

### Frontend (`pages/index.tsx`)

- Fetches from `/api` endpoint on component mount
- Displays the generated idea in a styled card
- Handles loading and error states

## 🔒 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OLLAMA_BASE_URL` | Remote Ollama server URL | Yes | `"..."` (must be set) |

## 🐛 Troubleshooting

### Connection Issues

- **Error: Connection refused**
  - Check if your Ollama server is running
  - Verify the `OLLAMA_BASE_URL` is correct
  - Ensure the server is accessible from the deployment environment

### Model Not Found

- **Error: Model not found**
  - Ensure `gemma3:27b` is installed on your Ollama server
  - Run: `ollama pull gemma3:27b` on your remote server

### Vercel Deployment Issues

- **Build fails**
  - Check that `requirements.txt` includes all dependencies
  - Verify Python version compatibility
  - Check Vercel build logs for specific errors

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Vercel Deployment Guide](https://vercel.com/docs)

## 📄 License

This project is part of a learning exercise. Feel free to use and modify as needed.

## 👤 Author

Created as part of Week 1 Day 2 assignment.

---

**Note**: Make sure your remote Ollama server is running and accessible before deploying to production.

