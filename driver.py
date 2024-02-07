from flask import Flask, render_template, request, redirect, url_for
import requests
import textflowsms as tf
import pandas as pd

app = Flask(__name__, static_folder='templates/assets')
tf.useKey("6y8bb44d0QfyeTw77RyFFAsBrom900M8WxYwgSCYfwCezqgXhlO9RIRSDJmztK5W")
number_table = pd.read_csv("number-sheet.csv")


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'monique':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/sendText', methods = ['POST'])
def sendText():
    text_body = str(request.form.get("body"))

    for index, row in number_table.iterrows():
        print(row['Name'], row['Number'])
        number = "+1" + str(row["Number"])
        print(number)
        result = tf.sendSMS(number,text_body)
        if(result.ok):
            print(result.data)
        else:
            print(result.message)


    return "success"

# @app.route('/codeVerifcation', methods = ['POST'])
# def codeVerification():
#     country_code = "+1"
#     number = request.form.get("phone_number")

#     # The number that will receive the SMS. Test accounts are limited to verified numbers.
#     # The number must be in E.164 Format, e.g. Netherlands 0639111222 -> +31639111222
#     toNumber = country_code + str(number)


#     #The verification code
#     code = request.form.get("code")
#     code = str(code)

#     # The key from one of your Verification Apps, found here https://dashboard.sinch.com/verification/apps
#     applicationKey = "dbb2e813-9522-4d05-b20d-8351515678fc"

#     # The secret from the Verification App that uses the key above, found here https://dashboard.sinch.com/verification/apps
#     applicationSecret = "dD2b/usNQ06WhvT73ZYCKA=="



#     sinchVerificationUrl = "https://verification.api.sinch.com/verification/v1/verifications/number/" + toNumber

#     payload = {
#         "method": "sms",
#         "sms": {
#             "code": code
#         }
#     }

#     headers = {"Content-Type": "application/json"}

#     response = requests.put(sinchVerificationUrl, json=payload, headers=headers, auth=(applicationKey, applicationSecret))

#     data = response.json()
#     print(data)
#     return "success"

# @app.route('/phoneVerification', methods=['POST'])
# def phoneVerification():
#     country_code = "+1"
#     number = request.form.get("phone_number")

#     print(number)


#     # The number that will receive the SMS. Test accounts are limited to verified numbers.
#     # The number must be in E.164 Format, e.g. Netherlands 0639111222 -> +31639111222
#     toNumber = (country_code + str(number))

#     # The key from one of your Verification Apps, found here https://dashboard.sinch.com/verification/apps
#     applicationKey = "dbb2e813-9522-4d05-b20d-8351515678fc"

#     # The secret from the Verification App that uses the key above, found here https://dashboard.sinch.com/verification/apps
#     applicationSecret = "dD2b/usNQ06WhvT73ZYCKA=="

    
#     sinchVerificationUrl = "https://verification.api.sinch.com/verification/v1/verifications"

#     payload = {
#         "identity": {
#             "type": "number",
#             "endpoint": toNumber
#         },
#         "method": "sms"
#     }

#     headers = {"Content-Type": "application/json"}

#     response = requests.post(sinchVerificationUrl, json=payload, headers=headers, auth=(applicationKey, applicationSecret))

#     data = response.json()
#     print(data)


#     return "Success"


if __name__ == "__main__":
    app.run()