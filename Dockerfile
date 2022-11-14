FROM python:3.10-alpine3.16

# Log Python output immediately to standard out instead of buffereing so messages do not get stuck
# in buffer in event of crash.
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

# create a virtual environment and install python dependencies into it.
# create a user to run the application so we are not running as root.
# add static and media directories and give app user ownership.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
    
# prepend virtual environment binary to path to set it as the default
# python inside the container.
ENV PATH="/scripts:/py/bin:$PATH"

# everything below will be run as app user
USER app

CMD ["run.sh"]