"""
爬取4k动漫图片

"""
import random
import requests
import time
import os
import re

from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

# 代码仅供参考

headers = {
    "Cookie": "__cfduid=d721a11a68c11b42fd826a3f7911420ef1583308775; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1583308776,1583372170,1583461537; zkhanecookieclassrecord=%2C54%2C55%2C53%2C66%2C; PHPSESSID=m9ne0k3tlqc3splbsm166spkt0; zkhanmlusername=qq859967158330; zkhanmluserid=2784448; zkhanmlgroupid=1; zkhanmlrnd=rbkdHsUPlnYCkf3D3IOL; zkhanmlauth=f17d3bfc99bb8576da87e3e991375ecc; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1583473648"
    ,
    "User-Agent": ua.random
}
root = 'D://img//'
if not os.path.exists(root):
    os.mkdir(root)

# range此参数可以自己更改，第几页到第几页
for page in range(0,2):
    os.chdir(root)
    # 创建文件夹
    if not os.path.exists(f"4k动漫的第{page + 1}页"):
        os.mkdir(f"4k动漫的第{page + 1}页")
    # 改变当前文件目录
    os.chdir(f"4k动漫的第{page + 1}页")
    if page+1 == 1:
        url = f"http://pic.netbian.com/4kdongman/index.html"
    else:
        url = f"http://pic.netbian.com/4kdongman/index_{page + 1}.html"
    response = requests.get(url,headers=headers,verify=False)
    response.encoding = 'gbk'

    if response.status_code == 200 :
        result = """<a href="(.*?)" target="_blank"><img src=".*?" alt=".*?" /><b>.*?</b></a>"""
        contents = re.findall(result,response.text)
        # 去遍历所有的图片
        for i in contents:
            path = i
            print(f"{path}正在进入html......")
            response2 = requests.get("http://pic.netbian.com" + path, headers=headers, verify=False)
            response2.encoding = "gbk"
            num = random.randint(5,10)
            time.sleep(num)
            result2 = """<a href="" id="img"><img src="(.*?)" data-pic=".*?" alt="(.*?)" title=".*?"></a>"""
            contents2 = re.findall(result2, response2.text)
            print(contents2)
            # 去遍历所有的图片
            for content2 in contents2:
                path2 = content2[0]
                name = content2[1]
                response3 = requests.get("http://pic.netbian.com"+path2, headers=headers,verify=False)
                #保存到本地
                with open(f"{name}.jpg", "wb") as f:
                    f.write(response3.content)
                number = random.randint(5,10)
                print(f"{name} : {path2} 保存成功,等待"+str(number)+"秒后继续爬取")
                time.sleep(number)
    print(f"第{page + 1}页抓取成功，,等待2秒后继续爬取")
    time.sleep(2)
print("爬取结束")