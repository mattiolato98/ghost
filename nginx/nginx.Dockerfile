FROM nginx

COPY ./fullchain.pem /etc/letsencrypt/live/soulscribe.ml/fullchain.pem

COPY ./privkey.pem /etc/letsencrypt/live/soulscribe.ml/privkey.pem

COPY ./nginx/nginx.conf.template /etc/nginx/templates/nginx.conf.template

USER root

RUN mkdir -p /vol/static && \
    chmod -R 777 /vol/static