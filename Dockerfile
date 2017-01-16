FROM python:3.5-alpine
ADD . .
RUN pip install -r ./requirements.txt

# This is to protect against load balancer keep-alive timeouts; see 
# https://github.com/benoitc/gunicorn/issues/1194 and
# https://serverfault.com/questions/782022/keepalive-setting-for-gunicorn-behind-elb-without-nginx
ENV PYTHONUNBUFFERED 1

CMD gunicorn -b 0.0.0.0:8080 -w 4 hello:app --log-file - --access-logfile -
