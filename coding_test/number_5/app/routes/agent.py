from fastapi import APIRouter, Request

from app.schemas.agent import AgentRequest
from app.schemas.response import DefaultResponse
from app.services.agent import get_agent_response

router = APIRouter(prefix="/agent")


@router.post("/chitchat", response_model=DefaultResponse)
async def chitchat(request: Request, agent_request: AgentRequest):
    context = {
        "vector_db": request.app.context["vector_db"],
    }
    runner = request.app.context["runner"]
    response = await get_agent_response(runner, agent_request, context)
    return DefaultResponse(message=response)
