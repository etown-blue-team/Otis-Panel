'import Shell as shell'
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('OtisPanel/index.html', title='Home')


if __name__ == "__index__":
    app.run(debug=True)
