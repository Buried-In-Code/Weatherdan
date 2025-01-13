# Weatherdan

![Python](https://img.shields.io/badge/Python-3.13-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

[![Github - Version](https://img.shields.io/github/v/tag/Buried-In-Code/Weatherdan?logo=Github&label=Version&style=flat-square)](https://github.com/Buried-In-Code/Weatherdan/tags)
[![Github - License](https://img.shields.io/github/license/Buried-In-Code/Weatherdan?logo=Github&label=License&style=flat-square)](https://opensource.org/licenses/MIT)
[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Weatherdan?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Weatherdan/graphs/contributors)

Retrieve weather information from Ecowitt devices and display in graphs, allows for manual additions and updates.\
Currently, tracks total Rainfall and high, average and low for Solar, UV Index and Wind readings.

## Usage

### via uv

1. Make sure you have [uv](https://docs.astral.sh/uv/) installed: `uv --version`
2. Clone the repo: `git clone https://github.com/Buried-In-Code/Weatherdan`
3. Install the project: `uv sync`
4. Run using: `uv run run.py`

### via Docker Compose

1. Make sure you have [Docker](https://www.docker.com/) installed: `docker --version`
2. Make sure you have [Docker-Compose](https://github.com/docker/compose) installed: `docker-compose --version`
3. Create a `docker-compose.yaml` file, _an example:_

```yaml
version: '3'

services:
  weatherdan:
    image: 'ghcr.io/buried-in-code/weatherdan:latest'
    container_name: 'Weatherdan'
    environment:
      TZ: 'Pacific/Auckland'
    ports:
      - '25710:25710'
    volumes:
      - './cache:/app/cache'
      - './config:/app/config'
      - './data:/app/data'
      - './state:/app/state'
```

4. Run using: `docker-compose up -d`

## Socials

[![Social - Fosstodon](https://img.shields.io/badge/%40BuriedInCode-teal?label=Fosstodon&logo=mastodon&style=for-the-badge)](https://fosstodon.org/@BuriedInCode)\
[![Social - Matrix](https://img.shields.io/matrix/The-Dev-Environment:matrix.org?label=The-Dev-Environment&logo=matrix&style=for-the-badge)](https://matrix.to/#/#The-Dev-Environment:matrix.org)
