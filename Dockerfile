FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/blog

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh

COPY ./entrypoint.sh .
RUN ["chmod", "+x", "/usr/src/blog/entrypoint.sh"]
ENTRYPOINT ["/usr/src/blog/entrypoint.sh"]

# copy project
COPY . .
