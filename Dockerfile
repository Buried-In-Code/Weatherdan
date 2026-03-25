FROM --platform=$BUILDPLATFORM gradle:9.4.1-jdk17 AS builder

WORKDIR /data
COPY . /data/
RUN gradle build -x test

FROM --platform=$TARGETPLATFORM eclipse-temurin:17.0.18_8-jre

WORKDIR /app
COPY --from=builder /data/weatherdan/build/libs/weatherdan-0.8.0-all.jar /app/Weatherdan.jar
ENV XDG_CACHE_HOME=/app/cache \
    XDG_CONFIG_HOME=/app/config \
    XDG_DATA_HOME=/app/data \
    XDG_STATE_HOME=/app/state
RUN mkdir -p $XDG_CACHE_HOME \
    && mkdir -p $XDG_CONFIG_HOME/weatherdan \
    && mkdir -p $XDG_DATA_HOME/weatherdan \
    && mkdir -p $XDG_STATE_HOME/weatherdan

EXPOSE 25710
CMD ["java", "-jar", "Weatherdan.jar"]
