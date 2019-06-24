'''
Created on Jun 24, 2019

@author: jlepore
'''
from flask import Flask,request,render_template,jsonify
import requirements as script # ignore this error

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/request", methods=["POST"])
def get_data():
    f = request.form['contents']
    lines = f.split("\n")
    parts_list = script.getPartsList(lines)
    
    for item in parts_list:
        print(item, ":", len(parts_list[item]))
    
    return jsonify(parts_list)

if __name__ == '__main__':
    app.run("0.0.0.0", "3000", debug=True)
    
    