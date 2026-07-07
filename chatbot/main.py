# Import FastAPI
from fastapi import FastAPI, UploadFile, File
# Import CORS Middleware
from fastapi.middleware.cors import CORSMiddleware
# Import BaseModel from Pydantic
import time
from pydantic import BaseModel
# OpenRouter Client
from openai import OpenAI
# Load environment variables
from dotenv import load_dotenv
# Read environment variables
import os
# Import Retriever
from chatbot.retriever import retrieve_context

# Create FastAPI app
app = FastAPI()
# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load .env file
load_dotenv()
# Read API Key
api_key = os.getenv("OPENROUTER_API_KEY")
# Read Model Name
model = os.getenv("OPENROUTER_MODEL")

# Create OpenRouter Client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Store conversation history
chat_history = [
    {
        "role": "system",
        "content": (
            "You are an Enterprise AI Knowledge Assistant.\n"
            "Answer the user's question only using the provided context.\n"
            "If the answer is not present in the context, clearly state that the information is not available in the provided document.\n"
            "Do not make up or assume information.\n"
            "Provide clear, professional and concise responses."
        )
    }
]
# Request Model
class ChatRequest(BaseModel):
    question: str
# Home Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise AI Knowledge Assistant!"
    }

# Health Endpoint
@app.get("/health")
def health_check():
    return {
        "status": "Backend Running Successfully",
        "version": "1.0.0"
    }


# About Endpoint
@app.get("/about")
def about():
    return {
        "name": "Enterprise AI Knowledge Assistant",
        "framework": "FastAPI",
        "frontend": "Next.js",
        "backend": "Python",
        "database": "ChromaDB",
        "AI Model": "OpenRouter"
    }
# Upload PDF Endpoint
@app.post("/upload")
async def upload_pdf(pdf: UploadFile = File(...)):

    # Save uploaded PDF
    file_path = f"data/{pdf.filename}"

    with open(file_path, "wb") as file:
        file.write(await pdf.read())

    return {
        "message": "PDF uploaded successfully",
        "filename": pdf.filename
    }

# Chat Endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    # Get user's question
    user_question = request.question
    # Measure retriever time
    start = time.time()
    # Retrieve relevant document context
    context, retrieved_metadata = retrieve_context(
        user_question,
        source="HR_Policy_Manual.pdf"
    )
    print("Retriever Time:", time.time() - start)
    # Add context and question to conversation history
    chat_history.append(
        {
            "role": "user",
            "content": f"""
        Context:
        {context}
        Question:
        {user_question}
        """
        }
    )
    # Measure OpenRouter time
    start = time.time()
    # Generate AI response
    response = client.chat.completions.create(
        model=model,
        messages=chat_history
    )
    print("OpenRouter Time:", time.time() - start)
    # Extract AI response
    ai_response = response.choices[0].message.content
    # Save AI response
    chat_history.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )
    # Return response
    return {
        "question": user_question,
        "answer": ai_response
    }