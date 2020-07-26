import os
import shutil
import django
django.setup()
from myapp.models import *
from django.core.files import File

import logging
logger = logging.getLogger(__name__)

ROOT_DIR = "media"
dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

for current_dir in dirs:
    current_dir = os.path.join(ROOT_DIR, current_dir)
    temp_dir = os.path.join(current_dir, 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

all_students = Student.objects.all()
students_count = Student.objects.count()

counter = 0
for i in all_students:
    counter = counter + 1
    username = str(i.user)
    deptname = str(i.department)
    logging.info("Processing user: " + username + " dept: " + deptname + "...............(" + str(counter) + "/" + str(students_count) + ")")
    if i.genPic1:
        filename, file_extension = os.path.splitext(i.genPic1.name)
        dir = os.path.join(ROOT_DIR, deptname + '/temp/' + username + '_genPic1' + file_extension)
        img = os.path.join(ROOT_DIR, i.genPic1.name)
        shutil.copy(img, dir)

    if i.genPic2:
        filename, file_extension = os.path.splitext(i.genPic2.name)
        dir = os.path.join(ROOT_DIR, deptname + '/temp/' + username + '_genPic2' + file_extension)
        img = os.path.join(ROOT_DIR, i.genPic2.name)
        shutil.copy(img, dir)
    