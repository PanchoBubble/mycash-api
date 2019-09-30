# pull official base image
FROM python:3


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY /requirements /requirements
RUN pip install -r /requirements/base.txt

# copy project
COPY . /app

# set work directory
WORKDIR /app