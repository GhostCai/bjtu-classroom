# BJTU空教室查询的后端

## Quick Start

登录mis系统，把自己的cookie拷出来，放到环境变量里
```
export csrftoken=你的csrftoken
export sessionid=你的csrftoken
```

然后爬教室数据
```
python 1.fetch-data.py
```

得到`data.json`后，运行后端
```
python 2.app.py
```
