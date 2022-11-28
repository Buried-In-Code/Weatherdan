import uvicorn
from rich import box
from rich.panel import Panel

from common import __version__, get_project_root
from common.console import CONSOLE
from common.settings import Settings


def main():
    CONSOLE.print(
        Panel.fit(
            "Welcome to Weatherdan",
            title="Web Interface",
            subtitle=f"v{__version__}",
            box=box.SQUARE,
        ),
        style="bold magenta",
        justify="center",
    )

    settings = Settings.load().save()
    log_folder = get_project_root() / "logs"
    log_folder.mkdir(parents=True, exist_ok=True)
    uvicorn.run(
        "web_interface.__main__:app",
        host=settings.web.host,
        port=settings.web.port,
        use_colors=True,
        server_header=False,
        log_config="log_config.yaml",
    )


if __name__ == "__main__":
    main()
