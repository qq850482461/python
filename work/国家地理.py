import urllib.request
import os
import bs4
import re
import threading
import queue

class Photo():
    def __init__(self,url,page=10):
        self.url = url
        self.page = page

    def get_html(self,url):
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        return html

    def latest_jpg(self):
        html = self.get_html(self.url)
        soup = bs4.BeautifulSoup(html,"html.parser")
        jpg_tag = soup.find_all("dl",class_="show-list-dl aside-box")
        url_list = []
        for tag in jpg_tag:
            url = tag.find("a").get("href")
            url = "http://www.nationalgeographic.com.cn" + url
            url_list.append(url)
        return url_list[:self.page]

    def get_jpg(slef,url):
        html = slef.get_html(url)
        reg = r'src="(.+?\.jpg)"'
        jpg = re.findall(reg,html)[-1]
        return jpg


    def floadr(self):
        if os.path.isdir("国家地理"):
            print("已发现目录移动到目录中")
            os.chdir("国家地理")
        else:
            os.mkdir("国家地理")
            os.chdir("国家地理")

    def download(self):
        self.floadr()
        url = self.latest_jpg()
        print(url)
        for i in url:
            jpg = self.get_jpg(i)
            name = jpg.split("/")[-1]
            try:
                print("正在下载",name)
                urllib.request.urlretrieve(jpg,name)
            except:
                print("出错跳过")




a = Photo("http://www.nationalgeographic.com.cn/photography/photo_of_the_day/")
a.download()



