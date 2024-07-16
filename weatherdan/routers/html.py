__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Cookie, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from weatherdan import get_project_root
from weatherdan.database import get_session
from weatherdan.models import Rainfall, Solar, UVIndex, Wind

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=str(get_project_root() / "templates"))


@router.get(path="/", response_class=HTMLResponse)
def dashboard(*, request: Request) -> Response:
    return templates.TemplateResponse("index.html.jinja", {"request": request})


@router.get("/editor", response_class=HTMLResponse)
def editor(
    *, request: Request, max_entries: int = Cookie(alias="weatherdan_max-entries", default=28)
) -> Response:
    return templates.TemplateResponse(
        "editor.html.jinja", {"request": request, "max_entries": max_entries}
    )


@router.get("/rainfall", response_class=HTMLResponse)
def rainfall(
    *,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    year: int = 0,
    month: int = 0,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    year_list = sorted({x.datestamp.year for x in session.exec(select(Rainfall)).all()})
    month_list = sorted(
        {
            x.datestamp.month
            for x in session.exec(select(Rainfall)).all()
            if x.datestamp.year == year
        }
    )

    return templates.TemplateResponse(
        "rainfall.html.jinja",
        {
            "request": request,
            "max_entries": max_entries,
            "year_list": year_list,
            "month_list": month_list if year else [],
            "year": year,
            "month": month,
        },
    )


@router.get("/solar", response_class=HTMLResponse)
def solar(
    *,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    year: int = 0,
    month: int = 0,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    year_list = sorted({x.datestamp.year for x in session.exec(select(Solar)).all()})
    month_list = sorted(
        {x.datestamp.month for x in session.exec(select(Solar)).all() if x.datestamp.year == year}
    )

    return templates.TemplateResponse(
        "solar.html.jinja",
        {
            "request": request,
            "max_entries": max_entries,
            "year_list": year_list,
            "month_list": month_list if year else [],
            "year": year,
            "month": month,
        },
    )


@router.get("/uv-index", response_class=HTMLResponse)
def uv_index(
    *,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    year: int = 0,
    month: int = 0,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    year_list = sorted({x.datestamp.year for x in session.exec(select(UVIndex)).all()})
    month_list = sorted(
        {x.datestamp.month for x in session.exec(select(UVIndex)).all() if x.datestamp.year == year}
    )

    return templates.TemplateResponse(
        "uv-index.html.jinja",
        {
            "request": request,
            "max_entries": max_entries,
            "year_list": year_list,
            "month_list": month_list if year else [],
            "year": year,
            "month": month,
        },
    )


@router.get("/wind", response_class=HTMLResponse)
def wind(
    *,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
    year: int = 0,
    month: int = 0,
    max_entries: int = Cookie(alias="weatherdan_max-entries", default=28),
) -> Response:
    year_list = sorted({x.datestamp.year for x in session.exec(select(Wind)).all()})
    month_list = sorted(
        {x.datestamp.month for x in session.exec(select(Wind)).all() if x.datestamp.year == year}
    )

    return templates.TemplateResponse(
        "wind.html.jinja",
        {
            "request": request,
            "max_entries": max_entries,
            "year_list": year_list,
            "month_list": month_list if year else [],
            "year": year,
            "month": month,
        },
    )

