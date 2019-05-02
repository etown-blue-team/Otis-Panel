import numpy as np
import pandas as pd
import csv
import io
from sklearn.model_selection import train_test_split
from werkzeug import *
from flask import Flask, render_template, request, redirect, url_for, make_response

''' Import from Otis repo '''
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
    data = pd.read_csv(stream)


    trainstart = result['trainstart']
    trainend = result['trainend']
    teststart = result['teststart']
    testend = result['testend']
    output = result['output']
    output = int(output)


    outdata = data.iloc[:, output - 1:output]
    indata = data.drop(data.columns[output - 1], axis=1)

    print(outdata)
    print(indata)

    inTrain, inTest, outTrain, outTest = train_test_split(indata, outdata, test_size=0.3, random_state=101)

    # print(inTrain)
    # print(inTest)
    # print(outTrain)
    # print(outTest)

    neural = Network(inTrain.values, outTrain.values)
    Network.train(neural, 1000)
    outputList = Network.run(neural, inTest)
    print(outputList)

    return render_template("view.html", outputList=outputList)










if __name__ == '__main__':
    app.run(debug=True)





