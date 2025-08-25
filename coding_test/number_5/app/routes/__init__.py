from fastapi import APIRouter

from app.routes import (
    agent,
    receipt,
)


router = APIRouter()
router.include_router(receipt.router)
router.include_router(agent.router)
