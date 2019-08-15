import numpy as np

import Ray

import multiprocessing
from multiprocessing import Process
import os
import time




def c(queue, noth):
  guy = Ray.Chess_AI()
  a = guy.print_python_stuff()
  queue.put(a)

def p():
  queue = multiprocessing.Queue()



  for i in range(20):

    if not queue.empty():
      print(queue.get())

    # SPAWN NEW PROCESS HERE (WOULD BE THE AI)
    if i == 5:
      cc = Process(target=c, args=(queue, 0))
      cc.start()

    print(f"python printing {i}")
    time.sleep(0.3)


if __name__ == '__main__':

  pp = Process(target=p)
  pp.start()

# def worker(procnum, send_end):
#     '''worker function'''
#     result = str(procnum) + ' represent!'
#     print result
#     send_end.send(result)

# def main():
#     jobs = []
#     pipe_list = []
#     for i in range(5):
#         recv_end, send_end = multiprocessing.Pipe(False)
#         p = multiprocessing.Process(target=worker, args=(i, send_end))
#         jobs.append(p)
#         pipe_list.append(recv_end)
#         p.start()

#     for proc in jobs:
#         proc.join()
#     result_list = [x.recv() for x in pipe_list]
#     print result_list