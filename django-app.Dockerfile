# BUILDER

FROM python:3.10-alpine as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp-deps \
        postgresql-dev gcc python3-dev musl-dev build-base libffi-dev linux-headers

RUN pip install --upgrade pip

COPY ./django-app/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

RUN apk del .tmp-deps

# DJANGO IMAGE

FROM python:3.10-alpine

RUN mkdir -p /home/app && addgroup -S -g 1000 app && adduser -S -u 1000 app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

RUN apk update && apk add libpq ffmpeg icu-dev gettext gettext-dev
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY ./django-app $APP_HOME

COPY scripts $HOME/scripts

RUN mkdir -p $HOME/vol/static && \
    mkdir -p $HOME/vol/media && \
    chmod -R 755 $HOME/scripts && \
    chown -R app:app $HOME

USER app

CMD ["sh", "-c", "$HOME/scripts/django_run.sh"]