from datetime import datetime

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest


def enrich_context_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    llm_request.append_instructions(
        [
            f"The current date is {datetime.now().strftime('%Y-%m-%d')}",
        ]
    )
    return
