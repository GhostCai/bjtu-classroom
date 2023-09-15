from flask import Flask
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10/minute", "50 per hour"],
    storage_uri="memory://",
)

import json
import time

lookup = {
    '上午1':1,
    '上午2':2,
    '中午':3,
    '下午1':4,
    '下午2':5,
    '晚上1':6,
    '晚上2':7
}
with open("data.json", "r") as f:
    data = json.load(f)

open_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
class Classroom(Resource):
    def get(self, building, week, day, start, end):
        # Read the JSON file
        start = lookup[start]
        end = lookup[end]

        if start > end:
            return ['开始时间不能大于结束时间']  + [''] + ['🚀 caiziqi.com']
        #print(start,end)

        # Filter the data based on the query parameters
        result = []
        vis = []
        cnt = {}
        for item in data:
            if item["building"] == building and item["week"] == week and item["day"] == day and item["time"] >= start and item["time"] <= end and item["status"] == "空闲":
                if item['classroom'] in cnt:
                    cnt[item['classroom']] += 1
                else:
                    cnt[item['classroom']] = 1
                if cnt[item["classroom"]] == end-start+1:
                    vis.append(item['classroom'])
                    result.append(item)

        # Return the filtered data as JSON
        rooms_sorted = sorted(result, key=lambda x: x["classroom"])
        return  [f"{x['classroom']}({x['capacity']})" for x in rooms_sorted] + [''] + [f'Last Updated {open_time}']

api.add_resource(Classroom, "/classroom/<string:building>/<int:week>/<int:day>/<string:start>/<string:end>")

app.run(host='0.0.0.0',port=8888)
