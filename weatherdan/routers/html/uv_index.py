__all__ = ["router"]
import logging

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pony.orm import db_session

from weatherdan import get_project_root
from weatherdan.database.tables import UVIndexReading

router = APIRouter(prefix="/uv-index")
templates = Jinja2Templates(directory=get_project_root() / "templates")
LOGGER = logging.getLogger(__name__)


@router.get("", response_class=HTMLResponse)
def current(
    request: Request,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    return templates.TemplateResponse(
        "uv-index/current.html.jinja",
        {"request": request, "max_entries": max_entries},
    )


@router.get("/historical", response_class=HTMLResponse)
def historical(
    request: Request,
    year: int = 0,
    month: int = 0,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    def year_list() -> list[int]:
        with db_session:
            return sorted({x.datestamp.year for x in UVIndexReading.select()})

    def month_list(year: int) -> list[int]:
        with db_session:
            return sorted(
                {x.datestamp.month for x in UVIndexReading.select() if x.datestamp.year == year},
            )

    return templates.TemplateResponse(
        "uv-index/historical.html.jinja",
        {
            "request": request,
            "max_entries": max_entries,
            "year_list": year_list(),
            "month_list": month_list(year=year) if year else [],
            "year": year,
            "month": month,
        },
    )
