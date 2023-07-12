import logging
from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2.exceptions import TemplateNotFound
from starlette.exceptions import HTTPException as StarletteHTTPException

from weatherdan import __version__, get_project_root, setup_logging
from weatherdan.routers.api import router as api_router
from weatherdan.routers.html import router as html_router
from weatherdan.settings import Settings

LOGGER = logging.getLogger("weatherdan")


def create_app() -> FastAPI:
    _app = FastAPI(title="Weatherdan", version=__version__)
    _app.mount("/static", StaticFiles(directory=get_project_root() / "static"), name="static")
    _app.include_router(html_router)
    _app.include_router(api_router)
    return _app


app = create_app()


@app.get(path="/")
def redirect() -> RedirectResponse:
    return RedirectResponse(url="/current")


@app.on_event(event_type="startup")
async def startup_event() -> None:
    setup_logging()
    settings = Settings()

    LOGGER.info(f"Listening on {settings.website.host}:{settings.website.port}")
    LOGGER.info(f"{app.title} v{app.version} started")


@app.middleware(middleware_type="http")
async def logger_middleware(request: Request, call_next):  # noqa: ANN001, ANN201
    LOGGER.debug(f"{request.method.upper():<7} {request.scope['path']}")
    response = await call_next(request)
    log_message = f"{request.method.upper():<7} {request.scope['path']} - {response.status_code}"
    if response.status_code < 400:
        LOGGER.info(log_message)
    elif response.status_code < 500:
        LOGGER.warning(log_message)
    else:
        LOGGER.error(log_message)
    return response


@app.exception_handler(exc_class_or_status_code=StarletteHTTPException)
async def http_exception_handler(request: Request, exc) -> JSONResponse:  # noqa: ARG001, ANN001
    status = HTTPStatus(exc.status_code)
    return JSONResponse(
        status_code=status,
        content={
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
            "status": f"{status.value}: {status.phrase}",
            "details": [exc.detail],
        },
        headers=exc.headers,
    )


@app.exception_handler(exc_class_or_status_code=RequestValidationError)
async def validation_exception_handler(
    request: Request,  # noqa: ARG001
    exc,  # noqa: ANN001
) -> JSONResponse:
    status = HTTPStatus(422)
    details = []
    for error in exc.errors():
        temp = ".".join(error["loc"])
        details.append(f"{temp}: {error['msg']}")
    return JSONResponse(
        status_code=status,
        content={
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
            "status": f"{status.value}: {status.phrase}",
            "details": details,
        },
    )


@app.exception_handler(exc_class_or_status_code=TemplateNotFound)
async def missing_template_exception_handler(
    request: Request,  # noqa: ARG001
    exc,  # noqa: ANN001
) -> JSONResponse:
    status = HTTPStatus(404)
    return JSONResponse(
        status_code=status,
        content={
            "timestamp": datetime.now().replace(microsecond=0).isoformat(),
            "status": f"{status.value}: {status.phrase}",
            "details": [f"{exc.message} not found."],
        },
    )
