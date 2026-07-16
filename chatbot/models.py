# Import SQLAlchemy column types
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from datetime import datetime
from sqlalchemy.sql import func

# Import relationship for table associations
from sqlalchemy.orm import relationship

# Import Base class from database.py
from chatbot.database import Base
from sqlalchemy import JSON


# User table
class User(Base):

    # Database table name
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # User name
    name = Column(String, nullable=False)

    # Email (must be unique)
    email = Column(String, unique=True, index=True, nullable=False)

    # Hashed password
    password = Column(String, nullable=False)

    # User role (admin / employee)
    role = Column(String, nullable=False)

    # One user can have many conversations
    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete"
    )


# Conversation table
class Conversation(Base):

    # Database table name
    __tablename__ = "conversations"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Conversation title
    title = Column(String, nullable=False)
    created_at = Column(
    DateTime,
    server_default=func.now()
    )

    # User ID (Foreign Key)
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Relationship with User table
    user = relationship(
        "User",
        back_populates="conversations"
    )

    # One conversation contains many messages
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete"
    )


# Message table
class Message(Base):

    # Database table name
    __tablename__ = "messages"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Message role (user / assistant)
    role = Column(String, nullable=False)

    # Message content
    content = Column(Text, nullable=False)

    timestamp = Column(
    DateTime,
    server_default=func.now()
    )

    # Conversation ID (Foreign Key)
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id")
    )

    # Relationship with Conversation table
    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )
    sources = Column(JSON, nullable=True)
    # Agent execution details
    agent = Column(JSON, nullable=True)