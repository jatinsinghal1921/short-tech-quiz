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
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome) \
        .simple_card(title='Launch page', content='Make your time')

@ask.intent('intro')
def introduction(name):
    dummy_string = "Hi " + name + ". Its good to see you."
    return question(dummy_string) \
        .simple_card(title='CATS says...', content='Make your time')



# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True)