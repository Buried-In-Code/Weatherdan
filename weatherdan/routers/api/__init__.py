__all__ = ["router"]

from fastapi import APIRouter

from weatherdan.responses import ErrorResponse
from weatherdan.routers.api.humidity import router as humidity_router
from weatherdan.routers.api.pressure import router as pressure_router
from weatherdan.routers.api.rainfall import router as rainfall_router
from weatherdan.routers.api.solar import router as solar_router
from weatherdan.routers.api.temperature import router as temperature_router

router = APIRouter(
    prefix="/api",
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)
router.include_router(humidity_router)
router.include_router(pressure_router)
router.include_router(rainfall_router)
router.include_router(solar_router)
router.include_router(temperature_router)
