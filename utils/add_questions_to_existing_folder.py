import sys
import os
import django
from bs4 import BeautifulSoup as bs

sys.path.append(r"C:\Users\MSI\Documents\repos\BitEd")
# here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bitedMainProject.settings")
django.setup()

# Now this script or any imported module can use any part of Django it needs.

from questions.models import Question  # noqa: E402
from folder.models import Folder  # noqa: E402

Step_2_folder = Folder.objects.filter(id=7042).first()

# that directory
for question in Question.objects.all():
    print('allocating', question)
    explanation = bs(question.question_explanation, 'html.parser')

    try:
        subject = (explanation.find('div', string="Subject").findPrevious('div').text)
        system = explanation.find('div', string="System").findPrevious('div').text[:128]
        topic = explanation.find('div', string="Topic").findPrevious('div').text[:128]
    except AttributeError:
        continue
    
    if "/" in subject:
        posttopic = topic
        topic = system
        system = subject.split("/")[1][:128]
        subject = subject.split("/")[0][:128]
    else:
        posttopic = None
        subject = subject[:128]

    if not Step_2_folder.children.filter(name=subject):
        new_subject_folder = Folder.objects.create()
        new_subject_folder.name = subject
        new_subject_folder.parent = Step_2_folder
        new_subject_folder.type = "S"
        new_subject_folder.save()
    else:
        new_subject_folder = Step_2_folder.children.filter(name=subject).first()

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
        
    if posttopic:
        if not new_topic_folder.children.filter(name=posttopic):
            new_posttopic_folder = Folder.objects.create()
            new_posttopic_folder.name = posttopic
            new_posttopic_folder.parent = new_topic_folder
            new_posttopic_folder.type = "T"
            new_posttopic_folder.save()
        else:
            new_posttopic_folder = (new_topic_folder.children
                                                    .filter(name=posttopic).first())
        new_posttopic_folder.questions.add(question)
        print('added question', question, 'to folder', new_posttopic_folder.ancestors(
            include_self=True))
    else:
        new_topic_folder.questions.add(question)
        print('added question', question, 'to folder', new_topic_folder.ancestors(
            include_self=True))
