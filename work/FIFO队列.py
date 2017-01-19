import queue
import threading
import time

exitFlag = 0 #代表false

class myThread (threading.Thread):#重写thread方法
    def __init__(self,name,q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
    def run(self):#重写run方法把执行函数写到run里面由name q传入执行函数
        print ("开启线程：" + self.name)
        process_data(self.name, self.q)
        print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag: #结果为真
        queueLock.acquire()#取得锁
        if not workQueue.empty():#queue队列不是空的
            data = q.get()#从队列中移除并返回一个数据
            queueLock.release()#释放锁
            print ("%s 在干活 %s" % (threadName, data))
        else:#queue队列是空的
            queueLock.release()#释放锁
        time.sleep(1)

threadList = ["Thread-0", "Thread-1", "Thread-2","Thread-3"]
nameList = []
for i in range(100):
    nameList.append(i)
queueLock = threading.Lock() #线程锁
workQueue = queue.Queue()#队列数量
threads = []


# 创建新线程
for tName in threadList:
    thread = myThread(tName, workQueue)
    thread.start()
    threads.append(thread)


# 填充队列
queueLock.acquire()#取得一个锁
for word in nameList:#通过for循环把list放到work里面
    workQueue.put(word)#放入队列
queueLock.release()#释放一个锁

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1 #代表ture

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")