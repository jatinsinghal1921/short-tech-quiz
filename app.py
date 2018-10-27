from flask import Flask, render_template
from flask_ask import Ask, statement, question
from datetime import datetime
import requests
import json
import random
import pickle

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
    welcome = "Welcome to the quiz Show.\n\nFollowing are the Quiz rules..\n\nThere are totally " + str(len(questions_list)) + " questions with each question having 4 options A,B,C and D. \n\nThere is only one correct answer. Select the answer by saying 'Option A or Option B or option C or Option D'. You can terminate the quiz at any time by saying terminate. The score will be displayed at the end of the quiz or on termination."
    return question(welcome)


@ask.intent("question_intent")
def display_question():
	index = 0
	query, option_str = fetch_question(index)

	write_pickle(index,0)

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


def write_pickle(index,score):
	data_dict = {}
	data_dict["qestion_index"] = index
	data_dict["Score"] = score
	data_file = open("data.pickle","wb")
	pickle.dump(data_dict,data_file)
	data_file.close()	


def read_pickle():
	data_file = open("data.pickle","rb")
	data_dict = pickle.load(data_file)
	i = data_dict["qestion_index"]
	score = data_dict["Score"]
	data_file.close()
	return i, score


@ask.intent("answer_intent")
def display_answer(user_answer):
	i, score = read_pickle()

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
		reply = reply + "Your Final Score is " + str(score) + "\n\nSee You Later "
		return statement(reply)
	
	write_pickle(i,score)
	query, option_str = fetch_question(i)
	reply = reply + "Next Question is ... \n\n" + query + "\n\n" + option_str
	return question(reply)
	
		
@ask.intent("terminate")
def terminate_quiz():
	i, score = read_pickle()
	reply = "Your Final Score is " + str(score)
	return statement(reply + "\n\nSee You Later")


@ask.intent("AMAZON.FallbackIntent")
def fallback():
	reply = "I didn't understand you.\nTo start quiz say, 'Lets begin'.\nTo terminate say 'terminate'. To answer the question say option Keyword and then A or B or C or D. "
	return question(reply)


@ask.intent("AMAZON.CancelIntent")
def cancel():
	reply = "Exiting the Quiz"
	return statement(reply)


@ask.intent("AMAZON.StopIntent")
def fallback():
	reply = "Exiting the Quiz"
	return statement(reply)


@ask.intent("AMAZON.HelpIntent")
def fallback():
	reply = "I didn't understand you.\nTo start quiz say, 'Lets begin'.\nTo terminate say 'terminate'. To answer the question say option Keyword and then A or B or C or D. "
	return question(reply)


@ask.intent("AMAZON.NavigateHomeIntent")
def fallback():
	reply = "Exiting the Quiz"
	return statement(reply)


@app.route("/", methods=["GET", "POST"])
def index():
	print(questions_list[0]["Question"])
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0",threaded=True)