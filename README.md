# MLOps Learning Journey 🚀

> **Status:** 🚧 Work in Progress

This repository contains scripts, projects, and experiments I've written during my MLOps (Machine Learning Operations) learning journey. The focus is on building production-ready AI applications using modern tools and frameworks.

## 📋 Overview

This repository is organized by weeks and days, with each day containing a complete project or exercise. Projects range from simple API integrations to full-stack applications with AI capabilities.

## 🎯 What You'll Find

- **FastAPI** ML model services
- **Next.js** frontend applications
- **Ollama** LLM integrations via LangChain
- **Vercel** deployment examples
- **Remote server** configurations
- **Full-stack** AI applications
- And more...

## 📁 Project Structure

```
.
├── week-1/
│   ├── day-1/                    # FastAPI + Ollama Remote Integration
│   │   ├── instant.py            # FastAPI app with HTML response
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── vercel.json           # Vercel configuration
│   │   └── README.md             # Detailed documentation
│   │
│   └── day-2/                    # Business Idea Generator (Full-Stack)
│       ├── saas/                 # Next.js + FastAPI application
│       │   ├── api/
│       │   │   └── index.py      # FastAPI backend endpoint
│       │   ├── pages/            # Next.js frontend pages
│       │   ├── requirements.txt  # Python dependencies
│       │   ├── package.json      # Node.js dependencies
│       │   └── vercel.json       # Vercel configuration
│       └── README.md             # Detailed documentation
│
└── README.md                      # This file
```

## 📚 Projects

### Week 1, Day 1: FastAPI + Ollama Remote Server Integration

**Description**: A simple FastAPI application that connects to a remote Ollama server using LangChain and returns dynamic HTML responses.

**Features**:
- FastAPI web server
- LangChain Ollama integration
- Remote Ollama server connection
- HTML response generation
- Vercel deployment

**Tech Stack**: FastAPI, LangChain, Ollama, Vercel

**Location**: [`week-1/day-1/`](./week-1/day-1/)

**Documentation**: See [week-1/day-1/README.md](./week-1/day-1/README.md)

---

### Week 1, Day 2: Business Idea Generator (Full-Stack)

**Description**: A full-stack application with Next.js frontend and FastAPI backend that generates AI-powered business ideas using a remote Ollama server.

**Features**:
- Next.js 16 frontend with React 19
- FastAPI backend API
- LangChain integration with remote Ollama
- Tailwind CSS styling
- TypeScript support
- Vercel zero-config deployment

**Tech Stack**: Next.js, React, FastAPI, LangChain, Ollama, Tailwind CSS, TypeScript, Vercel

**Location**: [`week-1/day-2/`](./week-1/day-2/)

**Documentation**: See [week-1/day-2/README.md](./week-1/day-2/)

---

## 🛠️ Technologies

### Backend
- **Python 3.8+** - Main backend language
- **FastAPI** - Modern, fast web framework
- **LangChain** - LLM framework for AI applications
- **langchain-ollama** - Ollama integration
- **Uvicorn** - ASGI server

### Frontend
- **Next.js 16** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Utility-first CSS framework

### AI/ML
- **Ollama** - Local/remote LLM runtime
- **gemma3:27b** - Google's Gemma 3 model (27B parameters)
- **LangChain** - LLM orchestration framework

### Deployment
- **Vercel** - Serverless deployment platform
- **Cloudflare Tunnel** - Remote server access

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.8+
- **Git** for version control
- **Vercel account** (for deployment)
- **Remote Ollama Server** (or use Cloudflare tunnel)

### Getting Started

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd instant
   ```

2. **Choose a project**
   - For Day 1: Navigate to `week-1/day-1/`
   - For Day 2: Navigate to `week-1/day-2/saas/`

3. **Follow project-specific README**
   - Each project has detailed setup instructions in its own README.md

## 📖 Learning Path

### Week 1: Foundation

- **Day 1**: Learn FastAPI basics and remote Ollama integration
- **Day 2**: Build a full-stack application with Next.js and FastAPI

### Future Weeks
- More projects and exercises will be added as the learning journey progresses

## 🔧 Common Setup

### Environment Variables

Most projects require the `OLLAMA_BASE_URL` environment variable:

```bash
# Set locally
export OLLAMA_BASE_URL="https://your-remote-ollama-server.com"

# Or in Vercel Dashboard
# Project Settings → Environment Variables
```

### Remote Ollama Server Setup

Projects use remote Ollama servers. You can:

1. **Use Cloudflare Tunnel** (Recommended for local development)
   ```bash
   cloudflared tunnel --url http://localhost:11434
   ```

2. **Use a VPS/Cloud Server** with Ollama installed

3. **Use a managed Ollama service** (if available)

## 📝 Notes

- This repository is continuously updated
- All code is written for learning purposes
- Improvement suggestions are welcome
- Each project is self-contained with its own documentation

## 🔄 Updates

### Week 1
- **Day 1** (✅ Complete): FastAPI + Ollama integration for using LLM through remote server
- **Day 2** (✅ Complete): Full-stack Business Idea Generator with Next.js frontend

## 🐛 Troubleshooting

### Common Issues

1. **Connection to Ollama Server**
   - Verify `OLLAMA_BASE_URL` is set correctly
   - Ensure the server is accessible
   - Check firewall/network settings

2. **Model Not Found**
   - Ensure the model is installed on the remote server
   - Run: `ollama pull gemma3:27b`

3. **Vercel Deployment**
   - Check build logs in Vercel dashboard
   - Verify all dependencies are in `requirements.txt`
   - Ensure environment variables are set

4. **Local Development**
   - Make sure all dependencies are installed
   - Check Python/Node.js versions
   - Verify port availability

## 📚 Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Vercel Documentation](https://vercel.com/docs)

### Learning Resources
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Learn](https://nextjs.org/learn)
- [LangChain Tutorials](https://python.langchain.com/docs/get_started/introduction)

## 🤝 Contributing

This is a personal learning repository, but suggestions and improvements are welcome!

## 📄 License

This project is for educational purposes. Feel free to use it as you wish.

## 🎓 Learning Outcomes

By working through these projects, you'll learn:

- How to build production-ready AI applications
- Serverless deployment with Vercel
- Remote LLM integration patterns
- Full-stack development with Next.js and FastAPI
- LangChain for LLM orchestration
- Environment variable management
- Modern web development practices

---

**Note**: This repository is actively being developed. It will be updated as new content is added.

**Status**: 🚧 Work in Progress - More projects coming soon!
