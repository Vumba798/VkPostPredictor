import sqlite3
from flask_cors import CORS
from model import Predictor

from flask import Flask, request

app = Flask(__name__)
CORS(app)

connection = sqlite3.connect("predictor.db")
cursor = connection.cursor()

model = Predictor("weights", "vocabulary.txt")

@app.route('/api/predict', methods=['GET', 'POST'])
def predict():
    text = request.get_json()['text']
    print(request.get_json())
    result = model.predict(text)

    return {"result": result.tolist()[0]}


@app.put('/post')
def putPost():
    json = request.get_json()
    text = json['text']
    label = json['label']
    cursor.execute("insert into posts (text, label) values(?, ?)", (text, label))
    connection.commit()
    return {"result": "ok"}
