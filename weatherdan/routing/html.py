__all__ = ["router"]

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from weatherdan import controller, get_project_root

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("/latest", response_class=HTMLResponse)
def latest(request: Request, maximum: int = 28) -> Response:
    controller.refresh_data()
    return templates.TemplateResponse("latest.html", {"request": request, "count": maximum})


@router.get("/filtered", response_class=HTMLResponse)
def filtered(request: Request, maximum: int = 28, year: int = 0, month: int = 0) -> Response:
    controller.refresh_data()
    return templates.TemplateResponse(
        "filtered.html",
        {
            "request": request,
            "count": maximum,
            "year_list": controller.list_available_years(),
            "month_list": controller.list_available_months(year=year) if year else [],
            "year": year,
            "month": month,
        },
    )
