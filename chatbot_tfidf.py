#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import random
import sqlite3
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import pairwise
import jieba
jieba.load_userdict("words.txt")


def dist_norm(v1, v2):
    '''距离计算'''
    v1_normalized = v1/sp.linalg.norm(v1.toarray())
    v2_normalized = v2/sp.linalg.norm(v2.toarray())
    delta = v1_normalized - v2_normalized
    return sp.linalg.norm(delta.toarray())


def cos(vector1,vector2):
    '''余弦相似度计算'''
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0;  
    for a,b in zip(vector1,vector2):  
        dot_product += a*b  
        normA += a**2  
        normB += b**2  
    if normA == 0.0 or normB == 0.0:  
        return None  
    else:  
        return dot_product / ((normA*normB)**0.5)  


def supper_cos(total_array, input_array):
    '''余弦相似度计算
    vector1 is tfidf vector
    vector2 is array need to be compared
    '''
    return pairwise.cosine_similarity(total_array, input_array)


def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

class ChatBotTFIDF:

    def __init__(self):

        self.if_idf_vector_list = []
        self.chat_datas = []
        self.vectorizer = TfidfVectorizer(min_df=0, max_df=1.0, max_features=10000)
        self.already_train_flag = 0

    def train_tfidf(self):
        print('1'*100)
        print(time.process_time())
        conn = sqlite3.connect('chat_corpus.db')
        cursor = conn.cursor()
        sql = "select id, question, answer, source from chat_corpus"
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.chat_datas = rows
        seg_list = []
        for r in rows:
            question = ' '.join(jieba.cut(r[1])).strip()
            # temp_str = question.encode('utf-8').strip()
            seg_list.append(question)
        X = self.vectorizer.fit_transform(seg_list)
        b2 = self.vectorizer.get_feature_names()
        print("词语序列：")
        print(b2)
        print('+'*60)
        print('你是谁' in b2)
        print('你' in b2)
        print('是' in b2)
        print('谁' in b2)
        print("TF IDF Vector：")
        print(X.toarray())
        x = X.toarray()
        print("colomn number：%d" % (len(x[0])))
        print("rows number: %d" % (len(x)))
        self.if_idf_vector_list = x
        # numpy.savetxt("tfidf_vector.txt", x)
        self.already_train_flag = 1
        cursor.close()
        conn.close()

    def find_similar_question(self, string):

        new_post = jieba.cut(string)
        str_new = " ".join(new_post)
        new_post_vec = self.vectorizer.transform([str_new])

        if len(self.if_idf_vector_list) == 0:
            self.if_idf_vector_list = numpy.loadtxt("tfidf_vector.txt")        # if vector not exists in memory, load from file
        cos_result = supper_cos(self.if_idf_vector_list, new_post_vec.toarray())
        cos_dict_new = {}
        for x_index, x_vector in enumerate(cos_result):
            cos_dict_new[x_index] = x_vector[0]
        sorted_cos_new = sorted(cos_dict_new.items(), key=lambda x: x[1], reverse=True)
        ticket_ids_new = {}
        best_answers = []
        for i in range(30):
            index, cos_value = sorted_cos_new[i]
            if len(self.chat_datas) != 0 and cos_value > 0.80:
                if len(best_answers) < 5:
                    best_answers.append(self.chat_datas[index][2])
                ticket_ids_new[self.chat_datas[index][0]] = {
                    'cos_value': cos_value,
                    'answer': self.chat_datas[index][2],
                    'question': self.chat_datas[index][1],
                    'source': self.chat_datas[index][3]
                    }
        random.shuffle(best_answers)
        best_answer = ''
        if best_answers:
            best_answer = best_answers[0]
        if not best_answer:
            unknow = ['呵呵', '不知道你在说什么', '哦', '...']
            random.shuffle(unknow)
            best_answer = unknow[0]
        return best_answer


if __name__ == '__main__':

    chatbot = ChatBotTFIDF()
    print(time.process_time())
    chatbot.train_tfidf()
    print(time.process_time())
    question = '介绍你自己'
    print(time.process_time())
    result = chatbot.find_similar_question(question)
    print(time.process_time())
    print(result)