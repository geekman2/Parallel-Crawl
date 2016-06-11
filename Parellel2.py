from multiprocessing import Process, Queue
from multiprocessing.process import current_process
import IndexnCrawl as Crawl


def arbitary_function(number):
    print "Executing number %s from %s" % (number, current_process().name)
    return True

def worker(worker_queue, result_queue):
    try:
        for number in iter(worker_queue.get, None):
            print number
            Crawl.crawl_web(number)
            result_queue.put("%s success with: %s" % (number,
                                                      current_process().name))
    except Exception, e:
        result_queue.put("%s failed with: %s" % (current_process().name,
                                                       e.message))


if __name__ == "__main__":
    worker_queue = Queue()
    result_queue = Queue()

    for n in range(1,10):
        worker_queue.put(n)

    core_worker = 2
    workers = [Process(target=worker, args=(worker_queue, result_queue)) for i in range(core_worker)]
    
    for each in workers:
        each.start()
        print 'started'

    for r in iter(result_queue.get, None):
        print r
