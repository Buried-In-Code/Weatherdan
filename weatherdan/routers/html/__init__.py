__all__ = ["router"]

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from weatherdan import get_project_root
from weatherdan.routers.html.pressure import router as pressure_router
from weatherdan.routers.html.rainfall import router as rainfall_router
from weatherdan.routers.html.solar import router as solar_router
from weatherdan.routers.html.uv_index import router as uv_index_router
from weatherdan.routers.html.wind import router as wind_router

router = APIRouter(tags=["WebInterface"], include_in_schema=False)
templates = Jinja2Templates(directory=get_project_root() / "templates")


@router.get(path="/", response_class=HTMLResponse)
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html.jinja", {"request": request})


@router.get("/editor", response_class=HTMLResponse)
def editor(request: Request, count: int = Cookie(alias="weatherdan_count", default=28)) -> Response:
    return templates.TemplateResponse("editor.html.jinja", {"request": request, "count": count})


router.include_router(pressure_router)
router.include_router(rainfall_router)
router.include_router(solar_router)
router.include_router(uv_index_router)
router.include_router(wind_router)
