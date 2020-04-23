import requests
import os
import time
import random
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

url = "http://lcoc.top/bizhi/api.php?"
header = {
    "Cookie": "__jsluid_h=646a80687aa0eb4fa855f4f5606c6eda; pgv_pvi=495470592; UM_distinctid=170a48ca65a306-0b26b50ab0838f-5040231b-13c680-170a48ca65b31a; pgv_si=s7351662592; CNZZDATA1264542189=61452249-1583307463-%7C1583740575"
    ,
    "User-Agent": ua.random
}
# 自定义下载多少页的数据
def getManyPages(pages):
    params = []
    for i in range(1, pages):
        params.append({
            'cid': '360new',
            'start': (i - 1) * 30,
            'count': 30
        })
    urls = []
    for i in params:
        urls.append(requests.get(url,params=i).json().get('data'))
    return urls

def getImg(urls,localPath):
    for lists in urls:
        for i in lists:
            down_url = i.get('img_1600_900')
            down_name = i.get('id')
            if down_url != None:
                response = requests.get(down_url, headers=header, verify=False)
                localName = localPath + f"{down_name}.jpg"
                if os.path.isfile(localName): # 判断是否有这个名字的文件 如果有就改变名字
                    if localName.find("_") != -1:
                        num = localName.split('_')[1].split('.')[0] + 1
                    else:
                        num = 1
                    localName = localPath + f"{down_name}._" +  f"{num}.jpg"
                with open(localName, "wb") as f: # 下载到指定位置
                    f.write(response.content)
                number = random.randint(2, 5)
                print(f"{localName} : {down_url} 保存成功,等待" + str(number) + "秒后继续爬取")
                time.sleep(number) # 为了不给服务器造成压力，所以休眠几秒
        print(f"等待2秒后继续爬取")
        time.sleep(2)
    print("==========END==================")

if __name__ == '__main__':
    localPath = "D://img/lcoc/"
    if not os.path.exists(localPath):  # 新建文件夹
        os.mkdir(localPath)
    getImg(getManyPages(10),localPath)
