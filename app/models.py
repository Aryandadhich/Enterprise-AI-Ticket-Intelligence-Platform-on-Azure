"""
models.py
---------
Request and Response data shapes for the RAG API.

Pydantic models do two things automatically:
  1. Validation  — if wrong data comes in, FastAPI returns 422 error instantly
  2. Docs        — FastAPI uses these to generate /docs page automatically

No logic here — just shapes.
"""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request Models — what the API receives
# ---------------------------------------------------------------------------

class TicketRequest(BaseModel):
    """
    What the caller sends when submitting a ticket for analysis.

    Example request body:
        {
            "ticket": "Logic App 401 error aa raha hai production mein"
        }
    """

    ticket: str = Field(
        ...,                          # ... means required — cannot be empty
        min_length=10,                # at least 10 characters
        max_length=2000,              # not too long
        description="The support ticket text to analyze",
        examples=["Database connection timeout in production environment"],
    )


# ---------------------------------------------------------------------------
# Response Models — what the API returns
# ---------------------------------------------------------------------------

class TicketResponse(BaseModel):
    """
    What the API returns after analyzing a ticket.

    Example response body:
        {
            "answer": "Based on the runbook, check connection pool settings...",
            "sources": ["database-connection-runbook.md"],
            "model_used": "gpt-4o"
        }
    """

    answer: str = Field(
        description="AI-generated answer based on knowledge base"
    )

    sources: list[str] = Field(
        default=[],
        description="Knowledge documents used to generate this answer"
    )

    model_used: str = Field(
        description="The GPT model that generated the answer"
    )


class HealthResponse(BaseModel):
    """
    Response for the GET /health endpoint.
    Used to check if the API is alive — standard practice in production.

    Example:
        { "status": "ok", "version": "1.0.0" }
    """

    status: str
    version: str = "1.0.0"
