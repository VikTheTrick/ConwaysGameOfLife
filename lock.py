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
            sleep(0.01)

        self.ziv = brojZivih == 3 or (brojZivih == 2 and self.ziv)
        svetovi[self.iteracija+1][self.y, self.x] = 1 if self.ziv else 0

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

svet = numpy.random.randint(2, size=(n,m))
loop(svet)
sleep(1)

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

anim = animate(svetovi);
HTML(anim.to_html5_video())