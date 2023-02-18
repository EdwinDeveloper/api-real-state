# Basic image of the container
FROM nginxinc/nginx-unprivileged:1-alpine

# The maintainer of the docker image
LABEL mantainer="Edwindeveloper@outlook.com"

# We copy the file default.conf.tpl in our container, in the direction of /etc/nginx/
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
# We copy the file uwsgi_params  in our container, in the directory of /etc/nginx/
COPY ./uwsgi_params /etc/nginx/uwsgi_params
# We copy the file /run.sh in our root container directory
COPY ./run.sh /run.sh

# Environment variables
ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# We switch to the root user
USER root

# We create a new directory
RUN mkdir -p /vol/static && \
    # We give read permitions from the static forder
    chmod 755 /vol/static && \
    # We create an empty file named "default.conf" in /etc/nginx/conf.d/ location
    touch /etc/nginx/conf.d/default.conf && \
    # We're making nginx the ouwner of the default.conf file
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    # We give execution permissions to the file run.sh
    chmod +x /run.sh

# We setting up a volume
VOLUME /vol/static

# We switch to the nginx user(NOT RUNNING THE SCRIPT AS ROOT USER)
USER nginx

# Default script
CMD ["/run.sh"]
