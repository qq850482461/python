import queue
import threading
import time

q = queue.Queue()#创建一个队列对象
lock = threading.Lock()#创建一个线程锁对象

numlist = [] #创建一个列表。。
for i in range(100):
    numlist.append(i)

threads = []#线程列表

#装载queue队列
for i in numlist:#填充q顺序队列
    q.put(i)#放入queue队列

def work():
   while True: #循环执行
       lock.acquire() #添加一个锁
       if not q.empty():#q队列不为空执行
           data = q.get() #从q队列拿出一个数据并且移除
           lock.release() #释放锁定
           print(data) #工作模块打印Q队列拿出来的每一个东西
       else:
           lock.release() #释放锁定
           break #跳出循环
           print("队列为空执行这个")
       #time.sleep(1)


#创建线程列表
for i in range(8):
    i = threading.Thread(target=work)
    i.setDaemon(True)
    i.start()
    threads.append(i)



#执行关闭
for i in threads:
    i.join()


