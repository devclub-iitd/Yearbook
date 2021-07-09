import os, errno
import re
import subprocess
import django
import sys
import shutil
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from PIL import Image, ImageOps
from collage import collage_maker

import img2pdf
django.setup()
from myapp.models import *
from wordcloud import WordCloud
from django.core.files import File

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

FIRST_PAGE_LINES = 10
NEXT_PAGE_LINES = 25

from utils.emoji import emojis
reps = {"\\": "\\textbackslash", "\n": "\\\\", "\r": "", "_": "\_", "~": "\~", "$": "\$", "{": "\{", "}": "\}", "&": "\&", "%": "\%", "^": "\\textsuperscript{$\wedge$}", "#": "\#"}

rep = {**reps, **emojis}
rep = dict((re.escape(k), v) for k, v in rep.items())

def text_to_latex(text):
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


student = User.objects.get(username=(sys.argv[1]).lower()).student

GenQuestions = GenQuestion.objects.all()

friendsGroup = []
friendsGroup.append(str(student.user))
for closeFriend in student.closeFriends.keys():
    if closeFriend != str(student.user):
        friendsGroup.append(closeFriend)


##########################################
# generate wordcloud

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


color_to_words = {
    '#00cc99': [Adjective.adjective_list[0][0]],
    '#9999ff': [Adjective.adjective_list[1][0]],
    '#ffff00': [Adjective.adjective_list[2][0]],
    '#cc9900': [Adjective.adjective_list[3][0]],
    '#ff9933': [Adjective.adjective_list[4][0]],
    '#3333ff': [Adjective.adjective_list[5][0]],
    '#00cc00': [Adjective.adjective_list[6][0]],
    '#ff00ff': [Adjective.adjective_list[7][0]],
    '#00ccff': [Adjective.adjective_list[8][0]],
    '#ff3300': [Adjective.adjective_list[9][0]],
    '#cc33ff': [Adjective.adjective_list[10][0]],
    '#ff9933': [Adjective.adjective_list[11][0]],
    '#3333ff': [Adjective.adjective_list[12][0]],
    '#00cc00': [Adjective.adjective_list[13][0]],
    '#ff00ff': [Adjective.adjective_list[14][0]]
}

default_color = '#ff9999'

grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

def createWordCloud(student):
    """Generate and save wordcloud for student
    """

    dictionary = {}  # { adjective : vote }
    for adj in student.AdjectivesIGet.all():
        dictionary[adj.adjective] = adj.byWhom.count()

    wordcloud = WordCloud(width=800, height=550, margin=60, max_words=300,min_font_size=20,
                          background_color="rgba(255,255,255,0)", mode="RGBA").generate_from_frequencies(dictionary)

    wordcloud.recolor(color_func=grouped_color_func)

    wordcloud_directory = 'media/wordcloud'
    if not os.path.exists(wordcloud_directory):
        os.makedirs(wordcloud_directory)   
    image_url = wordcloud_directory + '/' + student.user.username + '_wc.png'

    wordcloud.to_file(image_url)
    student.WordCloud.save(student.user.username + 'wc_image.png',
                           File(open(image_url, 'rb')))
    student.save()


if student.AdjectivesIGet.exists():
    createWordCloud(student)

##########################################
# prepare directory

ROOT_DIR = "collage_and_yearbook_personal"
student_dir_path = os.path.join(ROOT_DIR, student.user.username)
folder_path = os.path.join(student_dir_path, 'collages')
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(folder_path)

if student.closeFriendsPic:
    ImageOps.expand(Image.open(student.closeFriendsPic.path),border=400,fill='white').save(os.path.join(student_dir_path, "closeFriendsPic.jpg"))

for friendUserName in friendsGroup:
    i = User.objects.get(username=(friendUserName).lower()).student
    if i.closeFriendsPic:
        shutil.copyfile(i.closeFriendsPic.path, os.path.join(folder_path, os.path.basename(i.closeFriendsPic.name)))


##########################################
# generate collage

ROOT_DIR = "collage_and_yearbook_personal"
BATCH_SIZE = 8

dirs = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]

current_dir = str(student.user)
current_dir = os.path.join(ROOT_DIR, current_dir)
current_dir = os.path.join(current_dir, 'collages')

img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
folder_count = 0    
while (img_names != []):
    folder_path = os.path.join(current_dir, str(folder_count))
    try :
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print ("Folder created", folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        folder_count += 1
        continue
    img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    for i in range(BATCH_SIZE):
        try : 
            oldfilepath = os.path.join(current_dir,img_names[i])
            newfilepath = os.path.join(folder_path,img_names[i])
        except Exception as e : 
            print (e)
            break
        shutil.move(oldfilepath,newfilepath)

    folder_count += 1
    img_names = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]



dir_names = [f for f in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, f))]
for folder in dir_names:
    folder_path = os.path.join(current_dir, folder)
    image_path = os.path.join(current_dir,'out_'+folder+'.jpg')
    args = {'folder':folder_path, 'width':850 , 'init_height':720, 'shuffle' : True , 'output' : image_path}
    collage_maker.prepare(args)

    # add margin
    ImageOps.expand(Image.open(image_path),border=60,fill='white').save(image_path)

    # convert to pdf
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(os.path.join(current_dir,'out_'+folder+'.pdf'), "wb") as f:
        f.write(img2pdf.convert(image_path, layout_fun=layout_fun))


##########################################
# generate tex and pdf

FRAME_SIZE = 250
allFriends = []
for friendUserName in friendsGroup:
    i = User.objects.get(username=(friendUserName).lower()).student
    i.oneliner = text_to_latex(i.oneliner)
    i.future = text_to_latex(i.future)
    i.email = text_to_latex(i.email)
    i.phone = text_to_latex(i.phone)
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
            comment_lines = a['comment'].count('\n') + int(len(a['comment']) / 117)
            current_lines += comment_lines
            newPage = False
            if current_lines > FRAME_SIZE:
                max_lines = NEXT_PAGE_LINES
                current_lines = comment_lines
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

subprocess.run(["lualatex", "-output-directory=" + output_directory, latex_file])   # generate pdf from tex
subprocess.run(["pdfjam", "-q", "--outfile", out_file, "--paper", "a4paper", pdf_file])   # convert to a4


##########################################
# merge pdfs

FRONT_PAGE = "myapp/static/myapp/pdf/Yearbook21GTA.pdf"
ROOT_DIR = "collage_and_yearbook_personal/"

current_dir = str(student.user)
student_name = current_dir
current_dir = os.path.join(ROOT_DIR, current_dir)
yearbook_pdf = os.path.join(current_dir, 'yearbook.pdf')
collage_dir = os.path.join(current_dir, 'collages')
collage_pdfs = os.listdir(collage_dir)
# frontpage_pdf = os.path.join(ROOT_DIR, 'frontpage.pdf')

a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # specify page size (A4)
layout_fun = img2pdf.get_layout_fun(a4inpt)

# convert close friends pic to pdf
close_friends_pic_pdf = os.path.join(current_dir,'closeFriendsPic.pdf')
close_friends_pic = os.path.join(current_dir,'closeFriendsPic.jpg')
if os.path.exists(close_friends_pic):
    with open(close_friends_pic_pdf, "wb") as f:
        f.write(img2pdf.convert(close_friends_pic, layout_fun=layout_fun))

merger = PdfFileMerger()
merger.append(FRONT_PAGE)
merger.append(yearbook_pdf)

if os.path.exists(close_friends_pic_pdf):
    merger.merge(1, close_friends_pic_pdf)

for collage in collage_pdfs:
    if collage.endswith('.pdf'):
        pdf = os.path.join(collage_dir, collage)
        merger.append(pdf)

merger.write(os.path.join(current_dir, 'final_yearbook_' + student_name + '.pdf'))
merger.close()