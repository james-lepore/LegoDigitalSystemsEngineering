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
def getData():
    f = request.form['contents']
    lines = f.split("\n")
    parts_list = script.getPartsList(lines)
    if type(parts_list) is not dict:
        return jsonify(["False", parts_list])
    
    results = [script.seatOrientation(parts_list), \
               script.seatObstruction(parts_list), \
               script.consoleOrientation(parts_list), \
               script.numWheels(parts_list), \
               script.wheelOrientation(parts_list), \
               script.headlightOrientation(parts_list), \
               script.taillightOrientation(parts_list), \
               script.licensePlateOrientation(parts_list), \
               script.numChassis(parts_list), \
               script.getChassisType(parts_list)]
    return jsonify(results)


@app.route("/metrics", methods=["POST"])
def getMetrics():
    f = request.form['contents']
    lines = f.split("\n")
    parts_list = script.getPartsList(lines)
    results = [script.getSeatingScore(parts_list), \
               script.getVentilationScore(parts_list), \
               script.getStabilityScore(parts_list), \
               script.getHeadlightScore(parts_list), \
               script.getTaillightScore(parts_list), \
               script.getCargoSpaceScore(parts_list), \
               script.getAerodynamicsScore(parts_list), \
               script.getCost(parts_list), \
               script.getMarketPrice(parts_list), \
               script.getProfit(parts_list)]
    return jsonify(results)


if __name__ == '__main__':
    app.run("0.0.0.0", "3000", debug=True)
    
