from pydantic import BaseModel


class ReceiptUploadRequest(BaseModel):
    image_base64: str
    metadata: dict | None = None


class ReceiptUploadResponse(BaseModel):
    message: str


class ChitchatRequest(BaseModel):
    messages: list[str]
    session_id: str
    user_id: str


class ChitchatResponse(BaseModel):
    message: str
