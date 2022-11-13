__all__ = ["router"]

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from web_interface import controller, get_project_root

router = APIRouter(prefix="/weatherdan", tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("", response_class=HTMLResponse)
def index(request: Request):
    return RedirectResponse(url="/weatherdan/latest")


@router.get("/latest", response_class=HTMLResponse)
def latest(request: Request):
    return templates.TemplateResponse("latest.html", {"request": request})


@router.get("/filtered", response_class=HTMLResponse)
def filtered(request: Request, year: int = 0, month: int = 0):
    return templates.TemplateResponse(
        "filtered.html",
        {
            "yearsAvailable": controller.list_available_years(),
            "yearSelected": year,
            "monthsAvailable": controller.list_available_months(year=year) if year else [],
            "monthSelected": month,
            "request": request,
        },
    )
