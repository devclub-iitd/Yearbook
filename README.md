# Yearbook
This repository contains the development code for the yearbook portal

## Installation Instructions (Local Deployment)
 1. Install virtualenv using `sudo pip3 install virtualenv`.
 2. After cloning the repo, create a new virtual environment using `virtualenv venv`.
 3. Activate the virtual env using `source venv/bin/activate`.
 4. Make sure your virtual environment has **python3** by running `python --version`. If not, delete venv folder and create a new virtual environment using `virtualenv -p python3 venv`.
 5. `source venv/bin/activate` to activate virtualenv
 6. Run `pip3 install -r requirements.txt` to install Django & other dependencies. (For errors regarding psycopg2 refer to further sections)
 7. Run `python manage.py makemigrations`. (For errors regarding postgresql refer to further sections)
 8. Run `python manage.py migrate`. If you face any errors, try `python manage.py migrate --fake`.
 9. Run `python manage.py createsuperuser`. You will be given prompts to enter credentials of your super user who can access the admin dashboard. Fill the details and keep pressing enter.
 10. Follow create database instructions ahead, to first create a postgres database. Then create .env with required credentials filling all the fields from .env_example.
 11. Run `source ./.env`. (If this doesn't work (like in windows subsystem), just copy paste the contents of your .env file into the active terminal session)
 12. Use `python manage.py runserver` to start the app!

## Error regarding psycopg2
 1. Run `sudo apt-get install libpq-dev`
 2. Try `which pg_config`. If it gives a path, then config file has been added to PATH correctly or else build psycopg2 from source and add it in your PATH environment variable.
 3. Re-run `pip3 install -r requirements.txt` and follow the Installation instructions.
 
## Error regarding Postgresql (Proper Installation)
 1. Make sure postgresql is installed by running `ps -ef | grep postgres`.
 2. If it shows postgres processes, then it is installed properly, else run `sudo apt-get install postgresql`
 3. After installation verify again by `ps -ef | grep postgres`. 
 4. RUN `sudo su - postgres`
 5. `pwd` 
 6. `psql -l` # This should output some default databases.
 7. `exit`
 8. Now proceed on and create a Database in postgres
 
## Creating a Database
* Login intoo postgres as root:
	```
	sudo su - postgres
	```
* Create a User:
	```
	createuser -EPd batman
	```
* Create a database:
	```
	createdb temp
	```
* Verify if database was created:
	```
	psql -l
	This should output something like:
	Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
	-----------+----------+----------+-------------+-------------+-----------------------
	temp  | postgres | UTF8     | en_SG.UTF-8 | en_SG.UTF-8 | 
	```
* Now we need to shift all the rights over database temp to user batman
	```
	psql
	postgres=# ALTER DATABASE temp OWNER TO batman;
	(The above command starts from ALTER ..., before that is the by default command line syntax)
	postgres=# \q
	psql -l
	(Now Owner of temp should be set to batman. If yes, we are done)
	exit
	```
* Database is successfully setup. Just enter these credentials as described in the steps "Running the System"

