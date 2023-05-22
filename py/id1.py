#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint
from threading import Condition, Thread
from queue import Queue
from time import sleep
from typing import List

cv = Condition()
q = Queue()


def customer(books):
    while True:
        with cv:
            while not q.empty():
                cv.wait()
            try:
                for i in range(10):
                    n_book = randint(0, 5)
                    q.put(f"заказ №{i + 1}: {books[n_book]}")
                    if i % 4 == 0:
                        q.put("full order")

                    print(f"Новый заказ!")
                break
            except:
                pass


# Consumer function for order processing
def order_processor(shop):
    while True:
        with cv:
            # Wait while queue is empty
            while q.empty():
                cv.wait()
            try:
                # Get data (order) from queue
                order = q.get_nowait()
                if order == "full order":
                    print("full order!")
                    break
                print(f"В магазин {shop} {order}")

            except:
                pass




if __name__ == "__main__":
    # Run order processors
    books: list[str] = ['Алые паруса', 'Недоросль', 'До встречи с тобой',
             'Заводной апельсин', 'Три товарища', 'Ася']
    Thread(target=customer, args=(books, )).start()
    Thread(target=order_processor, args=("Князь Мышкин",)).start()
    Thread(target=order_processor, args=("Читай-Город",)).start()
    Thread(target=order_processor, args=("Лабиринт",)).start()
    # Notify all consumers
    with cv:
        cv.notify_all()