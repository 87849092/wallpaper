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
SAVE_PATH = "D://img//小姐姐网//"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

# url = "http://www.waxjj.cn"
url = "http://www.waxjj.cn/6336.html"
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

def get_img_url(url):
    res = requests.get(url, headers)
    tp_name = re.findall(r'<h1.*>(.*)</h1>', res.text)
    tp_name = re.sub('\\[.*?\\]', '', tp_name[0])

    tp_url = re.findall(r'<img src="(.*?)" alt=""', res.text)  # 获取到所有图片的路径地址
    return tp_name,tp_url

def save_img(url):
    if not url.startswith('http'):
        url = 'http:' + tp_url[i]
    if url.startswith('http://www.52xjj.icu'):
        url = url.replace('http://www.52xjj.icu', 'http://cdn.waxjj.cn')
    if url.startswith('http://cdn.52xjj.icu'):
        url = url.replace('http://cdn.52xjj.icu', 'http://cdn.waxjj.cn')
    save_url = ''
    localPath = os.getcwd()
    tp_name = url.split("/")[-1].split("-")[0]
    save_url = localPath +"//" +  f'{tp_name}.jpg'
    response = requests.get(url, headers=headers)
    with open(save_url, 'wb') as f:
        f.write(response.content)
        print("==========下载===" + tp_name + " ========成功======")

if __name__ == '__main__':
    # html = download_page()
    # contents = parser_html(html)[8:-1]
    tp_name,contents = get_img_url(url)
    localPath = SAVE_PATH + tp_name + '//'
    if not os.path.exists(localPath):
        os.makedirs(localPath)
    os.chdir(localPath)
    for content in contents:
        p = multiprocessing.Process(target=save_img,args=(content,))
        p.start()
        p.join()
       # save_img(content)