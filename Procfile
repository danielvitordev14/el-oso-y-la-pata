web: gunicorn M_inha.wsgi:application --host 0.0.0.0 --port $PORT
release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py restore_dados 