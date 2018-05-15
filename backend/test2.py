from django.test import TestCase
from django.test import Client
import os, django, time, datetime
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top.settings')
django.setup()
import random
# Create your tests here.

import requests
import string
from bs4 import BeautifulSoup



c = Client()

response = c.post('/api/get_token/', data={
    'username': 'xixi',
    'password': '456789',
})


import json

data = json.loads(response.content.decode('utf-8'))
print(data['token'])

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

print(response.content.decode('utf-8'))


exit(0)


with open('names.txt', encoding='utf-8', mode='w') as fp:
    for letter in string.ascii_lowercase[:]:
        url = url_pattern.replace('*', letter)
        content = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(content, 'lxml')
        table = soup.find('table', class_='table').tbody
        for tr in table.find_all('tr'):
            name = tr.td.text
            if len(name) > 0:
                fp.write(name + "\t" + str(id_base) + "\n")
                print(name)
                id_base += 1


c = Client()
response = c.post('/api/login', data={
    'username': 'xixi',
    'password': '456789',
})

with open('names.txt', encoding='utf-8') as fp:
    cnt = 0
    for line in fp.readlines():
        cnt += 1
        name, id = line.strip("\n").split("\t")
        if cnt > 500:
            c.post('/api/register_faculty', {
                'username': name,
                'id_number': int(id),
                'user_type': 2,
                'email': '**@163.com'.replace('**', name),
                'name': name,
                'gender': random.choice(['F', 'M']),
                'title': 'professor',
                'department': '计算机',
            })
        else:
            response = c.post('/api/register_student', {
                'username': name,
                'id_number': int(id),
                'user_type': 1,
                'email': '**@126.com'.replace('**', name),
                'name': name,
                'gender': random.choice(['F', 'M']),
                'department': '计算机',
                'grade': '2015',
                'major': '计算机',
                'class_name': random.choice(['1501', '1502', '1503']),
            })
        print(response.content)