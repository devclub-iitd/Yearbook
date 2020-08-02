import os
import shutil
import django
django.setup()
from myapp.models import *
from django.template.loader import render_to_string

from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)

all_students = Student.objects.all()
students_count = Student.objects.count()
GenQuestions = GenQuestion.objects.all()

counter = 0
for student in all_students:
    counter = counter + 1
    logging.info("Processing user: " + str(student.user) + "...............(" + str(counter) + "/" + str(students_count) + ")")
    
    friendsGroup = []
    friendsGroup.append(str(student.user))
    for closeFriend in student.closeFriends.keys():
        if closeFriend != str(student.user):
            friendsGroup.append(closeFriend)

    allFriends = []
    for friendUserName in friendsGroup:
        i = User.objects.get(username=(friendUserName).lower()).student
        gen_GenQuestions=list([])
        for q in GenQuestions:
            if ((str(q.id) in i.AnswersAboutMyself) and i.AnswersAboutMyself[str(q.id)]!=""):
                gen_GenQuestions.append([])
                gen_GenQuestions[-1] = [q.question,i.AnswersAboutMyself[str(q.id)]]
        i.AnswersAboutMyself=list(gen_GenQuestions)

        gen_commentsIGet=list([])
        for a in i.CommentsIGet:
            if(User.objects.filter(username=a['fromWhom']).exists() and a['comment']!="" and a['displayInPdf']=="True"):
                gen_commentsIGet.append([])
                gen_commentsIGet[-1] = [a['comment'],User.objects.filter(username=a['fromWhom'])[0].student.name]
        i.CommentsIGet=list(gen_commentsIGet)
        allFriends.append(i)

    # deployPort = os.getenv("DEPLOY_PORT")
    # if not deployPort:
    #     deployPort = '8000'
    # baseURL = 'http://0.0.0.0:' + deployPort
    baseURL = 'https://yearbook.devclub.in/'
    context={"students": allFriends, "user": student, "baseURL": baseURL}
    content = render_to_string('myapp/personalYearbook.html', context)
    with open('media/' + str(student.user) + '_personalYearbook.html', 'w') as static_file:
        static_file.write(content)
    