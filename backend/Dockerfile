# pull the official docker image
FROM python:3.10-slim

# set work directory
WORKDIR /backend

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# copy project
COPY . /backend
