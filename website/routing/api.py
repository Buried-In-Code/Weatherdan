__all__ = ["router"]

from fastapi import APIRouter

from website import __version__, controller
from website.responses import ErrorResponse
from website.schemas import Stat

router = APIRouter(
    prefix=f"/api/v{__version__.split('.')[0]}",
    tags=["API"],
    responses={
        422: {"description": "Validation error", "model": ErrorResponse}
    },
)


@router.get(path="/yearly-stats")
def get_yearly_stats(maximum: int = 1000) -> list[Stat]:
    return controller.generate_yearly_stats(maximum=maximum)


@router.get(path="/monthly-stats")
def get_monthly_stats(year: int = 0, maximum: int = 1000) -> list[Stat]:
    return controller.generate_monthly_stats(year=year, maximum=maximum)


@router.get(path="/weekly-stats")
def get_weekly_stats(year: int = 0, month: int = 0, maximum: int = 1000) -> list[Stat]:
    return controller.generate_weekly_stats(year=year, month=month, maximum=maximum)


@router.get(path="/daily-stats")
def get_daily_stats(year: int = 0, month: int = 0, maximum: int = 1000) -> list[Stat]:
    return controller.generate_daily_stats(year=year, month=month, maximum=maximum)
