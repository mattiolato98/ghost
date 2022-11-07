FROM nginx

COPY ${GHOST_FULLCHAIN_PEM} /etc/letsencrypt/live/soulscribe.ml/

COPY ${GHOST_PRIVKEY_PEM} /etc/letsencrypt/live/soulscribe.ml/

COPY ./nginx/nginx.conf.template /etc/nginx/templates/nginx.conf.template

USER root

RUN mkdir -p /vol/static && \
    chmod -R 777 /vol/static && \
    mkdir -p /vol/media && \
    chmod -R 777 /vol/media