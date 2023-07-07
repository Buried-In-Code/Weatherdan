__all__ = ["router"]

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from weatherdan import get_project_root
from weatherdan.storage import read_from_file

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/current", response_class=HTMLResponse)
def latest(request: Request, count: int = 28) -> Response:
    return templates.TemplateResponse("current.html.jinja", {"request": request, "count": count})


@router.get("/historical", response_class=HTMLResponse)
def filtered(request: Request, maximum: int = 28, year: int = 0, month: int = 0) -> Response:
    def year_list() -> list[int]:
        return sorted({x.timestamp.year for x in read_from_file()})

    def month_list(year: int) -> list[int]:
        return sorted({x.timestamp.month for x in read_from_file() if x.timestamp.year == year})

    return templates.TemplateResponse(
        "historical.html.jinja",
        {
            "request": request,
            "count": maximum,
            "year_list": year_list(),
            "month_list": month_list(year=year) if year else [],
            "year": year,
            "month": month,
        },
    )
