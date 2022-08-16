import logging

from fastapi import APIRouter

from app.src.api.api_v1.routers import images

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    deprecated=False
)

router.include_router(images.router)
