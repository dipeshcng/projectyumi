#Project Overview
- API Project
- Four different user (Admin, Host Business, Graduate and Volunteer)
- CRUD operation for every tables


#Required Python >=3.9 and pip latest

#Update settings.py file
- SECRET_KEY = django-insecure-8#-1gzyi%5s1e_$skx*+lg2t@(&fo$%f8b#$@1m#7l+)jl2()4
- EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
- EMAIL_HOST = "smtp.gmail.com"
- EMAIL_USE_TLS = True
- EMAIL_PORT = 587
- EMAIL_HOST_USER = {sender_email}
- EMAIL_HOST_PASSWORD = {sender_password}

#Installation:
- git clone https://github.com/dipeshcng/projectyumi.git
- cd projectyumi
- pip install virtualenv venv
- activate virtualenv
- pip install -r requirements.txt


#Process
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser


#Test
- localhost:8000/admin