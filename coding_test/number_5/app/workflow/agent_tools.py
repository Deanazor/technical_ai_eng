from google.adk.tools import ToolContext
from litellm import aembedding
from typing import Optional

from app.constants.receipt import TEXT_EMBEDDING_API_BASE, TEXT_EMBEDDING_MODEL
from app.schemas.vector import VectorSearchRequest
from app.services.vector import VectorDB


async def search_receipt_tool(
    user_question: str,
    tool_context: ToolContext,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    store_name: Optional[str] = None,
) -> str:
    """
    Search for receipts data in the vector database.
    Args:
        user_question: The question asked by the user.
        start_date: The start date of the receipts to search for.
        end_date: The end date of the receipts to search for.
        store_name: The name of the store to search for.
    Returns:
        The results of the search.
    """
    if start_date:
        user_question = f"{user_question}\n\nStart Date: {start_date}"
    if end_date:
        user_question = f"{user_question}\n\nEnd Date: {end_date}"
    if store_name:
        user_question = f"{user_question}\n\nStore Name: {store_name}"

    embedding_data = await aembedding(
        model=TEXT_EMBEDDING_MODEL,
        input=[user_question],
        api_base=TEXT_EMBEDDING_API_BASE,
    )
    vector_db: VectorDB = tool_context.state.get("vector_db", None)
    results = await vector_db.search(
        VectorSearchRequest(vector=embedding_data.data[0]["embedding"])
    )

    texts = "\n\n".join([result.text for result in results.results])
    response = f"Here are the receipts data:\n{texts}"
    return response
