#!/bin/bash

# this is an entry point for docker images
# the main purpose is to allow flexible launching
# of the gunicorn process based on environment
# variables which isn't possible with docker-compose
# at the moment.

paste_config="$1"
server_port="$2"
exec gunicorn \
	--paste ${paste_config} \
    --worker-class ${GUNICORN_WORKER_CLASS:=sync} \
    --workers ${GUNICORN_WORKERS:=1} \
    --timeout ${GUNICORN_TIMEOUT:=120} \
    --worker-connections 1024 \
    --bind 0.0.0.0:${server_port} \
    --limit-request-line 4094 \
    ${GUNICORN_OPTS}
