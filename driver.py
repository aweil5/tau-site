from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
from twilio.rest import Client
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='templates/assets')

# Loading Twilio Details
load_dotenv(".env")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

client = Client(account_sid, auth_token)
toll_free_num = os.getenv('from-number')

#Loading in all nums on Startup
df = pd.read_csv("Test Spam - Sheet1.csv")



# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    password = os.getenv("site_password")
    error = None
    if request.method == 'POST':
        if request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/home")
def home():
    return render_template("index.html")


@app.route('/sendText', methods=['POST'])
def sendText():
    country_code = "+1"
    text_body = str(request.form.get("text_body"))


    print(df)
    for index, row in df.iterrows():
        number = "+1" + str(row['Number'])

        message = client.messages \
                    .create(
                        body=str(text_body),
                        from_= toll_free_num,
                        to=number
                    )

        print(message.sid)


    return "Success"


if __name__ == "__main__":
    app.run()