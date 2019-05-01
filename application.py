import numpy as np
import pandas as pd
import csv
import io
from sklearn.model_selection import train_test_split
from werkzeug import *
from flask import Flask, render_template, request, redirect, url_for, make_response

''' Import from Otis repo '''
import Shell as shell
import DictionaryBuilder as db
from Network import *


nerual = Network


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html', title='Home')

@app.route('/data', methods=['POST'])
def getinfo():

    data = []
    result = request.form

    f = request.files['data_file']
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    readdata = csv.reader(stream)

    for row in readdata:
        data.append(row)

    data = np.array(data)
    print(data)

    return render_template("view.html", data=data, result=result)

    if __name__ == '__main__':
        app.run(debug=True)



