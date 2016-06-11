#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geekman2
#
# Created:     17/01/2014
# Copyright:   (c) Geekman2 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import multiprocessing
import Queue
import IndexnCrawl as Crawl


def worker(q1,q2):
    while True:
        # get item from queue, do work on it, let queue know processing is done for one item
        item = q1.get()
        print item
        q2.put(Crawl.crawl_web(item))
        q1.task_done()

def main(number):
    workers = 5
    processes = []
    work_queue = Queue.Queue()
    done_queue = Queue.Queue()

    for item in range(number):
        work_queue.put(item)

    for w in xrange(workers):
        p = multiprocessing.Process(target=worker, args = (work_queue,done_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__':
    main(input("Number"))
