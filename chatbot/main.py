# Import FastAPI
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query
)
# Import CORS Middleware
from fastapi.middleware.cors import CORSMiddleware
# Import BaseModel from Pydantic
from pydantic import BaseModel
# Import complete PDF ingestion pipeline
from chatbot.pdf_processor import ingest_pdf
# Import database engine and Base
from chatbot.database import engine, Base
# Import User model
from chatbot.models import (
    User,
    Conversation,
    Message
)
from sqlalchemy.orm import Session
from chatbot.database import get_db
# Import authentication router
from chatbot.auth import router as auth_router
# Import authentication dependency
from chatbot.dependencies import get_current_user
# Import Depends
from fastapi import Depends
from fastapi.responses import FileResponse, StreamingResponse
from chatbot.security import (
    verify_access_token,
    verify_password,
    hash_password
)
from chatbot.paths import DATA_FOLDER
from chatbot.spell_checker import correct_spelling
from chatbot.query_rewriter import rewrite_query
from chatbot.export_chat import export_pdf
from chatbot.title_generator import generate_title
import json
import shutil
import subprocess
import os
# Import Agent Orchestrator
from chatbot.agent.orchestrator import process_user_request
from chatbot.rag import generate_rag_answer

DATA_FOLDER = "data"
# Create FastAPI app
app = FastAPI()
# Create database tables
Base.metadata.create_all(bind=engine)
# Register authentication routes
app.include_router(auth_router)
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

# Request Model
class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

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
        "AI Model": "Gemini 2.5 Flash"
    }
# Download PDF
@app.get("/download/{filename}")
def download_document(
    filename: str,
    token: str = Query(...)
):
    # Verify JWT Token
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    # Create full file path
    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    # Check whether file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Send PDF to browser
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )

# Upload PDF Endpoint
@app.post("/upload")
async def upload_pdf(
    pdf: UploadFile = File(...),
    # Get current user dependency
    current_user: dict = Depends(get_current_user)
):
    # Save uploaded PDF
    file_path = os.path.join(
    DATA_FOLDER,
    pdf.filename
   )

    with open(file_path, "wb") as file:
        file.write(await pdf.read())
    # Process the uploaded PDF completely
    ingest_pdf(file_path)
    return {
    "message": "Document indexed successfully",
    "filename": pdf.filename
    }

# Get all uploaded PDF documents
@app.get("/documents")
def get_documents(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    metadata_file = os.path.join(
        DATA_FOLDER,
        "document_metadata.json"
    )

    with open(metadata_file, "r") as file:

        documents = json.load(file)

    return documents

@app.delete("/documents/{filename}")
def delete_document(
    filename: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    pdf_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    if not os.path.exists(pdf_path):

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    os.remove(pdf_path)

    metadata_file = os.path.join(
        DATA_FOLDER,
        "document_metadata.json"
    )

    with open(metadata_file, "r") as file:

        metadata = json.load(file)

    metadata = [
        doc
        for doc in metadata
        if doc["name"] != filename
    ]

    with open(metadata_file, "w") as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    return {
        "message": "Document deleted successfully."
    }

@app.get("/conversations")
def get_conversations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == current_user["email"])
        .first()
    )

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": c.created_at
        }
        for c in conversations
    ]

@app.post("/conversation/new")
def create_conversation(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == current_user["email"])
        .first()
    )

    conversation = Conversation(

        title="New Chat",

        user_id=user.id

    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return {

        "conversation_id": conversation.id

    }


@app.get("/conversation/{conversation_id}")
def get_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    messages = (
       db.query(Message)
       .filter(
           Message.conversation_id == conversation.id
        )
       .order_by(Message.id.asc())
       .all()
    )
    for m in messages:
      print(m.content[:30], m.timestamp)
    return {
       "id": conversation.id,
       "title": conversation.title,
       "messages": [
          {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp,
            "sources": m.sources,
            "agent": m.agent
          }
        for m in messages
      ]
    }

@app.put("/conversation/{conversation_id}/title")
def update_conversation_title(
    conversation_id: int,
    title: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    conversation.title = title

    db.commit()

    return {
        "message": "Conversation title updated."
    }


@app.delete("/conversation/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    db.delete(conversation)

    db.commit()

    return {
        "message": "Conversation deleted successfully."
    }

@app.put("/conversation/{conversation_id}/rename")
def rename_conversation(
    conversation_id: int,
    title: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    conversation.title = title

    db.commit()

    return {
        "message": "Conversation renamed successfully."
    }

# Chat Endpoint
@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's question
    original_question = request.question
    user_question = correct_spelling(original_question)
    conversation = db.query(Conversation).filter(
       Conversation.id == request.conversation_id
    ).first()
    if conversation is None:
      raise HTTPException(
        status_code=404,
        detail="Conversation not found."
    )
    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(Message.id.asc())
        .all()
    )
    conversation_messages = []

    # Keep only the last 8 messages
    previous_messages = previous_messages[-8:]

    for msg in previous_messages:

        conversation_messages.append(
            {
               "role": msg.role,
               "content": msg.content
            }
        )

    # Ask the Agent which tool should handle the request
    agent_response = process_user_request(
       user_question,
       conversation_messages
    )

    # Get the execution plan
    tools = agent_response["tools"]

    # Get the final agent result
    result = agent_response["result"]

    # If Knowledge Search is NOT required,
    # save the response and return it.
    if "knowledge_search" not in tools:

        user_message = Message(

           role="user",

           content=original_question,

           conversation_id=conversation.id

        )

        db.add(user_message)

        assistant_message = Message(

           role="assistant",

           content=result,

           conversation_id=conversation.id,

           sources=[],

           agent={
              "tools": tools,
              "steps": agent_response["steps"]
           }

        )

        db.add(assistant_message)

        if conversation.title == "New Chat":

           try:

              conversation.title = generate_title(original_question)

           except Exception:

              conversation.title = original_question[:40]

        db.commit()

        return {

           "answer": result,

           "sources": [],

           "agent": {

              "tools": tools,

              "steps": agent_response["steps"]

           }

        }
    
    db.add(
       Message(
        role="user",
        content=original_question,
        conversation_id=conversation.id
       )
    )
    if conversation and conversation.title == "New Chat":

      try:
        conversation.title = generate_title(original_question)
      except Exception:
        conversation.title = original_question[:40]

    db.commit()

    try:
      rewritten_question = rewrite_query(
        user_question,
        conversation_messages
    )
    except Exception as e:
      print("Query rewriter failed:", e)
      rewritten_question = user_question

    print("Original:", user_question)
    print("Rewritten:", rewritten_question)
    print("Logged in User:", current_user["email"])
    print("Role:", current_user["role"])
    
    # Generate RAG response
    ai_response, retrieved_metadata = generate_rag_answer(
      question=rewritten_question,
      conversation_messages=conversation_messages
    )
    if conversation:

      assistant_message = Message(

        role="assistant",

        content=ai_response,

        conversation_id=conversation.id,

        sources=retrieved_metadata,

        agent={
           "tools": tools,
           "steps": agent_response["steps"]
        }

    )
      db.add(assistant_message)
      db.commit()

    # Return response along with source metadata
    return {

      "question": user_question,

      "answer": ai_response,

      "sources": retrieved_metadata,

      "timestamp": assistant_message.timestamp,

      "agent": {

         "tools": tools,

         "steps": agent_response["steps"]

       }
    }
@app.get("/users")
def get_users(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]
@app.get("/conversation/{conversation_id}/export/pdf")
def export_conversation_pdf(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
    User.email == current_user["email"]
    ).first()

    conversation = (
      db.query(Conversation)
        .filter(
           Conversation.id == conversation_id,
           Conversation.user_id == user.id
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found."
        )

    pdf = export_pdf(conversation.messages)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f'attachment; filename="{conversation.title}.pdf"'
        }
    )

@app.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == current_user["email"])
        .first()
    )

    if not verify_password(
        request.current_password,
        user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

    user.password = hash_password(
        request.new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully."
    }
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if user.email == current_user["email"]:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account."
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully."
    }
@app.get("/analytics")
def analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    total_users = db.query(User).count()

    total_conversations = db.query(Conversation).count()

    total_messages = db.query(Message).count()

    recent_conversations = (
        db.query(Conversation)
        .order_by(Conversation.created_at.desc())
        .limit(5)
        .all()
    )

    recent = []

    for conversation in recent_conversations:

        recent.append(
            {
                "title": conversation.title,
                "user": conversation.user.name,
                "created_at": conversation.created_at
            }
        )

    return {

        "users": total_users,

        "conversations": total_conversations,

        "messages": total_messages,

        "recent": recent

    }