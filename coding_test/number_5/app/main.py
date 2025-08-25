from contextlib import asynccontextmanager

from fastapi import FastAPI
from google.adk.sessions import InMemorySessionService
from easyocr import Reader

from app.routes import router as api_router
from app.services.vector import VectorDB
from app.utils.agent import get_runner
from app.workflow.agent_workflow import root_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.context = {}
    app.context["vector_db"] = VectorDB()
    app.context["session_service"] = InMemorySessionService()
    app.context["ocr_reader"] = Reader(["en"])
    app.context["runner"] = get_runner(root_agent, app.context["session_service"])

    yield

    if hasattr(app.context, "vector_db"):
        delattr(app.context, "vector_db")
    if hasattr(app.context, "session_service"):
        delattr(app.context, "session_service")
    if hasattr(app.context, "runner"):
        delattr(app.context, "runner")
    if hasattr(app.context, "ocr_reader"):
        delattr(app.context, "ocr_reader")


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")
