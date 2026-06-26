"""
Orchestrator agent: the central coordinator of the multi-agent system.
Classifies user intent, routes to soccer_expert and reviewer agents,
implements the feedback loop for low-confidence results, and manages
session state across the conversation.
"""

import json
from google.adk.agents import Agent
from src.agents.soccer_expert import soccer_expert_agent_tool
from src.agents.world_cup_analyst import world_cup_analyst_agent_tool
from src.observability.logger import log_agent_call, log_pipeline_start, Timer
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# Global session service for conversation memory
global_session_service = InMemorySessionService()

ORCHESTRATOR_INSTRUCTION = """
You are the Orchestrator Agent for a Soccer Expert System. Your responsibilities are:

1. Analyze incoming queries to determine their type and intent
2. Route queries to the most appropriate specialized agent:
   - SOCCER_EXPERT for general soccer knowledge
   - WORLD_CUP_ANALYST for FIFA World Cup questions
3. Manage conversation context for multi-turn interactions

Query routing rules:
- If query mentions "World Cup" or "FIFA" or current information (standings, recent results): → World Cup Analyst
- If query is about soccer rules, players, teams: → Soccer Expert

Be concise and helpful. It is important to always cite sources in bold in a separate line when providing information.
"""




def create_orchestrator() -> Agent:
    """
    Creates and returns the configured Orchestrator agent with all
    sub-agent tools attached.

    Returns:
        Configured Google ADK Agent instance.
    """
    orchestrator = Agent(
        name="orchestrator",
        model="gemini-2.5-flash",
        instruction=ORCHESTRATOR_INSTRUCTION,
        tools=[soccer_expert_agent_tool, world_cup_analyst_agent_tool],
    )
    return orchestrator


async def run_chatbot(agent, message: str, user_id: str = "customer1", session_id: str = "session1"): 
    """
    Run the chatbot agent with conversation memory.

    Args:
        agent: The chatbot agent
        message: User message
        user_id: User identifier
        session_id: Session identifier for conversation memory
    """
    global global_session_service

    # Create or get session
    try:
        await global_session_service.create_session(
            app_name="soccer_expert_chatbot",
            user_id=user_id,
            session_id=session_id
        )
    except:
        pass  # Session already exists

    # Create a Runner to manage the agent execution
    runner = Runner(
        agent=agent,
        app_name="soccer_expert_chatbot",
        session_service=global_session_service,
    )

    print(f"\n{'='*60}")
    print(f"User: {message}")
    print(f"{'='*60}\n")
    print("Agent: ", end="", flush=True)

    # Create message content
    message_content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )

    # Run agent and collect response
    response_text = ""
    event_count = 0
    max_events = 25

    with Timer() as t:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message_content
        ):
            event_count += 1

            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
                            print(part.text, end='', flush=True)

            if event_count >= max_events:
                print("\n(Reached max events limit)")
                break

    print(f"\n{'='*60}\n")

    log_agent_call(
        agent_name="orchestrator",
        query=message,
        tools_called=["soccer_expert_agent_tool", "world_cup_analyst_agent_tool"],
        latency_ms=t.elapsed_ms,
        output_summary=str(response_text)[:200],
    )

    return response_text
