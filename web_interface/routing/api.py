__all__ = ["router"]

from fastapi import APIRouter
from natsort import humansorted as sorted
from natsort import ns

from web_interface import __version__, controller
from web_interface.responses import ErrorResponse
from web_interface.schemas import Device

router = APIRouter(
    prefix=f"/api/v{__version__.split('.')[0]}",
    tags=["API"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)


@router.get(
    path="/yearly-stats",
    response_model=list[Device],
    responses={409: {"model": ErrorResponse}},
)
def get_yearly_stats(maximum: int = 1000) -> list[Device]:
    return sorted(
        {
            controller.generate_yearly_stats(device=x, maximum=maximum)
            for x in controller.device_list()
        },
        alg=ns.NA | ns.G,
    )


@router.get(
    path="/monthly-stats",
    response_model=list[Device],
    responses={409: {"model": ErrorResponse}},
)
def get_monthly_stats(maximum: int = 1000, year: int = 0) -> list[Device]:
    return sorted(
        {
            controller.generate_monthly_stats(year=year, device=x, maximum=maximum)
            for x in controller.device_list()
        },
        alg=ns.NA | ns.G,
    )


@router.get(
    path="/weekly-stats",
    response_model=list[Device],
    responses={409: {"model": ErrorResponse}},
)
def get_weekly_stats(maximum: int = 1000, year: int = 0, month: int = 0) -> list[Device]:
    return sorted(
        {
            controller.generate_weekly_stats(year=year, month=month, device=x, maximum=maximum)
            for x in controller.device_list()
        },
        alg=ns.NA | ns.G,
    )


@router.get(
    path="/daily-stats", response_model=list[Device], responses={409: {"model": ErrorResponse}}
)
def get_daily_stats(maximum: int = 1000, year: int = 0, month: int = 0) -> list[Device]:
    return sorted(
        {
            controller.generate_daily_stats(year=year, month=month, device=x, maximum=maximum)
            for x in controller.device_list()
        },
        alg=ns.NA | ns.G,
    )
