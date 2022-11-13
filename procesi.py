import numpy
import multiprocessing
from time import sleep
import pickle

svetovi = []
MAX_ITERACIJA = 20
n=20
m=20
simulacija = []
celije = []

class Celija(multiprocessing.Process):
    def __init__(self, x, y, ziv):
        multiprocessing.Process.__init__(self)
        self.x = x
        self.y = y
        self.iteracija = 0
        self.procitan = 0
        self.ziv = ziv

    def setQueue(self,queue1):
        self.susedi = queue1

    def odrediDalJeZivaLock(self):
        brojZivih = 0
        for i in self.susedi:
            while(i.iteracija != self.iteracija) :
                sleep(0.01)

            i.lock.acquire()
            if(i.ziv == 1):
                brojZivih+=1
            i.procitan += 1
            i.lock.release()

        while True:
            if (self.procitan >= len(self.susedi)):
                self.procitan -= len(self.susedi)
                break
            sleep(0.001)

        if self.ziv:
            self.ziv = True if (brojZivih == 2 or brojZivih == 3) else False
        else:
            self.ziv = True if (brojZivih == 3) else False
        svetovi[self.iteracija+1][self.y, self.x] = 1 if self.ziv else 0
    def run(self):
        print('called run method in process: %s' % self.name)
        return
def loop(svet):
    svetovi.append(svet)
    for i in range(1,MAX_ITERACIJA+1) :
        svetovi.append(numpy.zeros((n,m),int))

    for i in range (0,n) :
        for j in range (0,m) :
            celije.append(Celija(j,i,svet[i,j]))

    for c in celije :
        queue = multiprocessing.Queue()
        for i in range(c.y - 1, c.y + 2):
            for j in range(c.x - 1, c.x + 2):
                if (i < 0 or i >= n or j < 0 or j >= m or (c.y == i and c.x == j)): continue
                queue.put(celije[i*m+j])
    c.setQueue(queue)
    for c in celije :
        c.start()
        c.join()
if __name__ == '__main__':
    svet = numpy.zeros((n, m), int)
    svet[0,0]=1
    svet[0,2]=1
    svet[1,1]=1
    svet[1,2]=1
    svet[2,1]=1
    simulacija.append(svet)
    loop(svet)