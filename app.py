from flask import Flask, render_template
from flask_ask import Ask, statement, question
from datetime import datetime
import requests
import json
import random

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

### Global Variables
quizFile = open("quiz.json","r")
questions_list = json.load(quizFile)
i = 0
score = 0

@ask.launch
def new_ask():
    print("Launch invoked")
    welcome = "Welcome to the quiz Show.\n\nThere are totally 5 questions.\n\nSay 'Go to Question Qno.' to start the quiz. and \n\n Goodbye to terminate the quiz."
    return question(welcome)


@ask.intent("question_intent")
def display_question():
	global i
	index = i
	query, option_str = fetch_question(index)
	return question(query + "\n\n" + option_str)


def fetch_question(index):
	questions_list_item = questions_list[index]
	print(questions_list_item)

	query = questions_list_item["Question"]
	print(query)

	options = questions_list_item["Options"]
	option_str = options[0] + "\n\n" + options[1] + "\n\n" +options[2] + "\n\n" +options[3]
	print(option_str)

	return query, option_str


@ask.intent("answer_intent")
def display_answer(user_answer):
	global i
	global score
	print("index : " + str(i))
	correct_answer = questions_list[i]["Answers"]
	
	reply = ""
	if user_answer.upper() == correct_answer.upper():
		reply = "Correct Answer. \n\n"
		score = score + 1
	else:
		reply = "Wrong Answer. \n\n"

	i = i+1
	if i >= len(questions_list):
		reply = reply + "Your Final Score is " + score + "\n\nSee You Later "
		return statement(reply)
	else:
		query, option_str = fetch_question(i)
		reply = reply + "Next Question is ... \n\n" + query + "\n\n" + option_str
		return question(reply)
	
		
@ask.intent("terminate")
def terminate_quiz():
	global score
	reply = "Your Final Score is " + score
	return statement(reply + "\n\nSee You Later")


@app.route("/", methods=["GET", "POST"])
def index():
	print(questions_list[0]["Question"])
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)