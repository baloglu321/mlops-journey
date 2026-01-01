# MLOps Learning Journey 🚀

> **Status:** 🚧 Work in Progress (Week 1 Complete)

This repository contains scripts, projects, and experiments I've written during my MLOps (Machine Learning Operations) learning journey. The focus is on building production-ready AI applications using modern tools and frameworks.

## 📋 Overview

This repository is organized by weeks and days, with each day containing a complete project or exercise. Projects range from simple API integrations to full-stack applications with AI capabilities.

## 🗺️ Roadmap & Progress

```mermaid
mindmap
  root((MLOps Journey))
    Week 1: Foundations
      Day 1: FastAPI + Local LLM
      Day 2: Full Stack Idea Generator
      Day 3: Secure Auth & Streaming
      Day 4: Professional SaaS (Consultation Notes)
    Week 2: Advanced Usage
      (Coming Soon)
```

## 📚 Projects

### Week 1: Foundation (✅ Complete)

#### [Day 1: FastAPI + Ollama Integation](./week-1/day-1/)
**Goal**: Connect a local LLM to a web server.
- **Tech**: FastAPI, LangChain, Ollama
- **Outcome**: A simple API that generates dynamic HTML from LLM responses.

#### [Day 2: Business Idea Generator](./week-1/day-2/)
**Goal**: Build a full-stack AI application.
- **Tech**: Next.js, FastAPI, SSE (Server-Sent Events)
- **Outcome**: A web app that streams business ideas in real-time.

#### [Day 3: Secure AI SaaS](./week-1/day-3/saas/)
**Goal**: Add authentication and security.
- **Tech**: Clerk Auth, JWT Verification, Protected Streams
- **Outcome**: A secure multi-user AI application.

#### [Day 4: MediNotes Pro](./week-1/day-4/saas/)
**Goal**: Build a production-ready vertical SaaS.
- **Tech**: Next.js 14, TailwindCSS, Mermaid Charts, Structured Output
- **Outcome**: A polished tool for doctors to summarize patient notes.

---

## 🛠️ Technologies

### Backend
- **Python 3.10+** - Core logic
- **FastAPI** - High-performance API
- **LangChain** - LLM Orchestration
- **Ollama** - Local LLM Runtime (Gemma 2, Llama 3)

### Frontend
- **Next.js 16** - React Framework
- **Tailwind CSS 4** - Styling
- **Clerk** - Authentication
- **Mermaid.js** - Diagrams

### Deployment
- **Vercel** - Serverless Hosting
- **Cloudflare Tunnel** - Exposing local LLMs to the web

## 🚀 Quick Start

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd instant
    ```

2.  **Navigate to a project**
    ```bash
    cd week-1/day-4/saas
    ```

3.  **Follow the local README**
    Each project folder contains its own `README.md` with specific setup instructions.

## 📄 License

This project is for educational purposes. Feel free to use it as you wish.

---
*Created by [Your Name] as part of the MLOps Production Course.*
