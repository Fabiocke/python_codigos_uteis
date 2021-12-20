from multiprocess import Process
from multiprocess import Queue as PQueue

from threading import Thread
from queue import Queue as TQueue


class Paralelism:
    def __init__(self, paralelism, queue):
        self.queue=queue
        self.paralelism=paralelism

    def run_fn(self, func, queue):
        r=func()
        queue.put(r)
        
    def get_result(self, queue):
        l=[]
        while queue.qsize():
            l.append(queue.get())
        return l
        
    def run(self, *fns):
        queue = self.queue()
        processes=[self.paralelism(target=self.run_fn, args=(fn, queue)) for fn in fns]
        [p.start() for p in processes]
        [p.join() for p in processes]
        return self.get_result(queue)
        

# roda várias funções em multiprocessamento 
def runMultiprocessReturn(*fns):
    p=Paralelism(Process, PQueue)
    return p.run(*fns)

# roda várias funções em multithread
def runThreadReturn(*fns):
    p=Paralelism(Thread, TQueue)
    return p.run(*fns)




