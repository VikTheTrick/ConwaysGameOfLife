import queue

import numpy
import multiprocessing
from multiprocessing import Process, Queue

from time import sleep
import pickle

svetovi = []
MAX_ITERACIJA = 5
n = 5
m = 5
simulacija = []
celije = []


class Celija(Process):
    def __init__(self, x, y, ziv):
        multiprocessing.Process.__init__(self)
        self.x = x
        self.y = y
        self.iteracija = 0
        self.procitaliMe = 0
        self.ziv = ziv
        self.susedi = set()
        self.redovi = []
        self.ziviSusedi = 0
        self.pozicije = []
        self.lock = multiprocessing.Lock()
    def addQueue(self, queue1):
        self.redovi.append(queue1)

    def iterate(self):
        for index in range(len(self.redovi)):
            if self.redovi[index].empty():
                self.redovi[index].put(self.ziv)
            else:
                self.pozicije[index] = 1
                self.ziviSusedi += self.redovi[index].get()
                self.redovi[index].put(self.ziv)
                self.redovi[index].put(self.ziv)

        for index in range(len(self.redovi)):
            if self.pozicije[index] == 0:
                while self.redovi[index].qsize() != 2:
                    sleep(0.01)
                self.ziviSusedi += self.redovi[index].get()
                self.redovi[index].get()
                self.procitaliMe += 1

            else:
                while not self.redovi[index].empty():
                    sleep(0.01)
                self.procitaliMe += 1

        print(self.ziviSusedi)
        if self.ziv:
            self.ziv = 1 if (self.ziviSusedi == 2 or self.ziviSusedi == 3) else 0
        else:
            self.ziv = 1 if (self.ziviSusedi == 3) else 0
        svetovi[self.iteracija + 1][self.y, self.x] = self.ziv

    def run(self):
        self.pozicije = [0] * (len(self.redovi))
        while self.iteracija < MAX_ITERACIJA:
            self.iterate()
            self.ziviSusedi = 0
            self.procitaliMe = 0
            self.iteracija += 1
        return


def loop(svet1):
    svetovi.append(svet1)
    for iterator in range(1, MAX_ITERACIJA + 1):
        svetovi.append(numpy.zeros((n, m), int))

    for iterator in range(0, n):
        for j in range(0, m):
            celije.append(Celija(j, iterator, svet1[iterator, j]))

    for c in celije:
        for iterator in range(c.y - 1, c.y + 2):
            for j in range(c.x - 1, c.x + 2):
                if iterator < 0 or iterator >= n or j < 0 or j >= m or (c.y == iterator and c.x == j): continue
                trenQueue = Queue()
                imaGa = (j, iterator) in c.susedi
                if not imaGa:
                    c.susedi.add((j, iterator))
                    celije[(iterator * m + j)].susedi.add((c.x, c.y))
                    c.addQueue(trenQueue)
                    celije[(iterator * m + j)].addQueue(trenQueue)

    for c in celije:
        c.start()
    for c in celije:
        c.join()


if __name__ == '__main__':
    svet = numpy.zeros((n, m), int)
    svet[0, 0] = 1
    svet[0, 2] = 1
    svet[1, 1] = 1
    svet[1, 2] = 1
    svet[2, 1] = 1
    simulacija.append(svet)
    loop(svet)
    print("kraj")
    for i in svetovi:
        print(i)
