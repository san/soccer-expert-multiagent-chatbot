"""
Web search tool: wraps the Tavily API as a Google ADK FunctionTool
so agents can fetch live FIFA World Cup information.
"""

import os
from typing import Any, Dict
from tavily import TavilyClient
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from dotenv import load_dotenv

load_dotenv()


def web_search(
    query: str,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Perform web search to get real-time information on FIFA World Cup.

    Args:
        query: Search query
        tool_context: Runtime context

    Returns:
        Dict with web search results
    """
    
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,
        )

        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
                "published_date": r.get("published_date", "unknown"),
                "score": r.get("score", 0.0),
            }
            for r in response.get("results", [])
        ]

        return {
            "success": True,
            "results": results,
            "query": query,
            "source": "web",
            "message": f"Found {len(results)} web results",
            "num_results": len(results),
        }
    
    except ImportError:
        return {
            "success": False,
            "message": "tavily-python package not installed. Install with: pip install tavily-python"
        }
    except Exception as e:
        return {"success": False, "message": f"Error performing web search: {str(e)}"}


# Wrap as ADK FunctionTool so agents can call it
web_search_tool = FunctionTool(func=web_search)
