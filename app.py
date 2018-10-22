from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import requests

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

@ask.launch
def new_ask():
    print("Launch invoked")

    return question("Hi Jatin")


@ask.intent('personalDetails')
def personal_details():
	print("in personal details section")
	return ("you are in personal details module")


@app.route("/", methods=["GET", "POST"])
def index():
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")