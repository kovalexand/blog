#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py makemigrations users
python manage.py makemigrations categories
python manage.py makemigrations posts
python manage.py makemigrations comments
python manage.py migrate
python manage.py collectstatic

exec "$@"