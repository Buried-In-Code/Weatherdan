<img src="./weatherdan/src/main/resources/static/img/logo.png" align="left" width="128" height="128" alt="Weatherdan Logo"/>

# Weatherdan

![Java Version](https://img.shields.io/badge/Temurin-21-green?style=flat-square&logo=eclipse-adoptium)
![Kotlin Version](https://img.shields.io/badge/Kotlin-2.2-green?style=flat-square&logo=kotlin&logoColor=white)
[![Version](https://img.shields.io/gitea/v/release/BuriedInCode/Weatherdan?gitea_url=https%3A%2F%2Fcodefloe.com&include_prereleases&label=Version&style=flat-square&logo=forgejo&logoColor=white)](https://codefloe.com/BuriedInCode/Weatherdan/tags)

[![Gradle](https://img.shields.io/badge/Gradle-9.2-informational?style=flat-square&logo=gradle)](https://github.com/gradle/gradle)
[![Spotless](https://img.shields.io/badge/Spotless-8.0-informational?style=flat-square)](https://github.com/diffplug/spotless)
[![Javalin](https://img.shields.io/badge/Javalin-6.7-informational?style=flat-square)](https://github.com/javalin/javalin)
[![Bulma](https://img.shields.io/badge/Bulma-1.0-informational?style=flat-square)](https://github.com/jgthms/bulma)

![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)
[![License](https://img.shields.io/badge/License-MIT-informational?style=flat-square)](https://opensource.org/licenses/MIT)

[![Pipeline Status](https://ci.codefloe.com/api/badges/542/status.svg)](https://ci.codefloe.com/repos/542)

Retrieve weather information from Ecowitt devices and display in graphs, allows for manual additions and updates.\
Currently, tracks total Rainfall and high, average and low for Solar, UV Index and Wind readings.

## Usage

### via Source

1. Make sure you have a supported version of [Java](https://adoptium.net/temurin/releases/) installed: `java --version`
2. Clone the repo: `git clone https://codefloe.com/BuriedInCode/Weatherdan.git`
3. Run using: `./gradlew build run`

### via Docker-Compose

1. Make sure you have [Docker](https://www.docker.com/) installed: `docker --version`
2. Make sure you have [Docker-Compose](https://github.com/docker/compose) installed: `docker-compose --version`
3. Create a `docker-compose.yaml` file, _an example:_

```yaml
services:
  weatherdan:
    image: 'codefloe.com/BuriedInCode/Weatherdan:latest'
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
[![Social - Matrix](https://img.shields.io/badge/%23The--Dev--Environment-teal?label=Matrix&logo=matrix&style=for-the-badge)](https://matrix.to/#/#The-Dev-Environment:matrix.org)
