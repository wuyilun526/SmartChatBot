#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, abort, make_response, request
from chatbot_tfidf import ChatBotTFIDF

app = Flask(__name__)

chatbot = ChatBotTFIDF()
chatbot.train_tfidf()


class ApiServer:

    @app.route('/')
    def index():
        return "Hello, Chatbot!"

    @app.route('/chatbot/get_answer', methods=['POST'])
    def get_answer():
        if request.mimetype == 'application/json':
            data = request.get_json()
            req = data["question"]
        else:
            req = request.form["question"]
        response = chatbot.find_similar_question(req)
        return jsonify({'answer':response})

    def run_server(self):
        app.debug = True
        app.run(host='0.0.0.0', port=5001)


if __name__ == '__main__':
    api_server = ApiServer()
    api_server.run_server()

#curl -H "Content-Type:application/json" -X POST --data '{"question":"123"}' http://127.0.0.1:5001/chatbot/get_answer