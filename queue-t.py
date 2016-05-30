# import traceback
# import sys
# import logging
#
# glist = ['a', 'b', 'c', 'd', 'e']
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     filename='test.log',
#     filemode='w',
#     format='%(asctime)s %(filename)s [line:(lineno)d] %(levelname)s %(message)s',
#
#coding=utf-8
import Queue
import threading
import random


class Producer(threading.Thread):
    def __init__(self, q, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        print "Producer " + self.name + " Started"

    def run(self):
        while 1:
            if self.q.full():
                print self.q.qsize()
                print self.name + 'Queue is full,producer wait\n'
            else:
                value = random.randint(0, 10)
                print self.name + " put value: " + str(value) + "into queue\n"
                self.q.put((self.name + ":" + str(value)))


class Consumer(threading.Thread):
    def __init__(self, q, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        print "Consumer " + self.name + " started\n "

    def run(self):
        while 1:
            if self.q.empty():
                print 'queue is empty,consumer wait!\n'
            else:
                value = self.q.get()
                print self.name + "get value" + value + " from queue\n"


if __name__ == "__main__":
    q = Queue.Queue(10)
    p = Producer(q, "P1")
    p.start()
    p1 = Producer(q, "P2")
    p1.start()
    c1 = Consumer(q, "C1")
    c1.start()
    q.join()
