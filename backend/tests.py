from django.test import TestCase
from django.test import Client
import os, django, time, datetime
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top.settings')
django.setup()
# Create your tests here.

from online_testing.models import Examination
c = Client()

response = c.post('/api/login', data={
    'username': 'Ben',
    'password': '456777',
})

for exam in Examination.objects.all():
    exam.submit = False
    exam.save()


insert_course = False
insert_people = False
insert_question = False
insert_paper = False
query_paper = False
begin_exam = False
test_exam = True

if insert_course:
    c.post('/api/course/', {
        'course_id': '21120261',
        "name": '软件工程',
        "credit": 2.5,
        "capacity": 60,
        "classroom": '玉泉曹光彪西-503',
        "assessment": '考试',
        "state": 2,
    })

if insert_people:
    c.post('/api/register_student', {
        'username': 'Ben',
        'id_number': 123456789123456777,
        'user_type': 1,
        'email': '1qa11@126.com',
        'name': 'Ben',
        'gender': 'M',
        'department': '计算机',
        'grade': '2015',
        'major': '计算机',
        'class_name': '1503',
    })

    c.post('/api/register_student', {
            'username': 'Mary',
        'id_number': 123456789123456877,
        'user_type': 1,
        'email': '11211@126.com',
        'name': 'Mary',
        'gender': 'F',
        'department': '计算机',
        'grade': '2015',
        'major': '计算机',
        'class_name': '1504',
    })

    c.post('/api/register_faculty', {
        'username': 'Yue',
        'id_number': 123456789123256877,
        'user_type': 2,
        'email': '11213@126.com',
        'name': 'Yue',
        'gender': 'F',
        'title': 'professor',
        'department': '计算机',
    })

if insert_question:
    response = c.post('/api/online_testing/question/', {
        "description": "Greedy method is a special case of local search.",
        "type": "Judge",
        "tag": "Local search",
        "choice_list": ['T', 'F'],
        "answer_list": [1],
        'level': 0,
        'course': '21120261',
        'provider': 'Yue',
    })

    print(response.content.decode('utf-8'))

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
        'course': '21120261',
        'provider': 'Yue',
    })

if insert_paper:
    d = datetime.datetime.now()
    response = c.post('/api/online_testing/paper/', {
        "paper_name": "Data Structure MidTerm Exam",
        'auto': True,
        'tag_list': [],
        'start_time': d,
        'deadline': d + datetime.timedelta(days=7),
        'duration': 120,
        'num_choice': 1,
        'num_judge': 1,
        'course': '21120261',
    })
    print(response.content.decode('utf-8'))
    response = c.post('/api/online_testing/paper/', {
        "paper_name": "Data Structure Final Exam",
        'auto': False,
        'question_id_list': [1, 2],
        'start_time': d + datetime.timedelta(days=2),
        'deadline': d + datetime.timedelta(days=7),
        'duration': 120,
        'course': '21120261',
    })
    print(response.content.decode('utf-8'))

if query_paper:
    c.get('/api/online_testing/paper/2/')

if begin_exam:
    response = c.post('/api/online_testing/examination/', data={
        "score": -1,
        "paper": '4a5a36b8-5010-11e8-bcba-c48e8f7f190e',
        "student": 'Ben',
        "teacher": 'Yue'
    })

if test_exam:
    '''response = c.post('/api/online_testing/examination/info/', data={
        'username': 'Ben',
        'paper_id': '8927a25c-5011-11e8-814c-c48e8f7f190e',
    })
    print(response.content.decode('utf-8'))

    response = c.get('/api/online_testing/examination/8927a25c-5011-11e8-814c-c48e8f7f190e/left_time/')
    print(response.content.decode('utf-8'))'''

    answers = {
        '3_answers': [1],
        '4_answers': [2],
    }
    response = c.post('/api/online_testing/examination/87eb0a1c-5373-11e8-9d86-c48e8f7f190e/conservation/', {
        'answers': repr(answers),
    })
    print('save', response.content.decode('utf-8'))

    answers = {
        '3_answers': [1],
        '4_answers': [2],
    }
    response = c.post('/api/online_testing/examination/87eb0a1c-5373-11e8-9d86-c48e8f7f190e/submission/', {
        'answers': repr(answers),
    })
    print('save', response.content.decode('utf-8'))