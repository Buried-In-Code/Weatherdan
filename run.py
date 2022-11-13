from pathlib import Path

import uvicorn

if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    uvicorn.run(
        "web_interface.__main__:app",
        host="0.0.0.0",
        port=8001,
        use_colors=True,
        server_header=False,
        log_config="log_config.yaml",
    )
