# AI Digital Twin (Week 2 - Day 1)

> **Learning Focus**: Creating a persistent AI personality clone

Build your first AI Digital Twin! This project creates a chatbot that mimics a specific persona using memory and context management. The twin remembers conversations across sessions and responds in a consistent style based on personal data.

**Course Guide**: 👉 [Week 2 - Day 1: Build Your Digital Twin](https://github.com/ed-donner/production/blob/main/week2/day1.md)

## 🎯 What You'll Learn

- Creating persistent AI personalities
- Implementing conversation memory with file storage
- Building context from structured personal data
- Managing stateful AI interactions
- Developing persona-driven AI applications

## 📋 Overview

This project is an **AI Digital Twin** system designed to mimic a specific personality using a local LLM. It consists of a modern **Next.js** frontend and a robust **FastAPI** backend, leveraging **Ollama (Gemma 3 27B)** for AI processing and a file-based JSON system for persistent memory.

## 🏗️ Architecture

The system architecture features a decoupled frontend and backend. The React-based frontend handles user interactions and communicates with the FastAPI backend. The backend manages the conversation logic, integrates with the local Ollama LLM (Gemma 3), and handles persistent memory storage.

```mermaid
graph TD
    subgraph Frontend ["Frontend (Next.js)"]
        UI[User Interface]
        API_Client[API Client]
    end

    subgraph Backend ["Backend (FastAPI)"]
        API[API Endpoints]
        Logic[Conversation Logic]
        Mem_Mgr[Memory Manager]
    end

    subgraph External ["External Services/Storage"]
        Ollama["Ollama (Local LLM)"]
        FileSystem[("JSON Memory Files")]
    end

    User[User] -->|Interacts| UI
    UI -->|Sends Requests| API_Client
    API_Client -->|HTTP /chat| API
    API -->|Process| Logic
    Logic -->|Retrieve/Store| Mem_Mgr
    Mem_Mgr -->|Read/Write| FileSystem
    Logic -->|Generate Response| Ollama
```

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety

### Backend
- **FastAPI** - Python async API framework
- **LangChain** - LLM orchestration and conversation management
- **Ollama** - Local/Remote LLM runtime
- **Gemma 3 27B** - Language model (via Ollama)
- **Python 3.8+** - Runtime environment

### Storage
- **JSON Files** - Persistent conversation memory
- **File System** - Local storage for memory and context

### 🔄 Difference from Course

**Course Version**: May use OpenAI API  
**This Implementation**: Uses **Ollama** with **Gemma 3 27B** model

This demonstrates how to build digital twins with open-source models and local/remote inference.

## 🚀 Setup & Running

### Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **Ollama** installed and running with `gemma3:27b` model (or configure your own).

### 1. Backend (FastAPI)

Navigate to the backend directory and start the server:

```bash
cd twin/backend
# Install dependencies (if not using uv, use pip install -r requirements.txt)
uv run uvicorn server:app --reload
```
The backend will run at `http://localhost:8000`.

### 2. Frontend (Next.js)

Navigate to the frontend directory and start the development server:

```bash
cd twin/frontend
npm install
npm run dev
```
The frontend will run at `http://localhost:3000`.

## 📸 Screenshots

Here is a glimpse of the project running:

![AI Digital Twin Interface](twin/screenshots/06af13e5-5843-498e-a6a4-4923d64611a3.png)

## 🔗 References

- Based on the guide: [Week 2 Day 1 - Production Engineering](https://github.com/ed-donner/production/blob/main/week2/day1.md)

## 📂 Data Architecture (facts.json)

The application relies on a `facts.json` file to populate the Digital Twin's knowledge base. Since the original file contains personal data and may be removed, here is the expected structure for recreating it:

**File Path**: `twin/backend/data/facts.json`

| Top-Level Key | Type | Description |
| :--- | :--- | :--- |
| `profile` | Object | Contains personal details: `full_name`, `current_status`, `title`, `location`, `email`, `linkedin`, `github`, `summary`, `soft_skills` (List). |
| `technical_skills` | Object | Categorized skills: `languages`, `core_ds_libraries`, `computer_vision`, `llm_and_genai`, `mlops_and_infrastructure`, `ui_prototyping`. |
| `work_experience` | List[Object] | List of roles with: `company`, `role`, `dates`, `location`, `is_current` (Bool), `description`, `highlights` (List), `tech_stack` (List). |
| `projects` | List[Object] | Portfolio projects: `name`, `description`, `tags`, `url`, `info`. |
| `education` | List[Object] | Academic history: `degree`, `institution`, `year`, `gpa`. |
| `languages` | List[Object] | Spoken languages: `language`, `level`. |
| `personal_interests` | List[String] | Hobbies and interests. |
| `certificates` | List[Object] | Certifications: `name`, `issuer`, `date`, `url`, `tags`. |
| `easter_eggs` | Object | Key-value pairs for special trigger phrases and their corresponding custom responses. |

## 💡 Key Takeaways

- **Digital Twins**: AI that mimics specific personalities require structured context
- **Memory Management**: File-based storage provides simple persistence for conversations
- **Context Building**: Rich personal data creates more authentic responses
- **Persona Consistency**: System prompts and facts maintain character
- **Open Source Advantage**: Gemma 3 27B runs locally for privacy and control

## 📚 Additional Resources

- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama Documentation](https://ollama.ai/)
- [Course Guide - Week 2 Day 1](https://github.com/ed-donner/production/blob/main/week2/day1.md)

---

*Part of the AI in Production course - Week 2, Day 1*

