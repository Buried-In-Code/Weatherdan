__all__ = ["router"]

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from common import get_project_root
from web_interface.models.user import User

router = APIRouter(prefix="/Weatherdan", tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get("", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/{username}", response_class=HTMLResponse)
def user(request: Request, username: str):
    user = User(username=username)
    return templates.TemplateResponse(
        "user.html",
        {
            "request": request,
            "user": user,
        },
    )
