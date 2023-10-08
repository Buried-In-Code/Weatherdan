import uvicorn

from weatherdan.constants import Constants


def main() -> None:
    uvicorn.run(
        "weatherdan.__main__:app",
        host=Constants.settings.website.host,
        port=Constants.settings.website.port,
        use_colors=True,
        server_header=False,
        reload=Constants.settings.website.reload,
        log_config=None,
    )


if __name__ == "__main__":
    main()
