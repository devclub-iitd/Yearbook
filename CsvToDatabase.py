import django
import csv
django.setup()
from myapp.models import *
import logging
import os

logger = logging.getLogger(__name__)

pswd = os.environ["pswd"]
ind = 0
with open("./Scrape/fileName.csv", "rU") as file:
	reader = csv.reader(file, delimiter=';')
	for col in reader:	
		ind = ind+1
		logger.info(ind)
		user_passwd = pswd + col[0].lower()[3:5]
		u = User(username=col[0].lower(), password=user_passwd)
		s = Student(name=col[1], department=col[2])
		try:
			u.save()
			u.student = s
			u.student.save()
		except:
			logger.exception("EXCEPTION: User Already Exists. Continuing")
