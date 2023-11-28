import uvicorn

from weatherdan.constants import constants


def main() -> None:
    uvicorn.run(
        "weatherdan.__main__:app",
        host=constants.settings.website.host,
        port=constants.settings.website.port,
        use_colors=True,
        server_header=False,
        reload=constants.settings.website.reload,
        log_config=None,
    )


if __name__ == "__main__":
    main()
