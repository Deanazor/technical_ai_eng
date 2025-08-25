import base64
import io

from easyocr import Reader
from litellm import aembedding
from PIL import Image

from app.constants.receipt import (
    RECEIPT_EMBEDDING_FORMAT,
    TEXT_EMBEDDING_API_BASE,
    TEXT_EMBEDDING_MODEL,
)
from app.schemas.receipt import ReceiptUploadRequest
from app.schemas.vector import VectorAddRequest, VectorSearchRequest
from app.services.vector import VectorDB


def extract_text(image_bytes: bytes, ocr_reader: Reader) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    results = ocr_reader.readtext(image)
    text = "\n".join([result[1] for result in results])
    return text


async def store_receipt(
    request: ReceiptUploadRequest, vector_db: VectorDB, ocr_reader: Reader
):
    print(f"Request: {request.image_base64[:10]}")
    image_bytes = base64.b64decode(request.image_base64)
    print(f"Image bytes: {image_bytes[:10]}")
    text = extract_text(image_bytes, ocr_reader)
    print(f"Extracted text: {text}")
    text = RECEIPT_EMBEDDING_FORMAT.format(text=text, metadata=request.metadata)
    embedding_data = await aembedding(
        model=TEXT_EMBEDDING_MODEL, input=[text], api_base=TEXT_EMBEDDING_API_BASE
    )
    vector_db.add_vector(
        VectorAddRequest(
            vector=embedding_data.data[0]["embedding"],
            text=text,
            metadata=request.metadata,
        )
    )


async def search_receipt(text: str, vector_db: VectorDB):
    embedding_data = await aembedding(
        model=TEXT_EMBEDDING_MODEL, input=[text], api_base=TEXT_EMBEDDING_API_BASE
    )
    results = await vector_db.search(
        VectorSearchRequest(vector=embedding_data.data[0]["embedding"])
    )
    return results
