# interesnee_places_remember

[![Coverage Status](https://coveralls.io/repos/github/sda97ghb/interesnee_places_remember/badge.svg)](https://coveralls.io/github/sda97ghb/interesnee_places_remember)

This is an example project to show what I can do. It is made with:

- Django 3.1
- Django Allauth
- Bootstrap 4

## Features

### Your personal memories collection

<img style="display: inline-block" alt="Your personal list of memories" src="https://raw.githubusercontent.com/sda97ghb/interesnee_places_remember/master/places_remember/static/places_remember/img/preview/list_of_memories.png" height="400">

Point any place, write down your memories and save them in your personal collection.

Nothing will be forgotten!


### As accurate as you need

<img alt="Memory editing: choose location on a map and write your memory down" src="https://raw.githubusercontent.com/sda97ghb/interesnee_places_remember/master/places_remember/static/places_remember/img/preview/memory_editing.png" height="400">

City, street or random location far away? Choose any place!

Write text up to 1000 characters long!


### Facebook social login

[Try it now with Facebook login!](https://places-remember-sda.herokuapp.com/)


## Deploy

1. Setup Python 3, pip, venv
2. Setup dependencies with ```pip install -r requirements.txt```
3. Set environment variables
    - DEBUG=False or True (development only)
    - SECRET_KEY=*django secret key*
    - FACEBOOK_SECRET=*facebook app secret*
    - YANDEX_MAPS_API_KEY=*yandex maps api key*
    - DATABASE_URL=e.g. postgres://*user*:*password*@*host*:5432/*db_name* or sqlite:///db.sqlite3 (development only)
4. Generate compiled translations with ```django-admin compilemessages --ignore=venv```
5. Collect static files with ```python manage.py collectstatic```
6. Migrate database with ```python manage.py migrate```
7. Run server
    - Production: ```gunicorn places_remember_project.wsgi --log-file -```
    - Development: ```python manage.py runserver```
