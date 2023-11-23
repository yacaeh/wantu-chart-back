# syntax = docker/dockerfile:1.2
# Dockerfile
# Django 최상위 루트에서 작성
FROM python:3.8
RUN mkdir -p /usr/src/static
# 컨테이너 내에서 코드가 실행될 경로 설정
ENV APP_HOME=/usr/src/app

WORKDIR $APP_HOME

# requirements.txt에 명시된 필요한 packages 설치
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Project를 /usr/src/app으로 복사
COPY . .
RUN python manage.py collectstatic --noinput
ENV DEBUG False
