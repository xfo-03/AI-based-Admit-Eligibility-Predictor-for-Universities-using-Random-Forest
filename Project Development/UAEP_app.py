import flask
from flask import request, render_template
from flask_cors import CORS
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "9VKQnZyBF_q8bkmUKuLvO-vN-duJcPi7X8-AX-2J1Rtc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)
@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('home_page.html')


@app.route('/predict_chances', methods=['POST'])
def predictEligibility():
    gre = int(request.form['GRE_Score'])
    toefl = int(request.form['TOEFEL_Score'])
    universityRating = int(request.form['u_rate'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = int(request.form['Research'])
    X = [[gre, toefl, universityRating, sop, lor, cgpa, research]]
    #model = joblib.load('model.pkl')
    #species = model.predict(X)[0]
    #return render_template('predict_chances.html', predict=species)

    payload_scoring = {"input_data": [
        {"field": [['gre', 'toefl', 'universityRating', 'sop', 'lor', 'cgpa', 'research']],
         "values":X}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3d1a9159-8ae8-41b8-8f35-e7cf4b5eeb46/predictions?version=2022-11-18',
        json=payload_scoring,
        headers=header
    ).json()

    predict = response_scoring['predictions'][0]['values'][0][0]

    if predict > 0.5:
        #txt = "You have good scores. All the best!!!"
        return render_template('chance.html', predict=predict)
    else:
        #txt = "You have good scores. All the best!!!"
        return render_template('no_chance.html', predict=predict)

if __name__ == '__main__':
    app.run()