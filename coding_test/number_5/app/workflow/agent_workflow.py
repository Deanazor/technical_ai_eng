from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from app.config import get_settings
from app.constants.agent import (
    AGENT_NAME,
    AGENT_RECEIPT_DESCRIPTION,
    AGENT_RECEIPT_SYSTEM_PROMPT,
    AGENT_INCLUDE_CONTENTS,
)
from app.workflow.agent_callbacks import enrich_context_callback
from app.workflow.agent_tools import search_receipt_tool

root_agent = LlmAgent(
    model=LiteLlm(
        model=get_settings().agent_model_name,
        api_base=get_settings().agent_base_url,
        api_key=get_settings().agent_api_key,
    ),
    name=AGENT_NAME,
    description=AGENT_RECEIPT_DESCRIPTION,
    instruction=AGENT_RECEIPT_SYSTEM_PROMPT,
    include_contents=AGENT_INCLUDE_CONTENTS,
    tools=[search_receipt_tool],
    before_model_callback=enrich_context_callback,
)
