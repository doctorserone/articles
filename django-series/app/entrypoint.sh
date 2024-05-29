#!/bin/sh

echo "Generate custom app migration files..."
python manage.py makemigrations

echo "Executing Django DB migration..."
python manage.py migrate

echo "Adding Django scheduled tasks..."
python manage.py crontab add
crontab -l
service cron restart

echo "Creating Django administrator..."
python manage.py createsuperuserwithpassword \
    --username $DJANGO_ADMIN_USERNAME \
    --password $DJANGO_ADMIN_PASSWORD \
    --email $DJANGO_ADMIN_EMAIL \
    --preserve

echo "Initial tasks finalized!"

# Execute gunicorn and wait
gunicorn ticmagicalline.wsgi:application --bind 0.0.0.0:8081
