FROM python:3.9-alpine3.13
LABEL mantainer="edwindeveloper@outlook.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    #Create a new virtual environment that our system will use
    /py/bin/pip install --upgrade pip && \
    #We upgrade the packages of pip dependencies
    apk add --update --no-cache postgresql-client jpeg-dev && \
    #We install the postgresql client in our container and the jpeg-dev library
    apk add --update --no-cache --virtual .tmp-build-deps \
    #We set a group of packages for install
        build-base postgresql-dev musl-dev zlib zlib-dev && \
        #Install the dependencies we list
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    #Install dependencies from requirement file
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    # Delete temporal folder
    apk del .tmp-build-deps && \
    #Remove the package we already install in previous steps
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
        #Adding the user   
    mkdir -p /vol/web/media && \
    # we crete the media volume
    mkdir -p /vol/web/static && \
    # we create the static volume
    chown -R django-user:django-user /vol && \
    # we change the owner with the user django-user in vol
    chmod -R 755 /vol
    # we change the mode of the permissions of the directory

ENV PATH="/py/bin:$PATH"

USER django-user