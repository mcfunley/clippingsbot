FROM python:3.5-alpine
ADD . .
RUN pip install -r ./requirements.txt
ENV PYTHONUNBUFFERED 1
CMD gunicorn -b 0.0.0.0:8080 -w 4 hello:app --log-file - --access-logfile -
