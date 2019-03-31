# -*- coding:utf-8 -*- 

import sqlite3

# cursor.execute('create table ch_corpus(id integer \
#     primary key AUTOINCREMENT, qustion text, answer text, source varchar(127))')
DB_NAME = 'chat_corpus.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'create table chat_corpus(id integer primary key autoincrement,\
        question text, answer text, source varchar(127))')
    cursor.close()
    conn.commit()
    conn.close()

def deal_with_xiaohuangji():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open('corpus/xiaohuangji.txt', encoding='utf8') as f:
        line = f.readline()
        line = line.strip()
        jline = line.split('|')
        if jline and len(jline) == 2:
            cursor.execute(
                "insert into chat_corpus(question, answer, source) \
                values(?,?,?)", (jline[0], jline[1], 'xiaohuangji'))
        while line:
            line = f.readline()
            line = line.strip()
            jline = line.split('|')
            if jline and len(jline) == 2:
                cursor.execute(
                    "insert into chat_corpus(question, answer, source) \
                    values(?,?,?)", (jline[0], jline[1], 'xiaohuangji'))
    cursor.close()
    conn.commit()
    conn.close()

def check_xiaohuangji():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    result = cursor.execute(
        'select * from chat_corpus where source=\'xiaohuangji\' limit 25')
    for row in result:
        print(row[1], ' ', row[2])
    cursor.close()
    conn.close()

def deal_with_gossip():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    with open('corpus/gossip.txt', encoding='utf8') as f:
        line = f.readline()
        line = line.strip()
        jline = line.split('#')
        if jline and len(jline) == 3:
            cursor.execute(
                "insert into chat_corpus(question, answer, source) \
                values(?,?,?)", (jline[1], jline[2], 'gossip'))
        while line:
            line = f.readline()
            line = line.strip()
            jline = line.split('#')
            if jline and len(jline) == 3:
                cursor.execute(
                    "insert into chat_corpus(question, answer, source) \
                    values(?,?,?)", (jline[1], jline[2], 'gossip'))
    cursor.close()
    conn.commit()
    conn.close()

def check_gossip():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    result = cursor.execute(
        'select * from chat_corpus where source=\'gossip\' limit 125')
    for row in result:
        print(row[1], ' ', row[2])
    cursor.close()
    conn.close()

# create_table()
# deal_with_xiaohuangji()
# check_xiaohuangji()
# deal_with_gossip()
# check_gossip()

