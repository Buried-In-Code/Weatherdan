FROM python:3.13

WORKDIR /app

COPY weatherdan /app/weatherdan
COPY pyproject.toml README.md run.py /app/

RUN pip install --no-cache-dir .[postgres]

ENV XDG_CACHE_HOME=/app/cache \
    XDG_CONFIG_HOME=/app/config \
    XDG_DATA_HOME=/app/data \
    XDG_STATE_HOME=/app/state

RUN mkdir -p $XDG_CACHE_HOME \
    && mkdir -p $XDG_CONFIG_HOME/weatherdan \
    && mkdir -p $XDG_DATA_HOME/weatherdan \
    && mkdir -p $XDG_STATE_HOME/weatherdan

COPY static /app/static
COPY templates /app/templates

EXPOSE 25710

CMD ["python", "run.py"]
