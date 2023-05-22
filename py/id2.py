#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Condition, Thread
from queue import Queue

cv = Condition()
q = Queue()


def check_sum(x):
    while True:
        with cv:
            # Wait while queue is empty
            while q.empty():
                cv.wait()
            try:
                res = q.get_nowait()
                y = (5-2*x) / (6 - 5*x + x**2)
                print(f"The result check-function is: {y}")
                print(f"The sum S is: {res}")
                break
            except:
                pass



def s_sum(x):
    while True:
        with cv:
            while not q.empty():
                cv.wait()
            try:
                n = 1
                term = (1 / (2 ** n) + 1 / (3 ** n)) * (x ** (n - 1))
                epsilon = 1e-7
                ssum = term

                while abs(term) >= epsilon:
                    n += 1
                    term = (1 / (2 ** n) + 1 / (3 ** n)) * (x ** (n - 1))
                    ssum += term
                q.put(ssum)
                break
            except:
                pass


def main():
    x = -0.8
    thread1 = Thread(target=s_sum, args=(x,))
    thread1.start()
    thread2 = Thread(target=check_sum, args=(x,))
    thread2.start()
    with cv:
        cv.notify_all()


if __name__ == '__main__':
    main()