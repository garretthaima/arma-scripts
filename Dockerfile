FROM debian:buster-slim

RUN apt-get update \
    && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        python3 \
        lib32stdc++6 \
        lib32gcc1 \
        wget \
        ca-certificates \
        python3-pip \
        python3-setuptools \
        locales \
    && \
    dpkg-reconfigure locales \
    && \
    apt-get remove --purge -y \
    && \
    apt-get clean autoclean \
    && \
    apt-get autoremove -y \
    && \
    rm /var/lib/apt/lists/* -r \
    && \
    mkdir -p /steamcmd \
        && cd /steamcmd \
        && wget -qO- 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar zxf - \
    && \
    /steamcmd/steamcmd.sh +login anonymous +quit

ENV ARMA_BINARY=./arma3server
ENV ARMA_CONFIG=
ENV ARMA_PROFILE=main
ENV ARMA_WORLD=empty
ENV ARMA_LIMITFPS=1000
ENV HEADLESS_CLIENTS=0
ENV PORT=2302
ENV MOD_FILE=
ENV STEAM_BRANCH=public
ENV STEAM_BRANCH_PASSWORD=

# Install python modules
COPY requirements.txt /src/requirements.txt
WORKDIR /src
ADD cfg /tmp/cfg
ADD mpmissions /tmp/mpmissions
RUN python3 -m pip install -r requirements.txt

ADD src /src
WORKDIR /arma3

VOLUME /steamcmd

STOPSIGNAL SIGINT

CMD ["python3", "/src/launch.py"]
