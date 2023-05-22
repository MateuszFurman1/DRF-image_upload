FROM python:3.10-slim-buster
LABEL maintainer="Mateusz Furman <furman.mateusz.outlook.com>"
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 uninstall django
RUN pip3 install -r requirements.txt
