#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import jieba
jieba.load_userdict("words.txt")

url = 'http://127.0.0.1:5001/chatbot/get_answer'
headers = {'Content-Type': 'application/json'}

question = '发图'
print(' '.join(jieba.cut(question)))
r = requests.post(url, json={'question':question}, headers=headers)
print(r.json())