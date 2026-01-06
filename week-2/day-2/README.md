# Digital Twin Project (Week 2 - Day 2)

A "Digital Twin" AI application that simulates a professional persona based on provided context (facts, resume, style). It features a Next.js frontend and a FastAPI backend powered by Ollama (Gemma 3) with persistent memory capabilities.

## 🏗 Architecture

The system consists of a modern web frontend communicating with a Python-based REST API. The backend manages conversation state, builds context from static files, and interacts with a local LLM to generate responses.

```mermaid
graph TD
    Client[User / Client] -->|HTTP Request| Frontend[Next.js Frontend]
    Frontend -->|API Call /chat| Backend[FastAPI Backend]
    
    subgraph "Backend Processing"
        Backend -->|Check| EasterEgg[Easter Egg Interceptor]
        EasterEgg -- Match --> Response[Immediate Response]
        EasterEgg -- No Match --> Context[Context Construction]
        
        Context -->|Load Data| Resources[(Resources: Facts, CV, Style)]
        Context -->|Load History| Storage[Conversation Memory]
        
        Storage -.->|Read/Write| S3[AWS S3 Bucket]
        Storage -.->|Read/Write| Local[Local Filesystem]
        
        Context -->|Prompt + History| LLM[Ollama LLM (Gemma 3)]
        LLM -->|Generation| Backend
    end
    
    Response --> Frontend
    Backend -->|Final Response| Frontend
```

## 🚀 Features

-   **Digital Twin Persona**: Acts as a faithful representation of the user based on structured data (`facts.json`) and text files (`summary.txt`, `style.txt`).
-   **Persistent Memory**: Conversational history is automatically saved. It supports both local file storage and cloud storage via AWS S3 (configurable via environment variables).
-   **Easter Eggs**: Includes an interceptor layer that allows for pre-defined, instant responses to specific keywords, bypassing the LLM.
-   **Modern UI**: A responsive and clean chat interface built with Next.js and Tailwind CSS.

## 🛠 Tech Stack

-   **Frontend**: Next.js 16, React 19, Tailwind CSS 4, Lucide React
-   **Backend**: Python, FastAPI, LangChain, Boto3
-   **AI Model**: Gemma 3:27b (running locally via Ollama)
-   **Infrastructure**: AWS S3 (optional for storage), AWS Lambda ready

## 📸 Screenshots

Here is the application running, showing the chat interface and the Digital Twin's responses.

![Digital Twin Chat Interface](./twin/screenshots/06af13e5-5843-498e-a6a4-4923d64611a3.png)

## 🔗 Development Steps

This project was developed by following the comprehensive guide from the "Production" course (Week 2, Day 2). You can view the specific steps and the original tutorial here:

👉 [Week 2 - Day 2 Development Guide](https://github.com/ed-donner/production/blob/main/week2/day2.md)

## 🏃‍♂️ Running the Project

### Prerequisites
-   Python 3.11 or higher
-   Node.js 18 or higher
-   Ollama installed with `gemma3:27b` model pulled

### Backend
1.  Navigate to the backend directory:
    ```bash
    cd twin/backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the FastAPI server:
    ```bash
    python server.py
    ```
    The server will start at `http://localhost:8000`.

### Frontend
1.  Navigate to the frontend directory:
    ```bash
    cd twin/frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:3000`.
