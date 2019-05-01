from flask import Flask, render_template,request, redirect, url_for, make_response
import csv
import io
from werkzeug import *
import numpy as np

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/data',methods=['POST'])
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
    app.run(debug = True)