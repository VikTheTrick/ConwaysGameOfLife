#30x30 100 iteracija 27 sekundi, pre pokretanja treba restart runtime na colabu

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import numpy as np
from time import sleep
from multiprocessing import  Lock, Condition, Barrier
import numpy
import threading

svetovi = []
MAX_ITERACIJA = 100
n=30
m=30
celije = []
usle = 0
izasle = n*m
bool = True
lock = Lock()

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
        global izasle, usle, bool, lock
        brojZivih = 0

        for i in self.susedi:
            if(i.ziv):
                brojZivih+=1
        while True:
            lock.acquire()
            if(izasle==n*m):
                break
            lock.release()
            sleep(0.01)
        lock.release()
        lock.acquire()
        if usle==0:
            usle+=1
            bool = False
        elif usle==n*m-1:
            usle=0
            bool = True
            izasle = 0
        else:
            usle+=1
        lock.release()
        self.ziv = brojZivih == 3 or (brojZivih == 2 and self.ziv)
        self.iteracija+=1
        svetovi[self.iteracija][self.y, self.x] = 1 if self.ziv else 0


        while True:
            with lock:
                if bool: break
            sleep(0.01)
        with lock:
            izasle += 1


    def run(self):
        while self.iteracija<MAX_ITERACIJA:
            self.odrediDalJeZiva()



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

def animate(steps):
  ''' Prima niz matrica (svaka matrica je stanje u jednom koraku simulacije) 
  prikazuje razvoj sistema'''
  
  def init():
    im.set_data(steps[0])
    return [im]
  
  
  def animate(i):
    im.set_data(steps[i])
    return [im]

  im = plt.matshow(steps[0], interpolation='None', animated=True);
  
  anim = FuncAnimation(im.get_figure(), animate, init_func=init,
                  frames=len(steps), interval=100, blit=True, repeat=False);
  return anim

anim = animate(svetovi)
HTML(anim.to_html5_video())