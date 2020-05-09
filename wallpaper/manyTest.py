import os
import sys
import io
import urllib
import requests
import re
import chardet
import time
import multiprocessing

#设置系统输出流的编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# 图片保存路径
SAVE_PATH = "D://img/小姐姐网/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

url = "http://www.waxjj.cn"

def download_page():
    try:
        res = requests.get(url,headers)
        if res.status_code == 200:
            res.encoding = chardet.detect(res.content).get('encoding')
            return res.text
    except requests.HTTPError as e:
        return None
def parser_html(html):
    if not html:
        return
    content  = re.findall(r'a href="([a-zA-z]+://[^\s]*)"',html)
    print(content)
    return content

def get_ImgUrl(url):
    if not url:
        return
    res = requests.get(url, headers)
    contents = re.findall(r'<img src="(.*?)" alt=""', res.text)  # 获取到所有图片的路径地址
    print(contents)
    return contents
def save_img(all_Img):
    return

if __name__ == '__main__':
    html = download_page()
    contents = parser_html(html)[8:-1]
    for content in contents:
        p = multiprocessing.Process(target = get_ImgUrl,args = (content,))
        p.start()
        p.join()
