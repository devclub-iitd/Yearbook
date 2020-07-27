import os
import django
django.setup()
from myapp.models import *
import logging
logger = logging.getLogger(__name__)

all_students = Student.objects.all()
students_count = Student.objects.count()

counter = 0
for i in all_students:
    counter = counter + 1   
    username = str(i.user)
    deptname = str(i.department)
    logging.info("Processing user: " + username + " dept: " + deptname + "...............(" + str(counter) + "/" + str(students_count) + ")")
    i.closeFriends = {}
    i.save()