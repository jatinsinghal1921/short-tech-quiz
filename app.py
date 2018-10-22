from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from datetime import datetime
import requests

# --------------------------------------------------------------------------------------------
# INITIALISATION

app = Flask(__name__)
ask = Ask(app, "/alexa")

email_dict = {}

sender_id = ""
password = ""
receiver_id = ""
email_subject = ""
email_body = ""


@ask.launch
def new_ask():
    print("Launch invoked")

    return question("Hi Jatin")


@ask.intent('personalDetails')
def personal_details(first_name):
	print("hello" + first_name + "in personal details section")
	welcome = render_template('welcome')
	return question(welcome)


@ask.intent('composeMail')
def compose_mail():
	return question("Please provide few details.\n Specify sender Email address by saying 'From address is ....'")


@ask.intent('fromAddress')
def get_from_address(from_address): 
	email_dict['sender_id'] = from_address
	return question("Now enter your password by saying 'Password is ....")


@ask.intent('password')
def get_password(pswd):
	email_dict['password'] = pswd
	return question("Now enter receiver email address by saying 'To address is ....")


@ask.intent('toAddress')
def get_to_address(to_address): 
	email_dict['receiver_id'] = to_address
	return question("Now enter subject of the mail by saying 'Subject is ....")


@ask.intent('emailSubject')
def get_to_address(subj):
	email_dict['email_subject'] = subj
	return question("Now enter content of the mail by saying 'Content is ....")


@ask.intent('emailBody')
def get_to_address(body): 
	email_dict['email_body'] = body
	return question("Now send the email by saying 'Send the mail'")

@ask.intent('sendMail')
def get_to_address():
	if len(email_dict) < 5:
		return question("Please enter all the details, before we can send the mail.")

	print("sender : " + email_dict['sender_id'] + "\n" + "password : " + email_dict['password'] + "\n" + \
		"receiver : " + email_dict['receiver_id'] + "\n" + "Email Subject : " + email_dict['email_subject'] + "\n" + "Content : " + email_dict['email_body'])
	return question("sender : " + email_dict['sender_id'] + "\n" + "password : " + email_dict['password'] + "\n" + \
		"receiver : " + email_dict['receiver_id'] + "\n" + "Email Subject : " + email_dict['email_subject'] + "\n" + "Content : " + email_dict['email_body'])



@app.route("/", methods=["GET", "POST"])
def index():
	return "Hello World"

# --------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")