__all__ = ["router"]

from fastapi import APIRouter, Body

from common import __version__
from common.statistics import (
    load_daily_stats,
    load_monthly_stats,
    load_weekly_stats,
    load_yearly_stats,
)
from web_interface.models.stats import Stats
from web_interface.models.user import User
from web_interface.responses import ErrorResponse

router = APIRouter(
    prefix=f"/api/v{__version__.split('.')[0]}",
    tags=["API"],
    responses={422: {"description": "Validation error", "model": ErrorResponse}},
)


@router.post(
    path="/users",
    status_code=201,
    response_model=User,
    responses={409: {"model": ErrorResponse}},
)
def create_user(username: str = Body(embed=True)) -> User:
    return User(username=username)


@router.get(
    path="/{username}", response_model=User, responses={404: {"model": ErrorResponse}}
)
def get_user(username: str) -> User:
    return User(username=username)


@router.get(
    path="/{username}/stats",
    response_model=Stats,
    responses={404: {"model": ErrorResponse}},
)
def get_user_stats(username: str) -> Stats:
    return Stats(
        daily=dict(reversed(list(load_daily_stats().items()))),
        weekly=dict(reversed(list(load_weekly_stats().items()))),
        monthly=dict(reversed(list(load_monthly_stats().items()))),
        yearly=dict(reversed(list(load_yearly_stats().items()))),
    )
