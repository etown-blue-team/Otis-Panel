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

    '''Get user specs from form'''
    output = result['output']
    output = int(output)

    '''Separate input data from output data'''
    outdata = data.iloc[:, output - 1:output]
    indata = data.drop(data.columns[output - 1], axis=1)

    '''Testing purposes to ensure data is placed correctly'''
    print(outdata)
    print(indata)

    '''Further separation of daata file'''
    #inTrain, inTest, outTrain, outTest = train_test_split(indata, outdata, test_size=0.3, random_state=101)

    # print(inTrain)
    # print(inTest)
    # print(outTrain)
    # print(outTest)


    inTest = indata.tail(1)
    outTest = outdata.tail(1)

    inTrain = indata[:-1]
    outTrain = outdata[:-1]

        

    '''Train data'''
    neural = Network(inTrain.values, outTrain.values)
    Network.train(neural, 1000)
    outputList = pd.DataFrame(Network.run(neural, inTest))
    print(outputList)

    return render_template("view.html", tables=[inTest.to_html(classes='intext'), outTest.to_html(classes='outTest'),outputList.to_html(classes='outTest')],titles = ['na','IN','OUT','OTIS'])

if __name__ == '__main__':
    app.run(debug=True)





