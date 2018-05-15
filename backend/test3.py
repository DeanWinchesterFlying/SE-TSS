from django.test import TestCase
from django.test import Client
import os, django, time, datetime
import json
import string
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top.settings')
django.setup()

c = Client()

response = c.post('/api/get_token/', data={
    'username': 'Zachariah',
    'password': '000512',
})

data = json.loads(response.content.decode('utf-8'))
print(data)
print(data['token'])

course_list = ["21120471", "21121340", "21191890", "21121170", "21120261"]
tag_list = ["tag" + c for c in string.ascii_uppercase]
print(tag_list)

import random

for i in range(100):
    if random.randint(0, 1) == 1:
        response = c.post('/api/online_testing/question/', {
            "description": "This is description of a question.....",
            "type": "Choice",
            "tag": random.choice(tag_list),
            "choice_list": ['choice1', 'choice2',
                            'choice3', 'choice4'],
            "answer_list": [random.randint(0, 4)],
            'level': random.randint(0, 3),
            'provider': 'Zachariah',
            'course': random.choice(course_list)
        }, HTTP_AUTHORIZATION='JWT ' + data['token'])
    else:
        response = c.post('/api/online_testing/question/', {
            "description": "This is description of a question.....",
            "type": "Judge",
            "tag": random.choice(tag_list),
            "choice_list": ['T', 'F'],
            "answer_list": [1] if random.randint(0, 1) == 1 else [0],
            'level': random.randint(0, 4),
            'provider': 'Zachariah',
            'course': random.choice(course_list)
        }, HTTP_AUTHORIZATION='JWT ' + data['token'])
    print(response.content.decode('utf-8'))

exit(0)

response = c.get('/api/course/', HTTP_AUTHORIZATION='JWT ' + data['token'])
print(response.content.decode('utf-8'))

c.post('/api/course/', {
    "course_id":"21120471",
    "name":"编译原理",
    "credit":4.0,
    "capacity":60,
    "classroom":"玉泉曹光彪西-503",
    "assessment":"考试",
    "state":2}, HTTP_AUTHORIZATION='JWT ' + data['token']
)

c.post('/api/course/', {
    "course_id":"21121340",
    "name":"计算机网络",
    "credit":4.5,
    "capacity":60,
    "classroom":"玉泉曹光彪西-503",
    "assessment":"考试",
    "state":2}, HTTP_AUTHORIZATION='JWT ' + data['token']
)

c.post('/api/course/', {
    "course_id":"21191890",
    "name":"人工智能",
    "credit":3.5,
    "capacity":60,
    "classroom":"玉泉曹光彪西-503",
    "assessment":"考试",
    "state":2}, HTTP_AUTHORIZATION='JWT ' + data['token']
)

c.post('/api/course/', {
    "course_id":"21121170",
    "name":"B/S体系软件设计",
    "credit":4.5,
    "capacity":60,
    "classroom":"玉泉曹光彪西-503",
    "assessment":"考试",
    "state":2}, HTTP_AUTHORIZATION='JWT ' + data['token']
)
exit(0)

