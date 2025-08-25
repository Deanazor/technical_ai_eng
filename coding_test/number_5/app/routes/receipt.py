from fastapi import APIRouter, Request

from app.schemas.receipt import (
    ReceiptSearchResponse,
    ReceiptUploadRequest,
)
from app.schemas.response import DefaultResponse
from app.services.receipt import search_receipt, store_receipt

router = APIRouter(prefix="/receipt")


@router.post("/upload", response_model=DefaultResponse)
async def upload(data: ReceiptUploadRequest, request: Request):
    print(f"Received request: {data.image_base64[:10]}")
    await store_receipt(
        data, request.app.context["vector_db"], request.app.context["ocr_reader"]
    )
    return DefaultResponse(message="success")


@router.get("/search", response_model=ReceiptSearchResponse)
async def search(text: str, request: Request):
    results = await search_receipt(text, request.app.context["vector_db"])
    return ReceiptSearchResponse(results=results)
