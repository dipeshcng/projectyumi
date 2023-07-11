# echo 'building the project'
# pip install -r requirements.txt

# echo 'make migrations'
# python manage.py makemigrations
# python manage.py migrate

# echo 'collect static...'
# python manage.py collectstatic

# build_files.sh
pip install -r requirements.txt

# make migrations
python3.11 manage.py migrate 
python3.11 manage.py collectstatic
