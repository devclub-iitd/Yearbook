# Yearbook
This repository contains the development code for the yearbook portal

## Database struncture
* Student:
  * id
  * one-one link with django inbuilt user(for auth purposes)
  * name
  * department
  * DP (display picture)
  * genPic1 (first out of the 2 pictures the user would like to contribute to the yearbook)
  * genPic2 (second out of the 2 pictures the user would like to contribute to the yearbook)
  * phone
  * email
  * oneliner (something that describes them)
  * AnswersAboutMyself (json of some answers they write about themselves)
  ```
  {
   "id of question":"answer"
  }
  example
  {
   "1":".",
   "3":"sample answer",
   "2":"another sample answer"
  }
  ```
  * VotesIHaveGiven (json of votes that this user has given)
  ```
  {
   "id of poll":"entry number of a user"
  }
  example
  {
    "283":"2014ee10444",
    "202":"2014ee10655",
    "265":"2014ee30544",
    "157":"2014ee30152",
    "211":"2014ee30531",
    "301":"2014ee10871",
    "310":"2014ee30527"
  }
  ```
  * CommentsIWrite (array of json of comments that this user has given)
  ```
  [
   {
    "comment":string of comment,
    "forWhom": "entry number of user"
   },...
  ]
  example
  [
   {
     "comment":"hello how are you.",
     "forWhom":"2014ch70049"
   },
   {
     "comment":"all the best for your future!",
     "forWhom":"2014ee30766"
   },
  ]
  ```
  * CommentsIGet (array of json of comments that this user gets)
  ```
  [
   {
    "comment":string of comment,
    "fromWhom": "entry number of user",
    "displayInPdf":"True or False"(based on whether the user wants this displayed in the pdf)
   },...
  ]
  example
  [
   {
     "comment":"I got this comment",
     "fromWhom":"2014ee30539",
     "displayInPdf":"True"
   },
   {
     "comment":"I got another comment ",
     "fromWhom":"2014ee10134",
     "displayInPdf":"True"
   },
   {
     "comment":"Ye lo ek aur",
     "fromWhom":"2014ee10496",
     "displayInPdf":"True"
   },
  ]
  ```
* GenQuestion (this consists of some general questions that admins have to publish before the portal is set up):
  * id
  * question 
* Poll (this consists of some poll questions)
  * id
  * poll (the poll title)
  * department
  * votes (json field which stores data about the votes given)
  ```
  {
   "entry number of some user":votes he/she gets,
   ...
  }
  example
  {
  "2014bb10048":4,
  "2014bb10021":3,
  "2014bb10028":6
  }
  ```
## Development
1. Activate your virtualenv.
2. Just use `./start_dev_server.sh` to start the local development server!  
A superuser is created with these credentials:
	```
	username (entry number): 2017_tester
	password: password
	student name: 2017_tester
	student department: cse
	```  
IITD OAuth is bypassed by default in development and you are directly logged in with user `2017_tester`. Set `BYPASS_OAUTH = False` in `settings_dev.py` to use OAuth instead. Entry year (2017) is required in tester username for polls to work properly.

## How is this supposed to work?
### Prior work to be done by admins
1. To get started with the yearbook follow the steps:
   * Clone the repository
   * Activate the virtalenv if you don't want python to interfere with your global packages
   * pip install -r requirements.txt (For errors regarding psycopg2 refer to further sections)
   * python manage.py makemigrations (For errors regarding postgresql refer to further sections)
   * python manage.py migrate
   * python manage.py createsuperuser
        * This will ask you for username, password and other details of the superuser you are creating. Remember the credentials. This             super user will allow you to handle django database.
   * Follow create database instructions ahead, to first create a postgres database. Then create .env with required credentials filling all the fields from .env_example.
   * Run `source ./.env`. (If this doesn't work (like in windows subsystem), just copy paste the contents of your .env file into the active terminal session)
   * Run python3 setAdminTable.py to create an admin table object if it does not exists already.
   * python manage.py runserver
        * This starts the Django server at port 8000
        * visit http://localhost:8000/admin on your browser
        * Enter the credentials of the superuser you created
        * Now you can see various tables like user, GenQuestions and Polls.
        * You can add or delete GenQuestions manually as their are only handful of them.
        * Rest of the polls and user entries will be done by the scripts.
        * This portal will be used to setup and verify the database entries.
2. Now, to populate the users table first we need to fetch all the users from IIT's internal site and populate the students in a file called filename.csv inside Scrape folder.
   * Follow the steps to populate users in the database.
        * Open your terminal inside the Scrape folder or navigate to the folder using cd Scrape. Let the django server running in one             terminal
        * Edit the urls inside Scrape.py to the site from you will pull the student records.
        * After desired editing run python Scrape.py 
        * This populates the filename.csv
        * After this copy and paste the following line in your terminal
            * export DJANGO_SETTINGS_MODULE=yearbook.settings
        * This exported the settings to connect with django. Now, navigate back to root folder of the project and type:
            * First navigate to myapp/ and edit Config.py to contain a seed value in the pswd variable.
            * Then navigate back to root folder and type python CsvToDatabase.py
            * This populates the scraped users in filename.csv in the database. Check if all the users are populated using the django                 admin portal.
3. For polls, edit polls.csv inside Scrape folder keeping the structure same as in the sample file already present.
     * all; xyz means that xyz poll needs to be created for all departments.
     * Now navigate back to root folder of project.
     * Remember, your django server must be running on the other terminal and export the django settings env variable if not already done.
     * Then type: python addPolls.py
     * This populates the polls in the database. Again verify the polls in database using the admin portal
4. Now, for redirection to authorization by kerberos system of IIT, you need to edit the Client ID and Client secret inside Config.py      present inside myapp/ provided to you by IIT and the again run the server.
5. Now, when you navigate to localhost:8000 or if you have deployed on IIT's server proceed to login and Enter your credentials. Your      credentials are not saved by us as authorization is done by an API (internal to IIT authorities) to which we redirect and verify by      your kerberos. 
6. Comment this line in urls.py:
```python
 url(r'^yearbook/$', views.yearbook, name='yearbook'),
```

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

### How does the general public use this?
1. On opening the website, you would be greeted with the welcome page, where you'd have to sign in with your Kerberos ID
2. The first thing which someone would want to do is to edit their profile page - add details about themselves.
3. Next, they would want to answer questions about themselves.
4. They can write comments about their friends(inter-department commenting is allowed)
5. They can vote in polls(If a poll is department specific, only students from that departments can vote for students in their department. If a poll has department - 'all', anyone one can vote for anyone)
6. If they don't want a comment written by someone for them, to be displayed in the yearbook, they can set displayInPdf for that comment to be False.

### Post work to be done by admins
1. Uncomment this line in urls.py: url(r'^yearbook/$', views.yearbook, name='yearbook'),
2. Now if a user browses to .../yearbook, they can see the yearbook of their department.
3. If the admin is logged in via the .../admin site, they can browse to .../yearbook?department=<dept_code>, to open the yearbook of any department.
```
dept_code - department name

chemical - chemical
civil - civil
cse - computer science
ee - electrical
maths - mathematics
mech - mechanical
physics - engineering physics
textile - textile engineering
dbeb - biotechnology
```
4. At this point of time, there are no pictures in yearbooks.
5. Admin must download all the yearbooks, by hitting Ctrl + P once they have opened the yearbooks. Use the following settings to download the yearbooks in a chrome browser:
 * Set the zoom to 125% (yeah, that changes the print of the yearbook)
 * Enable background graphics
 * Set margins to none, if that doesn't look good, let it be default
6. Now we need to optimize the size of the yearbooks using ps2pdf command. To do that run this for each book:
```
  $ ps2pdf <file_input> <file_output>
```
  Alternatively,
  * Create a new folder and put all the downloaded yearbooks inside it. 
  * Create a new folder inside this folder with the name "optimized".
  * Create a new file with the name "optimize.sh" and copy-paste the following inside it,
    ```
    for VAR in $(ls)
    do
            echo $VAR
            ps2pdf $VAR optimized/$VAR
    done
    ```
  * Run this script
7. For Collage Generation details, see the `README` inside 'collage' folder.

## Authors

* [**Mayank Singh Chauhan**](https://github.com/mayanksingh2298)
* [**Atishya Jain**](https://github.com/atishya-jain)


Also see the list of Devclub's [members](https://github.com/orgs/devclub-iitd/people).

## Acknowledgments

* [**Aman Agrawal**](https://github.com/aman71197) for your guidance
* [**Udit Jain**](https://github.com/udit01) for helping with the collage

## Running Locally simplified by Shashwat Shivam
1. To get started with the yearbook follow the steps:
   * Clone the repository
   * Activate the virtalenv if you don't want python to interfere with your global packages
   * pip install -r requirements.txt (For errors regarding psycopg2 refer to further sections)
   * Check .env file deployment mode to be localhost.
   * Export environment variables present in .env file (intended for docker environment) using the command `source <(sed -E -e "s/^([^#])/export \1/" -e "s/=/='/" -e "s/(=.*)$/\1'/" .env)` 
   * Create db (with same name as in env file in local postgres)
   * python manage.py makemigrations (For errors regarding postgresql refer to further sections)
   * python manage.py migrate
   * python manage.py createsuperuser
        * This will ask you for username, password and other details of the superuser you are creating. Remember the credentials. This super user will allow you to handle django database.
   * Run python3 setAdminTable.py to create an admin table object if it does not exists already.
   * python manage.py runserver
        * This starts the Django server at port 8000
        * visit http://localhost:8000/admin on your browser
        * Enter the credentials of the superuser you created
        * Now you can see various tables like user, GenQuestions and Polls.
        * You can add or delete GenQuestions manually as their are only handful of them.
        * Rest of the polls and user entries will be done by the scripts.
        * This portal will be used to setup and verify the database entries.
