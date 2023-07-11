__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from weatherdan import get_project_root
from weatherdan.storage import read_from_file

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/current", response_class=HTMLResponse)
def current(request: Request, count: Annotated[int, Cookie()] = 28) -> Response:
    return templates.TemplateResponse("current.html.jinja", {"request": request, "count": count})


@router.get("/historical", response_class=HTMLResponse)
def historical(
    request: Request,
    year: int = 0,
    month: int = 0,
    count: Annotated[int, Cookie()] = 28,
) -> Response:
    def year_list() -> list[int]:
        return sorted({x.timestamp.year for x in read_from_file()})

    def month_list(year: int) -> list[int]:
        return sorted({x.timestamp.month for x in read_from_file() if x.timestamp.year == year})

    return templates.TemplateResponse(
        "historical.html.jinja",
        {
            "request": request,
            "count": count,
            "year_list": year_list(),
            "month_list": month_list(year=year) if year else [],
            "year": year,
            "month": month,
        },
    )


@router.get("/editor", response_class=HTMLResponse)
def editor(request: Request, count: Annotated[int, Cookie()] = 28) -> Response:
    return templates.TemplateResponse("editor.html.jinja", {"request": request, "count": count})
