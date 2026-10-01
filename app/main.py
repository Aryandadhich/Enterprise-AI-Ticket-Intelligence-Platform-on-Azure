"""
main.py
-------
FastAPI application — entry point for the RAG API.

Endpoints:
  GET  /          → welcome message
  GET  /health    → health check (is API alive?)
  POST /analyze-ticket → main RAG endpoint

Run locally:
  uvicorn app.main:app --reload

Then open:
  http://localhost:8000/docs     → interactive API documentation
  http://localhost:8000/health   → health check
"""

from fastapi import FastAPI, HTTPException

from app.models import TicketRequest, TicketResponse, HealthResponse
from app.rag import analyze_ticket

# ---------------------------------------------------------------------------
# Create the FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Enterprise AI Ticket Intelligence Platform",
    description="RAG-powered API that analyzes IT support tickets using Azure OpenAI + Knowledge Base",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# GET / — Welcome
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    """
    Welcome endpoint.
    Just confirms the API is running.
    """
    return {
        "message": "Enterprise AI Ticket Intelligence Platform",
        "docs": "/docs",
        "health": "/health",
    }


# ---------------------------------------------------------------------------
# GET /health — Health Check
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
def health():
    """
    Health check endpoint.

    Used in production to check if the API is alive.
    Load balancers and monitoring tools call this every 30 seconds.
    If it returns 200 → API is healthy.
    If it fails → something is wrong → alert triggered.
    """
    return HealthResponse(status="ok")


# ---------------------------------------------------------------------------
# POST /analyze-ticket — Main RAG Endpoint
# ---------------------------------------------------------------------------

@app.post("/analyze-ticket", response_model=TicketResponse)
def analyze(request: TicketRequest):
    """
    Main endpoint — analyzes a support ticket using RAG.

    What happens:
      1. FastAPI validates the request using TicketRequest model
      2. rag.analyze_ticket() runs the full RAG pipeline:
           - Loads knowledge docs
           - Finds relevant docs for this ticket
           - Calls GPT-4o with docs as context
      3. Returns structured response with answer + sources

    Example request:
        POST /analyze-ticket
        { "ticket": "Logic App 401 error in production" }

    Example response:
        {
            "answer": "Based on logic-app-authentication-runbook.md...",
            "sources": ["logic-app-authentication-runbook.md"],
            "model_used": "gpt-4o"
        }
    """
    try:
        result = analyze_ticket(request.ticket)

        return TicketResponse(
            answer=result["answer"],
            sources=result["sources"],
            model_used=result["model_used"],
        )

    except Exception as exc:
        # If anything goes wrong — return proper HTTP error
        # Never let raw Python exceptions leak to the caller
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(exc)}"
        )
