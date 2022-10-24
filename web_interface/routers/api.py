__all__ = ["router"]

from fastapi import APIRouter

from common import __version__
from web_interface.controllers.reading import (
    generate_daily_stats,
    generate_monthly_stats,
    generate_weekly_stats,
    generate_yearly_stats,
)
from web_interface.responses import ErrorResponse

router = APIRouter(
    prefix=f"/api/v{__version__.split('.')[0]}",
    tags=["API"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)


@router.get(
    path="/yearly-stats",
    response_model=dict[str, float],
    responses={409: {"model": ErrorResponse}},
)
def get_yearly_stats(maximum: int = 1000) -> dict[str, float]:
    return dict(reversed(list(generate_yearly_stats().items())[:maximum]))


@router.get(
    path="/monthly-stats",
    response_model=dict[str, float],
    responses={409: {"model": ErrorResponse}},
)
def get_monthly_stats(maximum: int = 1000, year: int = 0) -> dict[str, float]:
    return dict(reversed(list(generate_monthly_stats(year=year).items())[:maximum]))


@router.get(
    path="/weekly-stats",
    response_model=dict[str, float],
    responses={409: {"model": ErrorResponse}},
)
def get_weekly_stats(maximum: int = 1000, year: int = 0, month: int = 0) -> dict[str, float]:
    return dict(reversed(list(generate_weekly_stats(year=year, month=month).items())[:maximum]))


@router.get(
    path="/daily-stats", response_model=dict[str, float], responses={409: {"model": ErrorResponse}}
)
def get_daily_stats(maximum: int = 1000, year: int = 0, month: int = 0) -> dict[str, float]:
    return dict(reversed(list(generate_daily_stats(year=year, month=month).items())[:maximum]))
