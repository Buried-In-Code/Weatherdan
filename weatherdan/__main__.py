import logging
from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from weatherdan import __version__, elapsed_timer, get_project_root, setup_logging
from weatherdan.constants import Constants
from weatherdan.routers.api import router as api_router
from weatherdan.routers.html import router as html_router

LOGGER = logging.getLogger("weatherdan")


def create_app() -> FastAPI:
    _app = FastAPI(title="Weatherdan", version=__version__)
    _app.mount("/static", StaticFiles(directory=get_project_root() / "static"), name="static")
    _app.include_router(html_router)
    _app.include_router(api_router)
    return _app


app = create_app()


@app.on_event(event_type="startup")
async def startup_event() -> None:
    setup_logging()

    LOGGER.info(
        "Listening on %s:%s",
        Constants.settings.website.host,
        Constants.settings.website.port,
    )
    LOGGER.info("%s v%s started", app.title, app.version)


@app.middleware(middleware_type="http")
async def logger_middleware(request: Request, call_next):  # noqa: ANN001, ANN201
    log_message = f"{request.method.upper():<7} {request.scope['path']}"
    LOGGER.debug(log_message)
    with elapsed_timer() as elapsed:
        response = await call_next(request)
    log_message += f" - {response.status_code} => {elapsed():.2f}s"
    if response.status_code < 400:
        LOGGER.info(log_message)
    elif response.status_code < 500:
        LOGGER.warning(log_message)
    else:
        LOGGER.error(log_message)
    return response


@app.exception_handler(exc_class_or_status_code=HTTPException)
async def http_exception_handler(request: Request, exc) -> JSONResponse:  # noqa: ARG001, ANN001
    status = HTTPStatus(exc.status_code)
    return JSONResponse(
        status_code=status,
        content={
            "timestamp": datetime.now(tz=UTC).astimezone().isoformat(),
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
            "timestamp": datetime.now(tz=UTC).astimezone().isoformat(),
            "status": f"{status.value}: {status.phrase}",
            "details": details,
        },
    )
