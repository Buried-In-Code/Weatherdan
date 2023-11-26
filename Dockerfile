FROM python:3.11

WORKDIR /app

COPY weatherdan /app/weatherdan
COPY static /app/static
COPY templates /app/templates
COPY pyproject.toml README.md run.py /app/

RUN pip install --no-cache-dir .

ENV XDG_CACHE_HOME /app/cache
ENV XDG_CONFIG_HOME /app/config
RUN mkdir -p $XDG_CONFIG_HOME/weatherdan
ENV XDG_DATA_HOME /app/data
RUN mkdir -p $XDG_DATA_HOME/weatherdan

EXPOSE 25710

CMD ["python" "run.py"]
