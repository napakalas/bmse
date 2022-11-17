FROM python:3.8-slim

RUN mkdir /usr/src/app
COPY . /usr/src/app

RUN pip install -r /usr/src/app/requirements.txt

RUN apt-get update

RUN apt-get install -y git

RUN pip install git+https://github.com/napakalas/casbert.git
