'''
Created on Jun 24, 2019

@author: jlepore
'''
from flask import Flask,request,render_template,jsonify


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/request", methods=["POST"])
def request():
    return "2"

if __name__ == '__main__':
    app.run("0.0.0.0", "3000", debug=True)
    
    