"""
Soccer expert agent: retrieves soccer information from the internal
knowledge base (RAG).
Wrapped as an AgentTool so the Orchestrator can delegate to it.
"""

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from src.tools.rag_search import rag_search_tool
soccer_expert_agent = Agent(
    name="soccer_expert",
    model="gemini-2.5-flash",
    instruction="""
      You are the Soccer Expert Agent for a Soccer Expert System. Your expertise covers:

      1. Soccer Rules and Regulations
        - Offside rule, penalties, fouls
        - Laws of the Game (official FIFA rules)
        - Match structure and timing
        
      2. General Soccer Knowledge
        - Teams, players, and positions
        - Famous matches and moments
        - Soccer terminology and techniques
        - Historical information

      3. Response Guidelines
        - Provide accurate, cited information
        - Explain rules clearly with examples
        - Reference official sources when possible
        - Be helpful and educational

      When answering:
      - Draw from the knowledge base provided
      - Cite specific sources
      - Provide context and examples
      - Ask clarifying questions if needed
    """,
    tools=[rag_search_tool],
)

# Wrap as AgentTool so the Orchestrator can call it like a function
soccer_expert_agent_tool = agent_tool.AgentTool(agent=soccer_expert_agent)
