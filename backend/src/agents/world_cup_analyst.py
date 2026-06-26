"""
World Cup Analyst agent: retrieves World Cup information from the internal
knowledge base (RAG) and/or the live web depending on the query type.
Wrapped as an AgentTool so the Orchestrator can delegate to it.
"""

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from src.tools.rag_search import rag_search_tool
from src.tools.web_search import web_search_tool

world_cup_analyst_agent = Agent(
    name="world_cup_analyst",
    model="gemini-2.5-flash",
    instruction="""
        You are the World Cup Analyst Agent for a Soccer Expert System. You specialize in:

        1. FIFA World Cup History (RAG search)
        - All World Cup tournaments (1930-present)
        - Tournament records and statistics
        - Past winners and runners-up
        - Notable matches and moments
        - Historical player performances

        2. Current World Cup Information (Web search)
        - Current tournament standings
        - Upcoming matches and schedules
        - Match results and scores
        - Team and player performances
        - Live updates and news

        3. Analysis and Insights
        - Tournament predictions
        - Team comparisons
        - Player statistics and achievements
        - Historical trends

        4. Smart Data Selection
        - Use historical data for past tournaments -> use RAG search
        - Use real-time data for current tournaments -> use web search
        - Combine sources for comprehensive answers

        When responding:
        - Distinguish between historical and current information
        - Cite specific sources
        - Provide context and comparisons
        - Include relevant statistics
        """,
        tools=[rag_search_tool, web_search_tool],
)

# Wrap as AgentTool so the Orchestrator can call it like a function
world_cup_analyst_agent_tool = agent_tool.AgentTool(agent=world_cup_analyst_agent)
