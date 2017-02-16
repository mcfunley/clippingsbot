FROM python:3.6-alpine
ADD . .

ENV BUILD_DEPS="postgresql-dev build-base"
ENV RUNTIME_DEPS="supervisor"

RUN apk update && \
    apk add $BUILD_DEPS $RUNTIME_DEPS && \
    pip install -r ./requirements.txt && \
    apk del $BUILD_DEPS && \
    rm -rf /tmp/* /var/cache/*

# This is to protect against load balancer keep-alive timeouts; see
# https://github.com/benoitc/gunicorn/issues/1194 and
# https://serverfault.com/questions/782022/keepalive-setting-for-gunicorn-behind-elb-without-nginx
ENV PYTHONUNBUFFERED 1

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
