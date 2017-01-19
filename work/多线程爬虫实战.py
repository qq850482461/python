import time
import queue
import threading
import urllib.request
import os
import re
import urllib.error
import sys



class App():
    def __init__(self,url,page=0):
        self.url = url
        self.page = page
        self.q = queue.Queue()#实例化queue
        self.lock = threading.Lock()#创建一个锁

    #构建一个url打开的方式
    def gethtl(self,url):
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        return html

    #解析页面上的图片并且保存成为一个列表()
    def jpglist(self,url):
        html = self.gethtl(url)
        re_jpg = r'src="(.+?\.jpg)"'
        #re_gif = r'src="(.+?\.gif)"'
        jpg = re.findall(re_jpg,html)
        #gif = re.findall(re_gif,html)
        jpg_list = jpg #+gif
        new_list = []
        for i in jpg_list:
            a = i.find("http:")
            if a == -1:
                i = "http://"+i
                new_list.append(i)
            else:
                new_list.append(i)

        return (new_list)

    #创建一个工作目录然后移动到该目录下载图片
    def floadr(self,name):
        name = str(name)
        if os.path.isdir(name):
            print("已发现目录移动到目录中")
            os.chdir(name)
        else:
            os.mkdir(name)
            os.chdir(name)

    #显示下载速度的回调函数
    def report(self,count, blockSize, totalSize):
        percent = int(count * blockSize * 100 / totalSize)
        sys.stdout.write("\r%d%%" % percent + ' complete')
        sys.stdout.flush()


    #工作内容
    def work(self,url):
        url = url
        jpg_list = self.jpglist(url)


        while True:
            self.lock.acquire()
            if not self.q.empty():
                data = self.q.get()
                self.lock.release()
                name = data.split("/")[-1]
                try:
                    print("正在下载",name)
                    #print(data)    '''
                    #time.sleep(1)
                    urllib.request.urlretrieve(url=data,filename=name,reporthook=self.report)
                except Exception as e:
                   print("出错了",e)
            else:
                self.lock.release()
                break

    #多线程下载图片
    def start(self,url):
        self.floadr("多线程爬虫")
        for i in self.jpglist(url):  # 装载Q队列
            self.q.put(i)
        threads = []
        for i in range(1):
            i = threading.Thread(target=self.work,args=(url,))
            i.setDaemon(True)
            i.start()
            threads.append(i)
        for i in threads:
            i.join()



if __name__  == "__main__":
    app = App("http://www.nationalgeographic.com.cn/")
    a = app.jpglist("http://www.nationalgeographic.com.cn/")
    app.start("http://www.nationalgeographic.com.cn/")