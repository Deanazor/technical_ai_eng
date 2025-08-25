from base64 import b64encode
import requests

from frontend.schemas import ChitchatRequest, ChitchatResponse, ReceiptUploadRequest, ReceiptUploadResponse


def upload_file(file: bytes, metadata: dict | None = None) -> str:
    request = ReceiptUploadRequest(
        image_base64=b64encode(file).decode(),
        metadata=metadata,
    )
    response = requests.post(
        "http://localhost:8000/api/receipt/upload",
        json=request.model_dump(),
    )
    response = ReceiptUploadResponse.model_validate(response.json())

    return response.message


def send_message(message: str, session_id: str) -> str:
    request = ChitchatRequest(
        messages=[message],
        session_id=session_id,
        user_id=session_id,
    )

    response = requests.post(
        "http://localhost:8000/api/agent/chitchat",
        json=request.model_dump(),
    )
    response = ChitchatResponse.model_validate(response.json())

    return response.message
