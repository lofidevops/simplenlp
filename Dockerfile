FROM ubuntu:20.04

RUN \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install pipenv

WORKDIR /app
COPY . /app

ENV LANG="en_US.UTF-8"
ENV PYTHONUNBUFFERED 1
RUN pipenv sync
RUN pipenv run python manage.py initwordy
RUN pipenv run python manage.py migrate

ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_EMAIL admin@admin.example
ENV DJANGO_SUPERUSER_PASSWORD admin
RUN pipenv run python manage.py createsuperuser --noinput
