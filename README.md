<img src="./static/img/logo.png" align="left" width="128" height="128" alt="Weatherdan Logo"/>

# Weatherdan

![Python](https://img.shields.io/badge/Python-3.11-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Hatch](https://img.shields.io/badge/Packaging-Hatch-4051b5?style=flat-square)](https://github.com/pypa/hatch)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?style=flat-square&logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/Code--Style-Black-000000?style=flat-square)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-informational?style=flat-square)](https://github.com/charliermarsh/ruff)

[![Github - Version](https://img.shields.io/github/v/tag/Buried-In-Code/Weatherdan?logo=Github&label=Version&style=flat-square)](https://github.com/Buried-In-Code/Weatherdan/tags)
[![Github - License](https://img.shields.io/github/license/Buried-In-Code/Weatherdan?logo=Github&label=License&style=flat-square)](https://opensource.org/licenses/MIT)
[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Weatherdan?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Weatherdan/graphs/contributors)

Retrieve weather information from Ecowitt devices and display in graphs, allows for manual additions and updates.\
Currently, tracks total Rainfall and high, average and low for Solar, UV Index and Wind readings.

## Usage

### via Github

1. Make sure you have a supported version of [Python](https://www.python.org/) installed: `python --version`
2. Clone the repo: `git clone https://github.com/Buried-In-Code/Weatherdan`
3. Install the project: `pip install .`
4. Run using: `Weatherdan`

### via Pipx

1. Make sure you have [Pipx](https://github.com/pypa/pipx) installed: `pipx --version`
2. Install the project `pipx install git+https://github.com/Buried-In-Code/Weatherdan.git`
3. Run using: `Weatherdan`

### via Docker-Compose

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
      - './config:/app/config'
      - './data:/app/data'
```

4. Run using: `docker-compose up -d`

## Socials

[![Social - Fosstodon](https://img.shields.io/badge/%40BuriedInCode-teal?label=Fosstodon&logo=mastodon&style=for-the-badge)](https://fosstodon.org/@BuriedInCode)\
[![Social - Matrix](https://img.shields.io/badge/%23The--Dev--Environment-teal?label=Matrix&logo=matrix&style=for-the-badge)](https://matrix.to/#/#The-Dev-Environment:matrix.org)
