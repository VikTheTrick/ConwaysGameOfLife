import queue

import numpy
import multiprocessing
from multiprocessing import Process, Queue

from time import sleep
import pickle

MAX_ITERACIJA = 10
n = 15
m = 15
simulacija = []
celije = []
krajnjiSvetovi =[]

class Poruka():
    def __init__(self, stanje, x, y, iteracija):
        self.stanje = stanje
        self.x = x
        self.y = y
        self.iteracija = iteracija


class Celija(Process):
    def __init__(self, x, y, ziv, consumerQueue, iterationQueue):
        multiprocessing.Process.__init__(self)
        self.x = x
        self.y = y
        self.iteracija = 0
        self.procitaliMe = 0
        self.ziv = ziv
        self.susedi = dict()
        self.ziviSusedi = 0
        self.consumerQueue = consumerQueue
        self.iterationQueue = iterationQueue

    def pozicija(self, x, y):
        return (self.y * m + self.x) > (y * m + x)

    def iterate(self):
        for sused in self.susedi:
            if self.pozicija(sused[0], sused[1]):
                self.susedi[sused].put(self.ziv)
            else:
                while self.susedi[sused].empty():
                    sleep(0.01)
                self.ziviSusedi += self.susedi[sused].get()
        for sused in self.susedi:
            if self.pozicija(sused[0], sused[1]):
                while not self.susedi[sused].qsize() == 2:
                    sleep(0.01)
                self.procitaliMe += 1
                self.ziviSusedi += self.susedi[sused].get()
            else:
                self.susedi[sused].put(self.ziv)
                self.susedi[sused].put(1)
                while not self.susedi[sused].qsize() == 1:
                    sleep(0.01)
                self.procitaliMe += self.susedi[sused].get()
        if self.ziv:
            self.ziv = 1 if self.ziviSusedi == 2 or self.ziviSusedi == 3 else 0
        else:
            self.ziv = 1 if self.ziviSusedi == 3 else 0

        self.procitaliMe = 0
        self.ziviSusedi = 0
        self.iteracija += 1
        self.consumerQueue.put(Poruka(self.ziv, self.x, self.y, self.iteracija))


        while self.iterationQueue.qsize() != self.iteracija:
            sleep(0.1)

    def run(self):
        while self.iteracija < MAX_ITERACIJA:
            self.iterate()
            # cekamo da q size bude n*m
        return


def consumer(queue, svetovi, iterationQueue):
    iteracija = 0
    # consume work
    global krajnjiSvetovi
    while iteracija < MAX_ITERACIJA * n * m:
        try:
            item = queue.get()
            iteracija += 1
            if iteracija % (n * m) == 0:
                print("desilo se")
                iterationQueue.put(1)
            svetovi[item.iteracija][item.y, item.x] = item.stanje
        except queue.Empty:
            sleep(0.01)
    print("svetovi")
    krajnjiSvetovi = svetovi
    print(svetovi)


def loop(svetovi):
    consumerQueue = Queue()
    iterationQueue = Queue()
    consumerProcess = multiprocessing.Process(target=consumer, kwargs={'queue': consumerQueue, 'svetovi': svetovi, 'iterationQueue' : iterationQueue})
    for i in range(0, n):
        for j in range(0, m):
            celije.append(Celija(j, i, svetovi[0][i, j], consumerQueue, iterationQueue))

    for c in celije:
        for i in range(c.y - 1, c.y + 2):
            for j in range(c.x - 1, c.x + 2):
                if i < 0 or i >= n or j < 0 or j >= m or (c.y == i and c.x == j):
                    continue
                trenQueue = Queue()
                imaGa = (j, i) in c.susedi
                if not imaGa:
                    c.susedi[(j, i)] = trenQueue
                    celije[i * m + j].susedi[(c.x, c.y)] = trenQueue

    consumerProcess.start()
    for c in celije:
        c.start()
    consumerProcess.join()
    for c in celije:
        c.join()


if __name__ == '__main__':
    svet = numpy.zeros((n, m), int)
    svet[0, 0] = 1
    svet[0, 2] = 1
    svet[1, 1] = 1
    svet[1, 2] = 1
    svet[2, 1] = 1
    svetovi = []
    svetovi.append(svet)
    for iterator in range(1, MAX_ITERACIJA + 1):
        svetovi.append(numpy.zeros((n, m), int))
    simulacija.append(svetovi)
    loop(svetovi)
    print("kraj")
    for i in krajnjiSvetovi:
        print(i)
