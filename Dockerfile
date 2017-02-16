FROM python:3.6-alpine
ADD . .

ENV BUILD_DEPS="postgresql-dev"
ENV RUNTIEM_DEPS="supervisor"

RUN apk add --no-cache $BUILD_DEPS $RUNTIME_DEPS && \
    pip install -r ./requirements.txt && \
    apk del $BUILD_DEPS

# This is to protect against load balancer keep-alive timeouts; see
# https://github.com/benoitc/gunicorn/issues/1194 and
# https://serverfault.com/questions/782022/keepalive-setting-for-gunicorn-behind-elb-without-nginx
ENV PYTHONUNBUFFERED 1

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]
