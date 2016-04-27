__author__ = 'shengjia'

from threading import *
import time
import random

class Storage:
    def __init__(self, M, N):
        self.a = 0
        self.b = 0
        self.c = 0
        self.lock = Lock()
        self.a_sem = Semaphore(0)
        self.b_sem = Semaphore(0)
        self.a_minus_b_sem = Semaphore(M)
        self.b_minus_a_sem = Semaphore(N)
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
            self.storage.b_minus_a_sem.acquire()
            self.storage.lock.acquire()
            self.storage.a += 1
            print("Added a A, A=" + str(self.storage.a) + ", B=" + str(self.storage.b))
            self.storage.check()
            self.storage.lock.release()
            self.storage.a_minus_b_sem.release()
            self.storage.a_sem.release()
            # time.sleep(random.random())


class B(Thread):
    def __init__(self, storage):
        Thread.__init__(self)
        self.storage = storage

    def run(self):
        while True:
            self.storage.a_minus_b_sem.acquire()
            self.storage.lock.acquire()
            self.storage.b += 1
            print("Added a B, A=" + str(self.storage.a) + ", B=" + str(self.storage.b))
            self.storage.check()
            self.storage.lock.release()
            self.storage.b_minus_a_sem.release()
            self.storage.b_sem.release()
            # time.sleep(random.random())


class Consumer(Thread):
    def __init__(self, storage):
        Thread.__init__(self)
        self.storage = storage

    def run(self):
        while True:
            self.storage.a_sem.acquire()
            self.storage.b_sem.acquire()
            self.storage.lock.acquire()
            self.storage.a -= 1
            self.storage.b -= 1
            self.storage.c += 1
            print("Produced a C, A=" + str(self.storage.a) + ", B=" + str(self.storage.b) + ", C=" + str(self.storage.c))
            self.storage.check()
            self.storage.lock.release()

            # time.sleep(random.random())

if __name__ == '__main__':

    mutex = Lock()

    storage = Storage(2, 4)
    thread1 = A(storage)
    thread1.start()
    thread2 = B(storage)
    thread2.start()
    thread3 = Consumer(storage)
    thread3.start()