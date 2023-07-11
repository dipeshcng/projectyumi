echo 'building the project'
python -m pip install -r requirements.txt

echo 'make migrations'
python manage.py makemigrations
python manage.py migrate

echo 'collect static...'
python manage.py collectstatic