import  re
import  requests
import time
import os
import random

saveUrl = 'D://img/'
url = "http://www.waxjj.cn"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

def getFile():
    # 获取分类地址和分类名字
    url_text = requests.get(url, headers=headers)
    tpName = re.findall(r'<a href.*>(.*)</a>', url_text.text)
    wallpaper_classification = re.findall(r'a href="([a-zA-z]+://[^\s]*)"', url_text.text)
    tpName = tpName[2:-1]
    wallpaper_classification_url = wallpaper_classification[1:7]

    return tpName,wallpaper_classification_url
# ['汉服', '制服', '写真', '清新', 'COS', '美腿']
# ['http://www.waxjj.cn/category/%e6%b1%89%e6%9c%8d', 'http://www.waxjj.cn/category/%e5%88%b6%e6%9c%8d',
# 'http://www.waxjj.cn/category/%e5%86%99%e7%9c%9f', 'http://www.waxjj.cn/category/%e6%b8%85%e6%96%b0',
# 'http://www.waxjj.cn/category/cos', 'http://www.waxjj.cn/category/%e7%be%8e%e8%85%bf']

def getUrl(wallpaper_classification_url):
    # 'http://www.waxjj.cn/category/%e6%b1%89%e6%9c%8d'
    # 获取壁纸分类下面的地址
    url_text = requests.get(wallpaper_classification_url,headers = headers)
    all_url = re.findall(r'a href="([a-zA-z]+://[^\s]*)"', url_text.text)
    next_url = re.findall(r'a class="next page-numbers" href="([a-zA-z]+://[^\s]*)"', url_text.text)
    all_url = all_url[8: -1]
    # all_url
    #['http://www.waxjj.cn/6206.html', 'http://www.waxjj.cn/6115.html', 'http://www.waxjj.cn/5927.html',
    # 'http://www.waxjj.cn/5905.html', 'http://www.waxjj.cn/5497.html', 'http://www.waxjj.cn/5167.html',
    # 'http://www.waxjj.cn/5156.html', 'http://www.waxjj.cn/4832.html', 'http://www.waxjj.cn/4432.html',
    # 'http://www.waxjj.cn/2419.html', 'http://www.waxjj.cn/2042.html', 'http://www.waxjj.cn/1521.html',
    # 'http://www.waxjj.cn/598.html', 'http://www.waxjj.cn/606.html', 'http://www.waxjj.cn/529.html']

    # next_url
    #  ['http://www.waxjj.cn/category/%E6%B1%89%E6%9C%8D/page/2']

    return all_url,next_url

def saveImg(all_url):
    # saveImg(['http://www.waxjj.cn/598.html'])
    for url in all_url:
        print(url)
        url_text = requests.get(url, headers=headers)
        # 获取到该分类图片的名字 并处理
        tp_name = re.findall(r'<h1.*>(.*)</h1>', url_text.text)
        tp_name = re.sub('\\[.*?\\]', '', tp_name[0])
        localPath = os.getcwd() + '\\' + tp_name + '\\'
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        tp_url = re.findall(r'<img src="(.*?)" alt=""', url_text.text) # 获取到所有图片的路径地址
        for i in range(len(tp_url)):
            print(tp_url[i])
            if not tp_url[i].startswith('http'):
                tp_url[i] ='http:' + tp_url[i]
            if tp_url[i].startswith('http://www.52xjj.icu'):
                tp_url[i] = tp_url[i].replace('http://www.52xjj.icu','http://cdn.waxjj.cn')
            if tp_url[i].startswith('http://cdn.52xjj.icu'):
                tp_url[i] = tp_url[i].replace('http://cdn.52xjj.icu', 'http://cdn.waxjj.cn')
            save_url = ''
            save_url = localPath  + f'{i+1}.jpg'
            if os.path.exists(save_url):
                number = random.randint(5, 7)
                time.sleep(number)
                print('文件存在下载下一张图片')
                continue
            response = requests.get(tp_url[i], headers=headers)
            with open(save_url,'wb') as f:
                f.write(response.content)
                number = random.randint(6, 10)
                time.sleep(number)
                print("=====================success====================")
                print("等待" + str(number) + '秒;' + '下载下一张图片')
def qtpy_url(url):
    all_url, next_url = getUrl(url)
    saveImg(all_url)
    if next_url:
        # 如果有下一页就递归调用
        qtpy_url(next_url[0])
    else:
        return

if __name__ == '__main__':
    # ['汉服', '制服', '写真', '清新', 'COS', '美腿']
    # saveImg(['http://www.waxjj.cn/4832.html','http://www.waxjj.cn/6206.html'])
    tpName, wallpaper_classification_url = getFile()
    for i in range(len(wallpaper_classification_url)):
        localPath = saveUrl + '\\' + tpName[i+3]
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        os.chdir(localPath)
        qtpy_url(wallpaper_classification_url[i+3])
    # all_url,next_url = getUrl(wallpaper_classification_url[0])