from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/dt_data_entry', methods = ['POST'])
def postInfo():
    client = MongoClient()
    db = client['doutuiDb']
    jsonInfo = request.json
    doutuiCol = db.doutuiCol
    doutuiCol.insert_one({"timestamps":jsonInfo['timestamps'],"count":jsonInfo['count']})
    return "Successed"

@app.route('/get_dt_data', methods=['GET'])
def getInfo():
    client = MongoClient()
    db = client['doutuiDb']
    limits = int(request.args.get('timeLimits'))
    interval = int(request.args.get('timeInterval'))
    startTime = limits - interval
    endTime = limits
    doutuiCol = db.doutuiCol
    cnt = 0
    for item in doutuiCol.find({'timestamps':{'$gt':startTime, '$lte':endTime}}):
        cnt = cnt + item['count']
    return str(cnt)


if __name__ == '__main__':
    app.run(debug=True)
