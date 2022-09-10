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
    apk add --update --no-cache postgresql-client && \
    #We install the postgresql client in our container
    apk add --update --no-cache --virtual .tmp-build-deps \
    #We set a group of packages for install
        build-base postgresql-dev musl-dev && \
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
        django-user
        #Adding the user

ENV PATH="/py/bin:$PATH"

USER django-user