from time import sleep
from multiprocessing import  Lock
import numpy
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np
import threading


# for i in range(y - 1, y + 2):
 #               for j in range(x - 1, x + 2):
     #               if (i < 0 or i >= n or j < 0 or j >= m or (y == i and x == j)): continue
      #              if (svet[i, j] == 1):
        #                brojZivih += 1

svetovi = []
MAX_ITERACIJA = 10
celije = []
locks = []
br = 0
n=20
m=20
simulacija = []
printlock = Lock()
class Celija(threading.Thread):
    def __init__(self, x, y, ziv, susedi):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.susedi = susedi
        self.iteracija = 0
        self.procitan = 0
        self.ziv = ziv
        self.lock = Lock()


    def odrediDalJeZiva(self):
        brojZivih = 0
        for i in self.susedi:
            i.lock.acquire()
            if(i.ziv == 1):
                brojZivih+=1
            i.procitan += 1
            i.lock.release()


        while True:
            self.lock.acquire()
            if (self.procitan >= len(self.susedi)):
                self.procitan -= len(self.susedi)
                break
            self.lock.release()
            sleep(0.001)

        if self.ziv:
            self.ziv = True if (brojZivih == 2 or brojZivih == 3) else False
        else:
            self.ziv = True if (brojZivih == 3) else False
        self.lock.release()
        svetovi[self.iteracija+1][self.y, self.x] = 1 if self.ziv else 0

    def run(self):
        global br
        while self.iteracija<MAX_ITERACIJA:
            self.odrediDalJeZiva()
            self.iteracija+=1



#def iteracija(svet):
    #narednisvet = numpy.zeros((n, m), int)
    #for i, j in np.ndindex(svet.shape):
        #narednisvet[i,j]=odrediDalJeZiva(i,j, svet)

    #return narednisvet


def loop(svet, br):

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




if __name__ == '__main__':
    svet = numpy.zeros((n,m),int)
    svet[0,0]=1
    svet[0,2]=1
    svet[1,1]=1
    svet[1,2]=1
    svet[2,1]=1
    simulacija.append(svet)
    #print(svet)
    loop(svet, 10)
    print("gotovo")
    #steps = [(np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8) for i in range(50)]
    #anim = animate(simulacija);
    #HTML(anim.to_html5_video())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


