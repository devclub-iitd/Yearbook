# Yearbook

This webapp is used to generate the yearbook every year for the final year students. 



### Database struncture
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

### How is this supposed to work?
### Prior work to be done by admins
1. To get started with the yearbook follow the steps:
   * Clone the repository
   * Activate the virtalenv if you don't want python to interfere with your global packages
   * pip install -r requirements.txt
   * python manage.py makemigrations
   * python manage.py migrate
   * python manage.py createsuperuser
        * This will ask you for username, password and other details of the superuser you are creating. Remember the credentials. This             super user will allow you to handle django database.
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
* [**Arshdeep Singh**](https://github.com/4rshdeep)


Also see the list of Devclub's [members](https://github.com/orgs/devclub-iitd/people).

## Acknowledgments

* [**Aman Agrawal**](https://github.com/aman71197) for your guidance
* [**Udit Jain**](https://github.com/udit01) for helping with the collage

