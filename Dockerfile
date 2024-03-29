FROM python:3.9-alpine3.13
LABEL mantainer="edwindeveloper@outlook.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEBUG_STATUS=false
RUN python3 -m venv /py && \
    #Create a new virtual environment that our system will use
    /py/bin/pip install --upgrade pip && \
    #We upgrade the packages of pip dependencies
    apk add --update --no-cache postgresql-client jpeg-dev && \
    #We install the postgresql client in our container and the jpeg-dev library
    apk add --update --no-cache --virtual .tmp-build-deps \
    #We set a group of packages for install  -- linux-headers is a requirement for AWS server instalation
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
        #Install the dependencies we list
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    #Install dependencies from requirement file
    if [ $DEBUG_STATUS = "true" ]; \
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
    chmod -R 755 /vol && \
    # make sure our scripts is executable in the directory
    chmod -R +x /scripts
    # we change the mode of the permissions of the directory

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user
# the name of the script that run our application
CMD ["run.sh"]