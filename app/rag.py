"""
rag.py
------
Core RAG (Retrieval-Augmented Generation) logic.

How it works:
  1. load_knowledge_docs()  — reads all .md files from Knowledge/ folder
  2. find_relevant_docs()   — finds which docs are relevant to the ticket
                              (simple keyword matching — works without AI Search)
  3. ask_gpt()              — calls Azure OpenAI GPT-4o with ticket + relevant docs
  4. analyze_ticket()       — orchestrates all 3 steps, returns final answer

When AI Search is available, find_relevant_docs() can be swapped to use
vector/semantic search instead — same interface, better results.
"""

from pathlib import Path
from openai import AzureOpenAI

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_API_VERSION,
    GPT_DEPLOYMENT_NAME,
    KNOWLEDGE_DIR,
)


# ---------------------------------------------------------------------------
# Step 1 — Load all knowledge documents from Knowledge/ folder
# ---------------------------------------------------------------------------

def load_knowledge_docs() -> dict[str, str]:
    """
    Read all .md files from the Knowledge/ directory.

    Returns a dict:
        {
            "logic-app-authentication-runbook.md": "# Logic App...<full content>",
            "database-connection-runbook.md": "# Database...<full content>",
            ...
        }

    Why dict? So we can return both the filename (for citations) and content.
    """
    docs = {}

    if not KNOWLEDGE_DIR.exists():
        print(f"[WARN] Knowledge directory not found: {KNOWLEDGE_DIR}")
        return docs

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        try:
            content = file_path.read_text(encoding="utf-8")
            docs[file_path.name] = content
            print(f"  [OK] Loaded: {file_path.name}")
        except Exception as exc:
            print(f"  [WARN] Could not read {file_path.name}: {exc}")

    print(f"[INFO] Loaded {len(docs)} knowledge document(s)")
    return docs


# ---------------------------------------------------------------------------
# Step 2 — Find relevant docs for the given ticket
# ---------------------------------------------------------------------------

def find_relevant_docs(ticket: str, docs: dict[str, str]) -> dict[str, str]:
    """
    Find which knowledge documents are relevant to the ticket.

    Strategy: simple keyword matching
      - Split ticket into words
      - Check if any word appears in the doc content or filename
      - Return docs that have at least 2 keyword matches

    This works well without AI Search. When AI Search is available,
    this function can be replaced with a vector similarity search
    for much better results — same return type, drop-in replacement.

    Returns: subset of docs dict — only relevant ones
    """
    # Clean the ticket — lowercase, split into words, remove short words
    ticket_keywords = [
        word.lower()
        for word in ticket.replace(",", " ").replace(".", " ").split()
        if len(word) > 3   # ignore short words like "the", "is", "in"
    ]

    relevant = {}

    for filename, content in docs.items():
        # Combine filename + content for matching (filename has good keywords)
        searchable_text = (filename + " " + content).lower()

        # Count how many ticket keywords appear in this doc
        matches = sum(1 for kw in ticket_keywords if kw in searchable_text)

        # At least 2 keyword matches = relevant
        if matches >= 2:
            relevant[filename] = content
            print(f"  [MATCH] {filename} ({matches} keyword matches)")

    if not relevant:
        # No specific match — return all docs as fallback
        # Better to give GPT all context than none
        print("  [INFO] No specific match — using all docs as context")
        return docs

    return relevant


# ---------------------------------------------------------------------------
# Step 3 — Call Azure OpenAI GPT-4o with ticket + relevant docs as context
# ---------------------------------------------------------------------------

def ask_gpt(ticket: str, relevant_docs: dict[str, str]) -> str:
    """
    Send the ticket + relevant knowledge docs to GPT-4o and get an answer.

    Prompt structure:
      - System message: tells GPT its role and how to behave
      - User message:   ticket text + relevant doc contents

    Why this structure?
      System message = permanent instructions (role, tone, constraints)
      User message   = the actual question with context
    """

    # Build the context string from relevant docs
    # Each doc is clearly labelled so GPT can cite the source
    context_parts = []
    for filename, content in relevant_docs.items():
        context_parts.append(f"--- Document: {filename} ---\n{content}")

    context = "\n\n".join(context_parts)

    # System prompt — tells GPT exactly how to behave
    system_prompt = """You are an expert IT support engineer for an enterprise platform.
Your job is to analyze support tickets and provide clear, actionable solutions.

Rules:
- Base your answer ONLY on the knowledge documents provided
- Be specific and practical — give exact steps to resolve the issue
- If the documents don't cover the issue, say so clearly
- Keep the answer concise but complete
- Mention which document your answer is based on"""

    # User prompt — ticket + relevant docs as context
    user_prompt = f"""Support ticket:
{ticket}

Relevant knowledge base documents:
{context}

Please analyze this ticket and provide a solution based on the above documents."""

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    # Call GPT-4o
    response = client.chat.completions.create(
        model=GPT_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.3,    # low = more focused, consistent answers
        max_tokens=800,     # enough for a detailed answer
    )

    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Step 4 — Main orchestrator function (called by main.py)
# ---------------------------------------------------------------------------

def analyze_ticket(ticket: str) -> dict:
    """
    Full RAG pipeline — orchestrates all 3 steps.

    Called by the FastAPI endpoint in main.py.

    Returns:
        {
            "answer": "Based on the runbook...",
            "sources": ["logic-app-authentication-runbook.md"],
            "model_used": "gpt-4o"
        }
    """
    print(f"\n[RAG] Analyzing ticket: {ticket[:60]}...")

    # Step 1 — Load all knowledge docs
    all_docs = load_knowledge_docs()

    if not all_docs:
        return {
            "answer": "Knowledge base is empty. Please add documents to the Knowledge/ folder.",
            "sources": [],
            "model_used": GPT_DEPLOYMENT_NAME,
        }

    # Step 2 — Find relevant docs
    relevant_docs = find_relevant_docs(ticket, all_docs)

    # Step 3 — Ask GPT with relevant docs as context
    answer = ask_gpt(ticket, relevant_docs)

    return {
        "answer": answer,
        "sources": list(relevant_docs.keys()),
        "model_used": GPT_DEPLOYMENT_NAME,
    }
