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

query_dict = dict()
query_dict["query"] = ""
query_dict["correct_answer"] = ""
query_dict["option_str"] = ""


@ask.launch
def new_ask():
    print("Launch invoked")
    welcome = "Welcome to the quiz Show. \n\n Say 'Lets Begin' to start the quiz. and \n\n Goodbye to terminate the quiz."
    return question(welcome)


@ask.intent('personalDetails')
def personal_details(first_name):
	print("hello" + first_name + "in personal details section")
	welcome = render_template('welcome')
	return question(welcome)


@ask.intent("question_intent")
def display_question():
	random.shuffle(questions_list)
	questions_list_item = questions_list[0]

	query_dict["query"] = questions_list_item["Question"]
	options = questions_list_item["Options"]
	query_dict["option_str"] = options[0] + "\n\n" + options[1] + "\n\n" +options[2] + "\n\n" +options[3]
	query_dict["correct_answer"] = questions_list_item["Answers"]

	print("In question_intent, Correct answer is " + query_dict["correct_answer"])
	return question(query_dict["query"] + "\n\n" + query_dict["option_str"])


@ask.intent("answer_intent")
def display_answer(user_answer):
	if user_answer.upper() == query_dict["correct_answer"].upper():
		return question("Your answer is right.")

	print("Correct Answer is Option " + query_dict["correct_answer"])	
	return question("Correct Answer is Option " + query_dict["correct_answer"])


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
	app.run(debug=True, host="0.0.0.0")