import sys, os, django
import random

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd") # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from bs4 import BeautifulSoup

from questions.models import Question
from questions.models import QuestionChoice
from django.db.models import Q
from writing.models import UserAnswer
from tiles.models import WriteRequestData
from tiles.models import Tile

from django.db.models import When, Case, Value
from django.db.models.functions import Length
from django.db.models import Subquery, OuterRef

from django.db.models import F
from django.db.models.lookups import Exact
from django.db.models import Exists

def is_image_extension(url):
    # List of common image extensions. You can extend this list if needed.
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico']
    
    # Convert url to lowercase and check if it ends with any of the image extensions.
    return any(url.lower().endswith(ext) for ext in image_extensions)

questions = Question.objects.all()

for q in questions:
    print(q, end=" :: ")

    soup_body = BeautifulSoup(q.question_body, "html.parser")
    soup_explan = BeautifulSoup( q.question_explanation, "html.parser")

   
    links_in_question = soup_body.find_all(['a']) + soup_explan.find_all(['a'])
    image_links = []

    for link in links_in_question:
        if link.get('href'):
            if is_image_extension(link.get('href')):
                image_links.append(link)
          
    
    if not image_links:
        print( 'No image links')
    else:
        for link, link_next in zip(image_links[1:], image_links[2:]):
            link['href'] = link_next['href']

        if len(image_links) > 1:
            image_links[-1]["href"] = "#"

        q.question_body = str(soup_body)
        q.question_explanation = str(soup_explan)
        q.save()

# link in qbody and explanations
# fist link is  correct


# duplicate questions = 20563
# pk user answer 1942, 1862


# Question object (6996) Question object (6981) ?
# Question object (9566) Question object (9563) + 
# Question object (10146) Question object (10145) + 
# Question object (11948) Question object (11947) +


# Biostatistics 
# Questions without graphs
# user answer 1682
# 1822
# 2231

# without sound
# 1966

# order change user answer 1718 + 
# 1846 + 
