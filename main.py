from time import sleep

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

class Celija(threading.Thread):
    def __init__(self, x, y, ziv, **susedi):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.susedi = susedi
        self.iteracija = 0
        self.procitan = 0
        self.ziv = ziv


    def odrediDalJeZiva(self):
        brojZivih = 0
        for i in self.susedi.keys():
            if(self.susedi[i].ziv == 1):
                brojZivih+=1
            self.susedi[i].procitan+=1 #treba da se lokuje

        while(self.procitan!=len(self.susedi)):
            sleep(0.001)

        if self.ziv:
            self.ziv = True if (brojZivih == 2 or brojZivih == 3) else False
        else:
            self.ziv = True if (brojZivih == 3) else False
        svetovi[self.iteracija][self.y, self.x] = 1 if self.ziv else 0

    def run(self):
        while self.iteracija<MAX_ITERACIJA:
            self.odrediDalJeZiva()
            self.iteracija+=1

n=10
m=10
simulacija = []

#def iteracija(svet):
    #narednisvet = numpy.zeros((n, m), int)
    #for i, j in np.ndindex(svet.shape):
        #narednisvet[i,j]=odrediDalJeZiva(i,j, svet)

    #return narednisvet


def loop(svet, br):
    while br>0:

        svet=iteracija(svet)
        simulacija.append(svet)
        #print(svet)
        #print("novi red \n")
        br-=1
        #print(na)


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
                         frames=len(steps), interval=500, blit=True, repeat=False);
    return anim




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
    print(simulacija)
    n = 10
    #steps = [(np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8) for i in range(50)]
    anim = animate(simulacija);
    HTML(anim.to_html5_video())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


