from django.test import TestCase
from django.test import Client
import os, django, time, datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top.settings')
django.setup()
# Create your tests here.

c = Client()

nowTime = lambda:int(round(time.time() * 1000))

insert_question = False
insert_paper = False
query_paper = True

if insert_question:
    response = c.post('/api/online_testing/question/', {
        "description": "Greedy method is a special case of local search.",
        "type": "Judge",
        "tag": "Local search",
        "choice_list": ['T', 'F'],
        "answer_list": [1],
        'level': 0
    })

    response = c.post('/api/online_testing/question/', {
        "description": "In the red-black tree that results after successively inserting the "
                       "keys 41; 38; 31; 12; 19; "
                       "8 into an initially empty red-black tree, which one of the following "
                       "statements is FALSE?",
        "type": "Choice",
        "tag": "Data Structure",
        "choice_list": ['38 is the root', '19 and 41 are siblings, and they are both red',
                        '12 and 31 are siblings, and they are both black', '8 is red'],
        "answer_list": [1],
        'level': 2,
    })

if insert_paper:
    d = datetime.datetime.now()
    response = c.post('/api/online_testing/paper/', {
        "papar_name": "Greedy method is a special case of local search.",
        'auto': True,
        'tag_list': [],
        'start_time': d + datetime.timedelta(days=2),
        'deadline': d + datetime.timedelta(days=7),
        'duration': 120,
        'num_choice': 2,
        'num_judge': 1,
    })
    print(response.content.decode('utf-8'))

if query_paper:
    c.get('/api/online_testing/paper/2/')