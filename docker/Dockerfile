FROM alpine:3.9

MAINTAINER "Anthony Bretaudeau <anthony.bretaudeau@inrae.fr>"

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache \
    gcc g++ libstdc++ make \
    zlib-dev libzip-dev bzip2-dev xz-dev \
    python3 python3-dev \
    py3-numpy \
    nodejs nodejs-npm \
    git bash && \
    mkdir /genocrowd && \
    cd /genocrowd && \
    python3 -m venv venv && source /genocrowd/venv/bin/activate && \
    mv /requirements.txt /genocrowd/requirements.txt && \
    pip install -r requirements.txt && \
    rm /genocrowd/requirements.txt

COPY . /genocrowd
WORKDIR /genocrowd

RUN rm -f config/genocrowd.ini && \
    /genocrowd/install.sh && \
    /genocrowd/build.sh
