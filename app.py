from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
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


@ask.launch
def new_ask():
    print("Launch invoked")
    welcome = "Welcome to the quiz Show.\n\nThere are totally 5 questions.\n\nSay 'Go to Question Qno.' to start the quiz. and \n\n Goodbye to terminate the quiz."
    return question(welcome)


@ask.intent("question_intent")
def display_question(qno):
	qno = int(qno)

	if qno > len(questions_list):
		return question("There are only 5 questions. So select from 1 to 5.")

	questions_list_item = questions_list[qno]
	print(questions_list_item)

	query = questions_list_item["Question"]
	print(query)

	options = questions_list_item["Options"]
	option_str = options[0] + "\n\n" + options[1] + "\n\n" +options[2] + "\n\n" +options[3]
	print(option_str)

	print("Storing Question no in txt file")
	qno_file = open("qno.txt","w")
	qno_file.write("Question No:" + str(qno))
	qno_file.close()

	return question(query + "\n\n" + option_str)


@ask.intent("answer_intent")
def display_answer(user_answer):
	print("Reading from qno file.")
	qno_file = open("qno.txt","r")
	qno = qno_file.read()

	qno = int(qno)
	correct_answer = questions_list[qno]["Answers"]
	if user_answer.upper() == correct_answer.upper():
		return question("Your answer is right.")
	else:
		return question("you answered " + user_answer.upper() +" ....Correct answer is  " + correct_answer.upper())


@ask.intent("terminate")
def terminate_quiz():
	return statement("See You Later")


@app.route("/", methods=["GET", "POST"])
def index():
	print(questions_list[0]["Question"])
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)