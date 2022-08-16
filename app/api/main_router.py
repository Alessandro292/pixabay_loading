import logging

from fastapi import APIRouter

from app.api.api_v1 import routers_v1

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api"
)

router.include_router(routers_v1.router)
