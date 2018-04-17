import django
import csv
django.setup()
from myapp.models import *
from myapp import Config as config

pswd = config.pswd
ind = 0
with open("./Scrape/fileName.csv", "rU") as file:
	reader = csv.reader(file, delimiter=';')
	for col in reader:	
		ind = ind+1
		print(ind)
		u = User(username=col[0].lower(), password=pswd)
		s = Student(name=col[1], department=col[2])
		u.save()
		u.student = s
		u.student.save()