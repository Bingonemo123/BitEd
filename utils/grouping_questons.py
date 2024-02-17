import sys
import os
import django
import json 

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from bs4 import BeautifulSoup as bs

from questions.models import Question
from questions.models import QuestionChoice
from django.db.models import Q
from writing.models import UserAnswer
from folder.models import WriteRequestData
from folder.models import Folder

from django.db.models import When, Case, Value
from django.db.models.functions import Length
from django.db.models import Subquery, OuterRef

from django.db.models import F
from django.db.models.lookups import Exact
from django.db.models import Exists


directory = r'C:\Users\MSI\Desktop\BitEd\allQuestions'
 
# iterate over files in
manual_questions = []

# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print('importing', f)
        struct = json.load(open(f))
        explanation = bs(struct["explanation-container"], 'html.parser')
        
        subject = (explanation.find('div', string="Subject")
                              .previousSibling.text)
        system = explanation.find('div', string="System").previousSibling.text
        topic = explanation.find('div', string="Topic").previousSibling.text

        if not Folder.objects.filter(name=subject):
            new_subject_folder = Folder.objects.create()
            new_subject_folder.name = subject
            new_subject_folder.parent = Folder.objects.filter(id=2220).first()
            new_subject_folder.type = "S"
            new_subject_folder.save()

        if not Folder.objects.filter(name=system):
            new_subject_folder = Folder.objects.create()
            new_subject_folder.name = system
            new_subject_folder.parent = (Folder.objects
                                               .filter(name=subject).first())
            new_subject_folder.type = "S"
            new_subject_folder.save()

        if not Folder.objects.filter(name=topic):
            new_subject_folder = Folder.objects.create()
            new_subject_folder.name = topic
            new_subject_folder.parent = (Folder.objects
                                               .filter(name=system).first())
            new_subject_folder.type = "T"
            new_subject_folder.save()
         
        answers_html = bs(struct["answerContainer"], "html.parser")
        answers_list = answers_html.find_all("tr")
        correct_choice = None

        q = Question.objects.create()
        q.question_title = bs(struct['questionText'], 'html.parser').text[:33]
        q.question_body = struct['questionText']
        q.question_explanation = struct["explanation-container"]

        Table_mode = False

        for answer in answers_list:
            if Table_mode is True and answer.select_one('.answer-choice-content') is None:
                continue
            choice = QuestionChoice()
            choice.choice_to = q
            try:
                choice.choice_text = answer.select_one('.answer-choice-content').text
            except AttributeError:
                manual_questions.append(q.id)
                Table_mode = True
                q.question_body += str(answer)
     
            if answer.find("i"):
                correct_choice = choice
            choice.save()
        
        q.correct_choice = correct_choice
        q.save()
        Folder.objects.filter(name=topic).first().questions.add(q)

