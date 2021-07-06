import os
import django
django.setup()
from myapp.models import *
from wordcloud import WordCloud
from django.core.files import File

import logging
logger = logging.getLogger(__name__)


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


all_students = Student.objects.all()
students_count = Student.objects.count()

counter = 0
for i in all_students:
    counter = counter + 1
    logging.info("Processing user: " + str(i.user) + "...............(" + str(counter) + "/" + str(students_count) + ")")
    if i.AdjectivesIGet.exists():
        createWordCloud(i)
        logger.info("Student: %s - Wordcloud created/updated", i.user)
    else:
        logger.info("Student: %s - No adjectives for user", i.user)