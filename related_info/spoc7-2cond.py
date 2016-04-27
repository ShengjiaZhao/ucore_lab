__author__ = 'shengjia'

from threading import *
import time
import random

class Storage:
    def __init__(self, M, N):
        self.a = 0
        self.b = 0
        self.c = 0
        self.condition = Condition()
        self.N = N
        self.M = M

    def check(self):
        assert(self.a >= 0 and self.b >= 0)
        assert(self.a - self.b <= self.N)
        assert(self.b - self.a <= self.M)

class A(Thread):
    def __init__(self, storage):
        Thread.__init__(self)
        self.storage = storage

    def run(self):
        while True:
            self.storage.condition.acquire()
            while self.storage.a - self.storage.b >= self.storage.N:
                self.storage.condition.wait()
            self.storage.a += 1
            print("Added a A, A=" + str(self.storage.a) + ", B=" + str(self.storage.b))
            self.storage.check()
            self.storage.condition.notify()
            self.storage.condition.release()


class B(Thread):
    def __init__(self, storage):
        Thread.__init__(self)
        self.storage = storage

    def run(self):
        while True:
            self.storage.condition.acquire()
            while self.storage.b - self.storage.a >= self.storage.M:
                self.storage.condition.wait()
            self.storage.b += 1
            print("Added a B, A=" + str(self.storage.a) + ", B=" + str(self.storage.b))
            self.storage.check()
            self.storage.condition.notify()
            self.storage.condition.release()
            # time.sleep(random.random())


class Consumer(Thread):
    def __init__(self, storage):
        Thread.__init__(self)
        self.storage = storage

    def run(self):
        while True:
            self.storage.condition.acquire()
            while self.storage.a <= 0 or self.storage.b <= 0:
                self.storage.condition.wait()
            self.storage.a -= 1
            self.storage.b -= 1
            self.storage.c += 1
            print("Produced a C, A=" + str(self.storage.a) + ", B=" + str(self.storage.b) + ", C=" + str(self.storage.c))
            self.storage.check()
            self.storage.condition.notify()
            self.storage.condition.release()

            # time.sleep(random.random())

if __name__ == '__main__':
    storage = Storage(2, 4)
    thread1 = A(storage)
    thread1.start()
    thread2 = B(storage)
    thread2.start()
    thread3 = Consumer(storage)
    thread3.start()