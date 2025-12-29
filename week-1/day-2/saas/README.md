# Business Idea Generator (SaaS)

This is a full-stack AI application that generates unique business ideas using a remote Ollama server. It features a Next.js frontend with streaming responses (Server-Sent Events) and a FastAPI backend.

## 🚀 Technologies

- **Frontend**: Next.js 16 (React 19), Tailwind CSS 4, TypeScript
- **Backend**: FastAPI (Python), LangChain
- **AI**: Ollama (gemma3:27b) via remote connection

## 🛠️ Prerequisites

Before you begin, ensure you have:

- **Node.js** 18+ installed
- **Python** 3.8+ installed
- Access to a remote **Ollama** server (or a local one exposed via tunnel)

## 📦 Installation

1. **Install Frontend Dependencies:**

   ```bash
   npm install
   # or yarn install
   # or pnpm install
   ```

2. **Setup Python Environment:**

   It is recommended to use a virtual environment.

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Mac/Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env.local` file in this directory (or set system environment variables):

```bash
# URL to your remote Ollama server
OLLAMA_BASE_URL="https://your-remote-server-url.com"
```

> **Note**: If testing locally with Cloudflare Tunnel, run `cloudflared tunnel --url http://localhost:11434` and use the resulting URL.

## 🏃‍♂️ Running Locally

This project uses a hybrid Next.js + FastAPI approach meant for Vercel deployment. To run it locally, you have two options:

### Option 1: Using Vercel CLI (Recommended)

This mimics the production environment perfectly.

1. Install Vercel CLI: `npm i -g vercel`
2. Run development server:
   ```bash
   vercel dev
   ```
3. Open `http://localhost:3000`

### Option 2: Split Terminal

You can run the backend and frontend separately (requires manual port configuration usually, but for simple inspection):

**Terminal 1 (Frontend):**
```bash
npm run dev
```

**Terminal 2 (Backend):**
```bash
# Note: Next.js won't proxy to this automatically without configuration
# This is mostly for testing the API processing in isolation
uvicorn api.index:app --reload --port 8000
```

*For a fully integrated local experience without Vercel CLI, you would need to add rewrites to `next.config.ts` pointing `/api/:path*` to `http://127.0.0.1:8000/api/:path*`.*

## 🚀 Deployment to Vercel

1. Push this code to GitHub.
2. Import the project in Vercel.
3. Add the `OLLAMA_BASE_URL` environment variable.
4. Deploy! Vercel automatically detects the Python API and Next.js frontend.
