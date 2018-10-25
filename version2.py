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

answer = ""

@ask.launch
def new_ask():
    print("Launch invoked")
    welcome = "Welcome to the quiz Show. \n\n Say 'Lets Begin' to start the quiz. and \n\n Goodbye to terminate the quiz."
    return question(welcome)


@ask.intent("question_intent")
def display_question():

	random.shuffle(questions_list)
	questions_list_item = questions_list[0]
	print(questions_list_item)

	query_dict["query"] = questions_list_item["Question"]
	print(query_dict["query"])

	options = questions_list_item["Options"]
	query_dict["option_str"] = options[0] + "\n\n" + options[1] + "\n\n" +options[2] + "\n\n" +options[3]
	print(query_dict["option_str"])

	query_dict["correct_answer"] = questions_list_item["Answers"]
	
	print(query_dict["correct_answer"])
	storing_global_var(query_dict["correct_answer"])

	global answer
	print("Global var in question intent : " + answer)

	return question(query_dict["query"] + "\n\n" + query_dict["option_str"])


def storing_global_var(params_answer):
	global answer
	if params_answer == "":
		return answer

	answer = params_answer
	return answer


@ask.intent("answer_intent")
def display_answer(user_answer):

	global answer
	print("Global var in answer intent : " + answer)

	# print(type(user_answer))
	# print("user ans : " + user_answer.upper())

	# empty_str = ""
	# stored_ans = storing_global_var(empty_str)
	# print("correct ans : " + stored_ans.upper())
	
	if user_answer.upper() == answer.upper():
		print(answer.upper())
		return question("Your answer is right.")
	else:
		return question("you answered " + user_answer.upper() +" ....Correct answer is  " + query_dict["correct_answer"].upper())


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