#barijere bez colaba
from time import sleep
from multiprocessing import  Barrier
import numpy
import threading

svetovi = []
MAX_ITERACIJA = 200
n=50
m=50
celije = []
barijera = Barrier(n*m)

class Celija(threading.Thread):
    def __init__(self, x, y, ziv, susedi):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.susedi = susedi
        self.iteracija = 0
        self.procitan = 0
        self.ziv = ziv

    def odrediDalJeZiva(self):
        global cekaonica
        brojZivih = 0

        for i in self.susedi:
            if(i.ziv):
                brojZivih+=1

        b = barijera.wait()
        if b==n*m-1:
            barijera.reset()

        if self.ziv:
            self.ziv = True if (brojZivih == 2 or brojZivih == 3) else False
        else:
            self.ziv = True if (brojZivih == 3) else False
        svetovi[self.iteracija+1][self.y, self.x] = 1 if self.ziv else 0

        b = barijera.wait()
        if b==n*m-1:
            barijera.reset()


    def run(self):
        while self.iteracija<MAX_ITERACIJA:
            self.odrediDalJeZiva()
            self.iteracija+=1



def loop(svet):
    svetovi.append(svet)
    for i in range(1,MAX_ITERACIJA+1) :
        svetovi.append(numpy.zeros((n,m),int))

    for i in range (0,n) :
        for j in range (0,m) :
            celije.append(Celija(j,i,svet[i,j], set()))
    for c in celije :
        for i in range(c.y - 1, c.y + 2):
            for j in range(c.x - 1, c.x + 2):
                if (i < 0 or i >= n or j < 0 or j >= m or (c.y == i and c.x == j)): continue
                c.susedi.add(celije[i*m+j])
    for c in celije :
        c.start()
    for c in celije :
        c.join()

svet = numpy.random.randint(2, size=(n,m))
loop(svet)


def prikazisvet(svet, indeks):
    s=""
    s+="\n"+str(indeks)+"\n"
    for red in svet:
        for slovo in red:
            s+="0 " if slovo==1 else "  "
        s+="\n"
    print(s)
            
def prikazi(svetovi):
    indeks = 0
    for s in svetovi:
        prikazisvet(s, indeks)
        sleep(0.5)
        indeks+=1

prikazi(svetovi)