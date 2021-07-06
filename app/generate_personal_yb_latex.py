import os
import re
import subprocess
import django
django.setup()
from myapp.models import *

from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)

import jinja2

latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%-',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

FIRST_PAGE_LINES = 20
NEXT_PAGE_LINES = 35

def text_to_latex(text):
    rep = {"\n": "\\\\", "\r": "", "_": "\_", "~": "\~", "$": "\$", "{": "\{", "}": "\}"}

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


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
                gen_GenQuestions[-1] = [q.question, text_to_latex(i.AnswersAboutMyself[str(q.id)])]
        i.AnswersAboutMyself=list(gen_GenQuestions)

        gen_commentsIGet=list([])
        current_lines = 0
        max_lines = FIRST_PAGE_LINES
        for a in i.CommentsIGet:
            if(User.objects.filter(username=a['fromWhom']).exists() and a['comment']!="" and a['displayInPdf']=="True"):
                gen_commentsIGet.append([])
                current_lines += a['comment'].count('\n') + int(len(a['comment']) / 117)
                newPage = False
                if current_lines > max_lines:
                    max_lines = NEXT_PAGE_LINES
                    current_lines = 0
                    newPage = True
                gen_commentsIGet[-1] = [text_to_latex(a['comment']), User.objects.filter(username=a['fromWhom'])[0].student.name, newPage]
        i.CommentsIGet=list(gen_commentsIGet)
        allFriends.append(i)

    template = latex_jinja_env.get_template('personal_yb_template.tex')

    context={"students": allFriends, "user": student}
    document = template.render(context)
    
    output_directory = "collage_and_yearbook_personal/" + str(student.user) + "/"
    latex_file = output_directory + 'personal_yb.tex'
    pdf_file = output_directory + 'personal_yb.pdf'
    out_file = output_directory + 'yearbook.pdf'

    with open(latex_file,'w') as output:
        output.write(document)

    subprocess.run(["pdflatex", "-output-directory=" + output_directory, latex_file])   # generate pdf from tex
    subprocess.run(["pdfjam", "-q", "--outfile", out_file, "--paper", "a4paper", pdf_file])   # convert to a4
