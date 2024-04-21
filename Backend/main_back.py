from flask import Flask
from Backend.API.dfender import Dfender


app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predict():
    dfender = Dfender()





