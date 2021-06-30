import os
import shutil
import django
django.setup()
from myapp.models import *

from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)

ROOT_DIR = "collage_and_yearbook_personal"
all_students = Student.objects.all()
students_count = Student.objects.count()

counter = 0
for student in all_students:
    counter = counter + 1
    logging.info("Processing user: " + str(student.user) + "...............(" + str(counter) + "/" + str(students_count) + ")")
    
    friendsGroup = []
    friendsGroup.append(str(student.user))
    for closeFriend in student.closeFriends.keys():
        if closeFriend != str(student.user):
            friendsGroup.append(closeFriend)

    folder_path = os.path.join(ROOT_DIR, student.user.username)
    folder_path = os.path.join(folder_path, 'collages')
    os.makedirs(folder_path)

    for friendUserName in friendsGroup:
        i = User.objects.get(username=(friendUserName).lower()).student
        if i.closeFriendsPic:
            shutil.copyfile(i.closeFriendsPic.path, os.path.join(folder_path, os.path.basename(i.closeFriendsPic.name)))



    