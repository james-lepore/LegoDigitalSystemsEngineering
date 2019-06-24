'''
Created on Jun 24, 2019

@author: jlepore
'''
from flask import Flask,request,render_template,jsonify


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/request", methods=["POST"])
def get_data():
    f = request.form['contents']
    print(f.split("\n"))
    return f

if __name__ == '__main__':
    app.run("0.0.0.0", "3000", debug=True)
    
    