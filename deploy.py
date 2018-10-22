from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import requests
import urllib
import re
import random

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

@ask.launch
def new_ask():
    # welcome = render_template('welcome')
    # return question(welcome) \
    #     .simple_card(title='Launch page', content='Make your time')
    return question("Hi Jatin")

@ask.intent('intro')
def introduction(name):
    # dummy_string = "Hi " + name + ". Its good to see you."
    # return question(dummy_string) \
    #     .simple_card(title=' Intro page...', content='Make your time')
    return statement("yo")

@app.route("/", methods=["GET", "POST"])
def index():
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")