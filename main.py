import logging
from dotenv import load_dotenv
from vision_agents.core import Agent, User, cli
from vision_agents.core.agents import AgentLauncher
from vision_agents.plugins import getstream, openai, ultralytics

load_dotenv()

async def create_agent(**kwargs) -> Agent:
    agent_user = User(
        name="Public Speaking & Presentation Coach",
        id="coach_agent",
        image="https://api.dicebear.com/7.x/bottts/svg?seed=coach"
    )
    return Agent(
        edge=getstream.Edge(),
        agent_user=agent_user,
        instructions="@instructions/coach.md",
        llm=openai.Realtime(
            fps=6,
            voice="alloy"
        ),
        processors=[
            ultralytics.YOLOPoseProcessor(model_path="yolo11n-pose.pt")
        ],
    )


async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    print(f"Presentation Coach Agent starting...")
    print(f"Joining call: {call_type}:{call_id}")

    call = await agent.create_call(call_type, call_id)
    session = await agent.join(call)

    print("Agent connected and ready!")
    print("Real-time coaching enabled")

    agent.llm.client.audio.enabled = False
    
    await agent.llm.simple_response(
        text="Greet the user warmly and say you're ready to help them practice. "
             "Watch their body language and speech — give encouraging, real-time feedback."
    )

    await agent.finish()   


if __name__ == "__main__":
    cli(AgentLauncher(create_agent=create_agent, join_call=join_call))

