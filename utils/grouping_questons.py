import sys
import os
import django
import json
from bs4 import BeautifulSoup as bs

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.

from questions.models import Question
from questions.models import QuestionChoice

from folder.models import Folder


directory = r'C:\Users\MSI\Desktop\BitEd\allQuestions'
 
Step_1_folder = Folder.objects.filter(id=9259).first()
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

        if not Step_1_folder.children.filter(name=subject):
            new_subject_folder = Folder.objects.create()
            new_subject_folder.name = subject
            new_subject_folder.parent = Step_1_folder
            new_subject_folder.type = "S"
            new_subject_folder.save()
        else:
            new_subject_folder = Step_1_folder.children.filter(name=subject).first()

        if not new_subject_folder.children.filter(name=system):
            new_system_folder = Folder.objects.create()
            new_system_folder.name = system
            new_system_folder.parent = new_subject_folder
            new_system_folder.type = "S"
            new_system_folder.save()
        else:
            new_system_folder = (new_subject_folder.children
                                                .filter(name=system).first())

        if not new_system_folder.children.filter(name=topic):
            new_topic_folder = Folder.objects.create()
            new_topic_folder.name = topic
            new_topic_folder.parent = new_system_folder
            new_topic_folder.type = "T"
            new_topic_folder.save()
        else:
            new_topic_folder = (new_system_folder.children
                                                .filter(name=topic).first())
         
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
        new_topic_folder.questions.add(q)

