#!/bin/sh

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput && \
python manage.py check --deploy && \
if [ "$DJANGO_DEBUG" == "True" ]; then
    exec python manage.py runserver 0.0.0.0:8000
else
    exec daphne -b 0.0.0.0 -p 8000 ft_transcendence.asgi:application
fi