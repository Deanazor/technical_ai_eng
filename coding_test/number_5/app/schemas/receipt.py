from pydantic import BaseModel


class ReceiptUploadRequest(BaseModel):
    image_base64: str
    metadata: dict | None = None


class ReceiptUploadResponse(BaseModel):
    text: str


class ReceiptSearchResponse(BaseModel):
    results: list
