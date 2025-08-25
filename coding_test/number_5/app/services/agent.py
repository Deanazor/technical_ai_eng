from typing import Any

from google.adk.runners import Runner
from google.genai import types

from app.constants.agent import AGENT_NAME
from app.schemas.agent import AgentRequest


async def get_agent_response(
    runner: Runner,
    request: AgentRequest,
    context: dict[str, Any] | None = None,
):
    session = await runner.session_service.get_session(
        app_name=AGENT_NAME, user_id=request.user_id, session_id=request.session_id
    )
    if session is None:
        if context is None:
            raise ValueError("Context is required for new session creation")
        session = await runner.session_service.create_session(
            app_name=AGENT_NAME,
            user_id=request.user_id,
            session_id=request.session_id,
            state=context,
        )

    parts = []
    for message in request.messages:
        parts.append(types.Part(text=message))
    formatted_messages = types.Content(
        role="user",
        parts=parts,
    )

    response = "Something wrong with agent"
    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=request.session_id,
        new_message=formatted_messages,
    ):
        print(f"Event: {event}")
        if event.is_final_response():
            if event.content and event.content.parts:
                response = event.content.parts[0].text
            break

    return response
