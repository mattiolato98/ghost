FROM nginx

COPY ./nginx/nginx.conf.template /etc/nginx/templates/nginx.conf.template

USER root

RUN mkdir -p /vol/static && \
    chmod -R 777 /vol/static