# Yearbook

This readme is built upon the readme in master branch.

## convert python2 to python3
## convert to postgres:
 https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
 DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'myproject',
         'USER': 'mayank',
         'PASSWORD': 'mayank123',
         'HOST': 'localhost',
         'PORT': '5432',
     }
 }
 
 ## Docker
 ## UI
 
 ## Running the app locally
 1. Install virtualenv using `sudo pip3 install virtualenv`.
 2. After cloning the repo, create a new virtual environment using `virtualenv venv`.
 3. Activate the virtual env using `source venv/bin/activate`.
 4. Make sure your virtual environment has **python3** by running `python --version`. If not, create a new virtual environment using `virtualenv -p python3 venv2`.
 5. Run `pip3 install -r requirements.txt` to install Django & other dependencies.
 6. Run `python manage.py makemigrations`.
 7. Run `python manage.py migrate`. If you face any errors, try `python manage.py migrate --fake`.
 8. Use `python manage.py runserver` to start the app!
