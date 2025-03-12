FROM docker.io/python:3.12.2-slim-bookworm AS python

# stage 1 Build our dependencies (wheels)
FROM python  AS python-build-stage


ARG BUILD_ENVIRONMENT=local

RUN apt-get update && install --no-instal-recommends -y \ 
   build-essential \
   libpq-dev


#    copy everything from host machine to container (requirements forlders)
COPY ./requirements .
RUN pip wheel --wheel-dir  /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt


# stage 2 Run stage
FROM python AS pyhton-run-stage
ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app


# tell python not to write binary files when importing modules (.pyc files) for resource saving space usage
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \    
    BUILD_ENVIRONMENT=${BUILD_ENVIRONMENT}



WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    libpq-dev gettext \ 
    # this treats recommended packeges as not inmportant
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    mkdir -p ${APP_HOME}/staticfiles && \
    chown django:django ${APP_HOME}/staticfiles && \
    chmod 775 ${APP_HOME}/staticfiles


COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/



COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint.sh
COPY --chown=django:django ./docker/local/django/start.sh /start.sh

# convert into unix style endings for windows
RUN sed -i 's/\r$//g' /entrypoint.sh  /start.sh && \
    # chmod ensure entrypint and start scripts anre executed as scripts in docker, +x givers permission to be executed by user
    chmod +x /entrypoint.sh /start.sh


COPY --chown=django:django . ${APP_HOME}
USER django
# specifies default execution file when docker is started
ENTRYPOINT [ "/entrypoint.sh" ]