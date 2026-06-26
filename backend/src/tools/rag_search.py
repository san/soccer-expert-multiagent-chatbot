"""
Rag search tool: wraps the RAG retriever as a Google ADK FunctionTool
so agents can search the soccer and FIFA World Cup knowledge base by natural language query.
"""

from google.adk.tools import FunctionTool
from src.rag.retriever import get_retriever


def rag_search(query: str) -> dict:
    """
    Searches the internal soccer and FIFA World Cup knowledge base using vector similarity.
    Use this for soccer rules, player statistics, and match results for past FIFA World Cups.

    Args:
        query: Natural language question about soccer or past FIFA World Cup.

    Returns:
        Dict with 'results' (list of relevant text passages) and
        'source' indicating this came from the knowledge base.
    """
    retriever = get_retriever()
    results = retriever.retrieve(query)

    chunks = [
        {
            "text": r["text"],
            "source_file": r["source"],
            "relevance_score": r["score"],
        }
        for r in results
    ]

    return {
        "success": True,
        "results": chunks,
        "source": "knowledge_base",
        "num_results": len(chunks),
    }


# Wrap as ADK FunctionTool so agents can call it
rag_search_tool = FunctionTool(func=rag_search)
