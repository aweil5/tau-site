from flask import Flask, render_template, request, redirect, url_for
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
df = pd.read_csv("FULL_NUMBER_SHEET - Sheet1.csv")
df.fillna(0)



# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    password = os.getenv("site_password")
    admin_pass = os.getenv("admin_pass")
    error = None
    if request.method == 'POST':
        if request.form['password'] == admin_pass:
            return redirect(url_for('adminPanel'))
        if request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/adminPanel")
def adminPanel():
    return render_template('admin_panel.html')
@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/sendTextPc', methods = ['POST'])
def sendTextPc():
    text_body = request.form.get("text_body")
    pc = str(request.form.get("pc"))

    print(text_body)
    for index, row in df.iterrows():
        
        number = "+1" + str(int(row['Number']))
        if(row['PC'] == pc):
            if(number != "+1"):

                message = client.messages \
                            .create(
                                body=str(text_body),
                                from_= toll_free_num,
                                to=number
                            )

                print(message.sid)
    return "success"



@app.route('/sendTextAll', methods=['POST'])
def sendTextAll():
    text_body = request.form.get("text_body")

    print(text_body)
    for index, row in df.iterrows():
        
        number = "+1" + str(int(row['Number']))
        if(number != "+1"):

            message = client.messages \
                        .create(
                            body=str(text_body),
                            from_= toll_free_num,
                            to=number
                        )
            
# USE THIS TO GET SID INFO AND ERROR HANDLE IF PERSON UNSUBSCRIBED
            # call = client.calls.get("CA42ed11f93dc08b952027ffbc406d0868")
            # print(call.to)


            print(message.sid)
    return "Success"


#     return "Success"


if __name__ == "__main__":
    app.run()