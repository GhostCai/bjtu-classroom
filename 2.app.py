from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import json


class Classroom(Resource):
    def get(self, building, week, day, start, end):
        with open("data.json", "r") as f:
            data = json.load(f)

        # Filter the data based on the query parameters
        result = []
        vis = []
        cnt = {}
        for item in data:
            if (
                item["building"] == building
                and item["week"] == week
                and item["day"] == day
                and item["time"] >= start
                and item["time"] <= end
                and item["status"] == "空闲"
            ):
                if item["classroom"] in cnt:
                    cnt[item["classroom"]] += 1
                else:
                    cnt[item["classroom"]] = 1
                if cnt[item["classroom"]] == end - start + 1:
                    vis.append(item["classroom"])
                    result.append(item)

        # Return the filtered data as JSON
        rooms_sorted = sorted(result, key=lambda x: x["classroom"])
        return [f"{x['classroom']}({x['capacity']})" for x in rooms_sorted]


api.add_resource(
    Classroom, "/classroom/<string:building>/<int:week>/<int:day>/<int:start>/<int:end>"
)

app.run(host="0.0.0.0", port=8888)
