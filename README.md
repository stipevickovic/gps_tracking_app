# GPS tracking app


### Quickstart

Create Python3 virtual environment:

    mkvirtualenv --python=/usr/bin/python3 <env-name>

Get the source from GitHub:

    git clone git@bitbucket.org:in_terra/gps_tracking.git

Navigate to the repo directory:

    cd gps_tracking

Install requirements:

    pip install -r requirements.txt

Navigate to Django project directory:

    cd django_project

Create .env file and define environment variables showed in env.sample.

Migrate the database:

    python manage.py migrate

Create super user:

    python manage.py createsuperuser

Run development server:

    python manage.py runserver

Point your browser to:

    127.0.0.1:8000
