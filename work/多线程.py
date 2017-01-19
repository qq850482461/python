import threading
import time
import urllib.request

num = []
for i in range(20):
    num.append(i)


def work(name,num):
    num = num
    loacl_time = time.asctime(time.localtime(time.time()))
    for i in num:
        quenelock.acquire()
        print(name,i,loacl_time)
        quenelock.release()
    time.sleep(1)
    return

threadLock = threading.Lock()
threads = []

quenelock = threading.Lock()
t1 = threading.Thread(target=work,args=("t1",num))
t2 = threading.Thread(target=work,args=("t2",num,))
#t1.setDaemon(True)
t1.start()
#t2.setDaemon(True)
t2.start()

threads.append(t1)
threads.append(t2)

for t in threads:
    t.join()

print("\n当前线程为 {:d} ".format(threading.activeCount()-1))

