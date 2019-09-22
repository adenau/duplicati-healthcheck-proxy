FROM python:3.7-slim


ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true

COPY Pipfile* /app/
COPY src /app/
WORKDIR /app

RUN pip3 install pipenv
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8000

#ENTRYPOINT ["/usr/local/bin/pipenv", "run", "gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":8000", "main:app"]
ENTRYPOINT ["/usr/local/bin/pipenv", "run", "gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "--config", "/app/gunicorn.conf", "-b", ":8000", "main:app"]
