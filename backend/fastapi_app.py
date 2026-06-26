"""
FastAPI application for Soccer Expert Chatbot Agent

Exposes the chatbot as a REST API with endpoints for:
- Chat messages
- Health checks
"""

import os
from dotenv import load_dotenv
import asyncio
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.genai import types


from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from src.rag.ingest import build_index
from src.agents.orchestrator import create_orchestrator, run_chatbot

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
agent = None
active_sessions = {}

# ============================================================================
# Pydantic Models
# ============================================================================

class ChatMessage(BaseModel):
    """Chat message request"""
    user_id: str = "user1"
    session_id: str = "session1"
    message: str
    temperature: Optional[float] = None


class ChatResponse(BaseModel):
    """Chat response"""
    success: bool
    response: str
    session_id: str
    user_id: str
    tool_used: Optional[str] = None


class DocumentRequest(BaseModel):
    """Add document to RAG system"""
    content: str
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    """Document addition response"""
    success: bool
    doc_id: Optional[str] = None
    message: str


class SearchRequest(BaseModel):
    """Search knowledge base"""
    query: str
    top_k: int = 3


class SearchResponse(BaseModel):
    """Search results"""
    success: bool
    query: str
    results: List[Dict[str, Any]]
    message: str


class WebSearchRequest(BaseModel):
    """Web search request"""
    query: str


class WebSearchResponse(BaseModel):
    """Web search results"""
    success: bool
    query: str
    results: List[Dict[str, Any]]
    message: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    active_sessions: int


# ============================================================================
# Startup and Shutdown
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup, cleanup on shutdown"""
    global agent

    logger.info("Initializing chatbot system...")
    agent = create_orchestrator()

    logger.info("Building RAG system...")
    build_index()
    logger.info("✓ RAG system built")

    logger.info("✓ Initialization complete")

    yield

    # Cleanup
    logger.info("Shutting down chatbot system...")
    active_sessions.clear()
    logger.info("✓ Cleanup complete")


# ============================================================================
# Create FastAPI App
# ============================================================================

app = FastAPI(
    title="Soccer Expert Chatbot",
    description="Multi-agent soccer expert chatbot powered by Google ADK",
    version="1.0.0",
    lifespan=lifespan
)

session_service = InMemorySessionService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and status"""
    return HealthResponse(
        status="healthy",
        message="Soccer Expert Chatbot API is running",
        active_sessions=len(active_sessions)
    )



@app.get("/test", response_class=HTMLResponse)
async def test():
    with open("src/test_ui.html") as f:
        return f.read()


@app.get("/")
async def root():
    """Help endpoint with API information"""
    return {
        "name": "Soccer Expert Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/query",
            "sessions": "/sessions"
        }
    }



@app.post("/query", response_model=ChatResponse)
async def query_endpoint(request: ChatMessage):
    
    if agent is None:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:

        # Track session
        if request.session_id not in active_sessions:
            active_sessions[request.session_id] = {
                "user_id": request.user_id,
                "message_count": 0
            }

        active_sessions[request.session_id]["message_count"] += 1

        logger.info(f"Chat request - Session: {request.session_id}, Message: {request.message[:50]}...")

         # Run agent
        response = await run_chatbot(
            agent,
            request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )

        logger.info(f"Response sent - Session: {request.session_id}")
       
        return ChatResponse(
            success=True,
            response=response,
            session_id=request.session_id,
            user_id=request.user_id,
            tool_used=''
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def get_sessions():
    """Get all active sessions"""
    return {
        "active_sessions": len(active_sessions),
        "sessions": active_sessions
    }


@app.delete("/sessions/{session_id}")
async def end_session(session_id: str):
    """End a chat session"""
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"status": "success", "message": f"Session {session_id} ended"}
    return {"status": "not_found", "message": f"Session {session_id} not found"}



# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "Internal server error",
        "detail": str(exc)
    }



if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
