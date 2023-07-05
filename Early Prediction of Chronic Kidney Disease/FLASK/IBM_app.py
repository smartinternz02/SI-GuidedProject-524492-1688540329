# importing the necessary dependencies
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import json
import requests

API_KEY="Y-gefoTlf5vIgow-kK6y6gGonehuZjuYBNGq7smfO_cN"
token_response = requests.post('https://iam.ng.bluemix.net/identity/token',data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)



app = Flask(__name__) # initializing a flask app


@app.route('/')# route to display the home page
def home():
    return render_template('home.html') #rendering the home page
@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('indexnew.html')
@app.route('/Home',methods=['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])# route to show the predictions in a web UI
def predict():
    
    #reading the inputs given by the user
    input_features = [float(x) for x in request.form.values()]
    features_value = np.array(input_features).tolist()
    
    
    payload_scoring = {
        "input_data": [
            {
                "field": [
                    [
                        "pus_cell",
                        "blood glucose random",
                        "blood_urea",
                        "pedal_edema",
                        "anemia",
                        "diabetesmellitus",
                        "hypertension",
                        "hemoglobin",
                        "specific_gravity",
                        "packed_cell_volume",
                        "red_blood_cell_count",
                        "appetite"
                    ]
                ],
                "values": [
                    features_value
                ]
            }
        ]
    }
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8a50bec4-e346-45c3-b0bb-ff087162c131/predictions?version=2021-05-01', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
   

    pred = predictions['predictions'][0]['values'][0][0]

    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('result.html', prediction_text=pred)

if __name__ == '__main__':
    # running the app
    app.run(debug=True)
