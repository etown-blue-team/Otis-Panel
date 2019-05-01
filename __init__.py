import numpy as np
import pandas as pd
from network import *
from sklearn.model_selection import train_test_split
import DictionaryBuilder as db
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request

# variables
outdata = pd.DataFrame()
indata = pd.DataFrame()

inRunData = pd.DataFrame()
outRunData = pd.DataFrame()

nerual = Network


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('OtisPanel/index.html', title='Home')


if __name__ == "__index__":
    app.run(debug=True)



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    global mdf
    mdf = pd.DataFrame()

    if request.method == 'POST':
        file = request.files['data_file']
        file.save('/var/www/uploads/uploaded_file.txt') + secure_filename(file.filename)

    mdf = pd.read_csv(file)
    for x in list(mdf):
        if mdf[x].dtype is np.dtype('O'):
            b = db.DictionaryBuilder(mdf)
            b.build()
            mdf = b.map()
            break
    else:
        ch = input("Data set already loaded. Overwrite? (y/n) ")
        if ch.lower() == 'y':
            mdf = pd.DataFrame()
            upload_file(file)

def export_data(file=""):
    '''Asks for a file name and writes out the modified dataframe'''
    global mdf
    if mdf.empty:
        print("Empty dataframe. Use import to load a data set")
    else:
        if file == "":
            file = input("File name: ")
        mdf.to_csv(str(file))


def view_data(n=0):
    if mdf.empty:
        print("Empty dataframe. Use import to load a data set")
    else:
        if n == 0:
            print(mdf)
        else:
            print(mdf.head(int(n)))


def list_commands():
    global cmd_list
    print('''
    import [source]      : Imports data from source (URL or File)
    export [destination] : Exports data to a CSV
    clear                : Clears current data
    view [rows]          : View [rows] rows
    train                : Trains network based on imported data
    run  [data]          : Get output from network
    help                 : Show this message
    exit                 : Exit Otis
    ''')


def train(col=-1):
    if mdf.empty:
        print("Empty dataframe. Data is needed to train. Use import to import data")
    else:
        if col == -1:
            col = int(input("Which column is output data "))

        col = int(col)
        outdata = mdf.iloc[:, col - 1:col]
        indata = mdf.drop(mdf.columns[col - 1], axis=1)

        inTrain, inTest, outTrain, outTest = train_test_split(indata, outdata, test_size=0.3, random_state=101)

        # print(inTrain)
        # print(inTest)
        # print(outTrain)
        # print(outTest)

        neural = Network(inTrain.values, outTrain.values)
        Network.train(neural, 1000)
        Network.run(neural, inTest)


def clear():
    # TODO: Clear Network Too
    mdf.drop(mdf.index, inplace=True)
    indata.drop(indata.index, inplace=True)
    outdata.drop(outdata.index, inplace=True)
    print("Dataframe Cleared")



