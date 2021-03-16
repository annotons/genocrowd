FROM alpine:3.12

MAINTAINER "Anthony Bretaudeau <anthony.bretaudeau@inrae.fr>"

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache \
    python3 \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor \
    ca-certificates \
    py3-numpy \
    py3-cffi \
    py3-bcrypt \
    py3-wheel \
    nodejs \
    nodejs-npm \
    git \
    nano \
    curl \
    bash && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    apk add --no-cache --virtual .build-deps gcc python3-dev zlib-dev libzip-dev bzip2-dev xz-dev g++ libstdc++ make libffi-dev && \
    mkdir /genocrowd && \
    cd /genocrowd && \
    mv /requirements.txt /genocrowd/requirements.txt && \
    pip install -r requirements.txt && \
    apk --purge del .build-deps && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache

COPY . /genocrowd
WORKDIR /genocrowd

COPY docker/nginx.conf /etc/nginx/
COPY docker/nginx_genocrowd.conf /etc/nginx/conf.d/
COPY docker/uwsgi.ini /etc/uwsgi/
COPY docker/supervisord.conf /etc/supervisord.conf

RUN rm -f config/genocrowd.ini && \
    echo "Installing webpack..." && \
    npm install --global webpack webpack-cli && \
    echo "Installing node deps..." && \
    npm install --loglevel verbose && \
    echo "" && \
    echo "-----------" && \
    echo "" && \
    echo "Building JS code..." && \
    npm run -d prod

ENTRYPOINT /genocrowd/run_genocrowd_docker.sh
