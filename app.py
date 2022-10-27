import requests as requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'URL'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "http://www.sdyu.edu.cn/index.htm",
}


@app.route('/url/')
def demo():
    url = request.args.get("url")
    ret = requests.get(url=f'http://{url}', headers=headers).text.encode().decode('utf-8')
    return ret


if __name__ == "__main__":
    app.run()
