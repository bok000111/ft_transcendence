
source /app/venv/bin/activate

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput && \
python manage.py check --deploy && \
exec daphne -b 0.0.0.0 -p 8000 ft_transcendence.asgi:application
# python manage.py test --noinput --exclude-tag=slow && \
# exec python manage.py runserver 0.0.0.0:8000