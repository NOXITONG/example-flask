import requests as requests
from flask import Flask, request
from aes import decrypt, encrypt
import bs4

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
    html = ''
    try:
        url = decrypt(request.args.get("url"))
        html = requests.get(url=f'http://{url}', headers=headers).text.encode().decode('utf-8')
        with open("tmp.html",'w') as f:
            f.write(html)
    # try:
        soup = bs4.BeautifulSoup(html, "html.parser")
        href_set = {item.get('href') for item in soup.find_all(href=True)}
        replace_dict = {}
        # print(href_set)
        for item in href_set:
            try:
                if item.startswith('https://'):
                    replace_dict[item] = f'/url/?url={encrypt(item)}'
                elif item.startswith('http://'):
                    replace_dict[item] = f'/url/?url={encrypt(item)}'
                # elif item.startswith('//'):
                #     replace_dict[item] = f'/url/?url={encrypt(f"http:{item}")}'
                # elif item.startswith('/'):
                #     replace_dict[item] = f'/url/?url={encrypt(f"http://{url}{item}")}'
            except:
                pass
        # href_set = {"" if item in replace_dict else item for item in href_set}
        # print(href_set)
        for key in replace_dict:
            html = html.replace(key, replace_dict[key])
    except:
        pass
    return html


if __name__ == "__main__":
    app.run()
