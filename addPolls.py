import django
import csv
django.setup()
from myapp.models import *

poll_filename  = "./Scrape/polls.csv"

depts = [
		("chemical", "Chemical Engineering"),
		("civil", "Civil Engineering"),
		("cse", "CS"),
		("ee", "Electrical Engineering"),
		("maths", "Maths"),
		("mech", "Mechanical Engineering"),
		("physics", "Engineering Physics"),
		("textile", "Textile engineering"),
		("dbeb", "Biotechnology"),
	]


def addPoll(poll_quest,dept):
    u = Poll(poll=poll_quest, department=dept)
    u.save()
    print(poll_quest,"------>",dept)
                
    return

with open(poll_filename, "rU") as file:
	reader = csv.reader(file, delimiter=';')
	for col in reader:
		poll_quest = col[1]
		if(col[0]=="all"):
			for dept in depts:
				addPoll(poll_quest,dept[0])
		elif(col[0]=="var"):
			for dept in depts:
				poll_quest_dept = poll_quest.replace("$DEPT$",dept[1])
				addPoll(poll_quest_dept,dept[0])
		elif(col[0][0]=="!"):
			for dept in depts:
				if(dept[0]!=col[0][1:]):
					addPoll(poll_quest,dept[0])
		else:
			for dept in depts:
				if(dept[0]==col[0]):
					addPoll(poll_quest,dept[0])