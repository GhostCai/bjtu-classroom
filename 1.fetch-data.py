import requests
import json
import time
import random
import os
from lxml import etree

csrftoken = os.environ["csrftoken"]
sessionid = os.environ["sessionid"]


def get_data(zxjxjhh, zc, jxlh, jash, page):
    base_url = "https://aa.bjtu.edu.cn/classroom/timeholdresult/room_view/"
    params = {
        "zxjxjhh": zxjxjhh,
        "zc": zc,
        "jxlh": jxlh,
        "jash": jash,
        "submit": "+%E6%9F%A5+%E8%AF%A2+",
        "has_advance_query": "",
        "page": page,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191215.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
    }
    cookies = {
        "csrftoken": csrftoken,
        "sessionid": sessionid,
    }
    r = requests.get(base_url, params=params, headers=headers, cookies=cookies)
    return r


color2status_table = {
    "#e46868": "有课",
    "#d8cc56": "社团",
    "#77bf6d": "实验",
    "#394ed6": "考试",
}


def color2status(style: str):
    color = style.split(":")[1].strip()
    if color in color2status_table:
        return color2status_table[color]
    else:
        return "空闲"


desired_buildings = [
    {"name": "思源", "id": "1"},
    {"name": "思西", "id": "2"},
    {"name": "思东", "id": "3"},
    {"name": "九教", "id": "4"},
    {"name": "逸夫", "id": "11"},
]


if __name__ == "__main__":
    results = []
    for building in desired_buildings:
        building_name = building["name"]
        building_id = building["id"]
        for week in range(26):  # 周次
            for page in range(1, 1000):
                req = get_data("2023-2024-1-2", week + 1, building_id, "", page)
                html = etree.HTML(req.text)
                succ = False
                print(f"fetching {building_name} week {week+1} page {page}")
                for classroom in range(20):
                    for day in range(7):
                        for peroid in range(7):
                            try:
                                classroom_name_path = f"/html/body/div[2]/div[2]/div/div[2]/table/tr[{classroom+3}]/td[1]/text()"
                                classroom_name = html.xpath(classroom_name_path)[
                                    0
                                ].strip()
                            except:
                                break

                            classroom_capacity_path = f"/html/body/div[2]/div[2]/div/div[2]/table/tr[{classroom+3}]/td[1]/span/text()"
                            classroom_capacity = html.xpath(classroom_capacity_path)
                            # remove left and right brackets
                            classroom_capacity = classroom_capacity[0][1:-1]

                            # /html/body/div[2]/div[2]/div/div[2]/table/tr[3]/td[2]
                            # /html/body/div[2]/div[2]/div/div[2]/table/tr[3]/td[2]/@style
                            status_path = f"/html/body/div[2]/div[2]/div/div[2]/table/tr[3]/td[{day*7+peroid+2}]/@style"
                            color = html.xpath(status_path)[0]
                            status = color2status(color)

                            item = {
                                "building": building_name,
                                "classroom": classroom_name,
                                "capacity": classroom_capacity,
                                "week": week + 1,
                                "day": day,
                                "time": peroid,
                                "status": status,
                            }
                            if item not in results:
                                results.append(item)
                                succ = True
                            # sleep for a while
                if succ == False:
                    break

            time.sleep(random.randint(0, 100) / 1000)

    # save to json file
    with open("data.json", "w") as f:
        json.dump(results, f)
