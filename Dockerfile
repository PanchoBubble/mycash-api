# pull official base image
FROM python:3.7.4-alpine


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY /requirements /requirements
RUN pip install -r /requirements/base.txt

# copy project
COPY /app /app

# set work directory
WORKDIR /app