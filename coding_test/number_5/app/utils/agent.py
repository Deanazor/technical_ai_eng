from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions.base_session_service import BaseSessionService

from app.constants.agent import AGENT_NAME


def get_runner(agent: LlmAgent, session_service: BaseSessionService):
    runner = Runner(
        agent=agent,
        app_name=AGENT_NAME,
        session_service=session_service,
    )
    return runner
