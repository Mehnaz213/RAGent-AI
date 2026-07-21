<h1 align="center">
🤖 RAGent AI — Enterprise Knowledge Assistant
</h1>

<p align="center">
An enterprise-grade Retrieval-Augmented Generation (RAG) assistant that enables employees to retrieve accurate information from organizational documents using AI-powered semantic search, vector embeddings, and Large Language Models.
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi"/>

<img src="https://img.shields.io/badge/Next.js-Frontend-black?style=for-the-badge&logo=nextdotjs"/>

<img src="https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge&logo=react"/>

<img src="https://img.shields.io/badge/TailwindCSS-UI-38B2AC?style=for-the-badge&logo=tailwind-css"/>

<img src="https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/LangChain-RAG-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/HuggingFace-Embeddings-yellow?style=for-the-badge"/>

<img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite"/>

<img src="https://img.shields.io/badge/JWT-Authentication-red?style=for-the-badge"/>

<img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge"/>

</p>

---

# 📖 Overview

RAGent AI is an Enterprise AI Knowledge Assistant that enables employees to retrieve accurate information from organizational documents using natural language.

The system combines Retrieval-Augmented Generation (RAG), semantic search, vector embeddings, and Large Language Models (LLMs) to deliver context-aware answers with source citations.

Beyond traditional RAG, RAGent AI now includes an Agentic AI layer capable of planning user requests, selecting appropriate tools, executing multi-step workflows, and displaying its reasoning process through an Agent Execution interface.

Administrators can securely manage users, upload organizational documents, monitor analytics, and maintain the enterprise knowledge base, while employees can interact with an intelligent AI assistant to instantly access company knowledge.
---

# ✨ Features

### 🤖 AI Assistant

- Enterprise RAG Chatbot
- Semantic Document Search
- Context-Aware Responses
- Source Citations
- Persistent Conversations
- Agentic AI Planning
- Multi-Step Task Execution
- AI-Powered Document Generation

### 📚 Knowledge Base

- Upload PDF Documents
- Automatic Text Chunking
- Embedding Generation
- ChromaDB Vector Storage
- Document Search
- Delete Documents

### 👥 User Management

- JWT Authentication
- Admin & Employee Roles
- Role-Based Access Control
- Password Management
- User Creation

### 📈 Analytics

- Total Users
- Total Conversations
- Total Messages
- Recent Conversations

### 💬 Chat Management

- New Chat
- Chat History
- Conversation Search
- Rename Conversations
- Delete Conversations

### 🎨 UI Features

- Responsive Design
- Dark / Light Theme
- Modern Enterprise Dashboard
- Professional Admin Panel

---

# 🤖 Agentic AI Features

Unlike a traditional RAG chatbot, RAGent AI includes an AI Agent capable of reasoning, selecting tools, and executing multi-step workflows automatically.

### 📄 AI Document Generation

The AI Agent can automatically generate professional business documents based on user requests.

Supported document types include:

- Professional Emails
- Leave Applications
- Business Letters
- Enterprise Reports
- Official Notices
- Project Proposals

The agent selects the appropriate document generation tool automatically based on the user's request.

### 🧠 Agent Planner

- Understands user intent
- Chooses the appropriate tools
- Plans multi-step execution
- Displays execution reasoning

### 🛠 Available AI Tools

- Knowledge Search
- Email Generator
- Leave Application Generator
- Letter Generator
- Report Generator
- Notice Generator
- Proposal Generator
- Document Summarizer
- Professional Text Rewriter
- Policy Comparison

### ⚡ Multi-Step Execution

Example:

```text
User
↓

Summarize the Leave Policy
and generate an email requesting leave

↓

Knowledge Search

↓

Summarization

↓

Email Generation

↓

Final Response
```
### Example

```text
User

↓

Generate a report on the Employee Handbook

↓

Knowledge Search

↓

Report Generation

↓

Professional Report
```


Every execution step is displayed to the user through the **Agent Execution** panel.

# 🏗️ System Architecture

```text
                          User
                            │
                            ▼
                   Next.js Frontend
                            │
                            ▼
                    FastAPI Backend
                            │
                            ▼
                    AI Agent Planner
                            │
             Intent Detection & Task Planning
                            │
                            ▼
                 Multi-Tool Orchestrator
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
      ▼                     ▼                     ▼
Knowledge Search     Document Generation   Text Processing
      │                     │                     │
      │        ┌────────────┼─────────────┐       │
      │        ▼            ▼             ▼       ▼
      │     Emails       Letters      Reports  Rewrite
      │        │            │             │
      │        ▼            ▼             ▼
      │     Notices    Leave Apps    Proposals
      │
      ▼
ChromaDB Vector Database
      │
      ▼
Semantic Search & Retrieval
      │
      ▼
Retrieved Context
      │
      ▼
Large Language Model
      │
      ▼
Context-Aware Final Response
```

## AI Stack

- Retrieval-Augmented Generation (RAG)
- OpenRouter LLM
- Sentence Transformers
- Cross Encoder Re-ranking
- ChromaDB
- Hugging Face Embeddings
- PyPDF
- Agent Planner
- Multi-tool Orchestration
  
# 📸 Screenshots

## 🔐 Login

![Login](assets/login.png)

---

## 💬 AI Chat

![Chat](assets/chat.png)

---

# 🤖 Agentic AI Workflow

RAGent AI goes beyond traditional Retrieval-Augmented Generation by incorporating an AI Agent capable of reasoning, planning, and executing multiple tools automatically to complete complex user requests.

### Step 1 — Planning & Task Decomposition

The user submits a complex request that requires multiple capabilities.

**Example Request**

> Summarize the leave policy and write an email requesting leave.

The Agent Planner analyzes the request and determines which tools should be executed in sequence.

**Tools Selected**

- Knowledge Search
- Summarization
- Email Generation

The complete execution process is displayed transparently through the **Agent Execution** panel.

![Agent Planning](assets/agent-execution-1.png)

---

### Step 2 — Knowledge Retrieval & Reasoning

The AI Agent retrieves the relevant information from the enterprise knowledge base using Retrieval-Augmented Generation (RAG), performs semantic search over indexed company documents, and generates a concise summary of the retrieved policy before continuing to the next task.

This intermediate reasoning step allows users to understand how the final answer is produced rather than treating the system as a black box.

![Knowledge Retrieval](assets/agent-execution-2.png)

---

### Step 3 — Final Response Generation

Using the summarized organizational knowledge, the AI Agent automatically generates a professional leave request email.

The entire workflow—from retrieving company policies to producing the final email—is completed within a single conversation without requiring additional user interaction.

This demonstrates the system's ability to orchestrate multiple AI tools and complete complex enterprise tasks autonomously.

![Final Response](assets/agent-execution-3.png)

---

---

## 🕒 Chat History

Search, rename, export, and delete previous conversations.

![History](assets/history.png)

---

## ⚙️ Settings

### Profile Information

![Profile](assets/settings-profile.png)

### Change Password

![Password](assets/settings-password.png)

### User Management (Admin)

![User Management](assets/settings-user-management.png)

---

## 📚 Knowledge Base

Upload PDFs, view indexed documents, monitor chunk count, and manage the enterprise knowledge base.

![Knowledge Base](assets/knowledge-base.png)

---

## 📊 Analytics Dashboard

Monitor users, conversations, messages, and recent activity.

![Analytics](assets/analytics.png)
# 📂 Project Structure

```text
AI-Knowledge-Assistant/

│

├── chatbot/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── security.py
│   ├── build_database.py
│   └── ...

├── data/
│   ├── Employee_Handbook.pdf
│   ├── document_metadata.json
│   └── ...

├── vector_db/

├── frontend/
│   ├── app/
│   ├── components/
│   └── ...

├── requirements.txt

└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Mehnaz213/AI-Knowledge-Assistant.git

cd AI-Knowledge-Assistant
```

---

## Backend

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn chatbot.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🚀 Future Improvements

- Multi-Agent Collaboration
- Long-Term Agent Memory
- Workflow Automation Agent
- Calendar Integration
- Outlook & Gmail Integration
- Slack & Microsoft Teams Integration
- Voice-Based Enterprise Assistant
- HR Workflow Automation
- IT Support Agent
- SQL Database Agent
- Cloud Deployment

---

# 👩‍💻 Author

**Fathimath Mehnaaz**

Artificial Intelligence & Machine Learning Engineering Student

GitHub:
https://github.com/Mehnaz213

LinkedIn:
https://www.linkedin.com/in/fathimath-mehnaaz/
