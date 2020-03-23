import api.GressTrade as gt
from multiprocessing import Process,Queue
import multiprocessing
import os
import pprint
import time



def recvQuote(q,api):
    for i in range(2000):
        api.getQuote2()
        q.put(api.quote.mautd.last)
        #q.put(i)
        print('进程1执行%d'%(i))
        #print(q.qsize())

def printQuote(q,api):
    for i in range(2000):
        price=q.get()
        print('进程2执行--%f'%(price))
        

if __name__=='__main__':
    api=gt.API()
    islog,logMasg=api.login('1021805322','615919')
    print(logMasg)

    q=Queue(1)
    p1 = Process(target=recvQuote, args=(q,api,))
    p2 = Process(target=printQuote, args=(q,api,))
    p2.daemon=True
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    api.Close()
    


