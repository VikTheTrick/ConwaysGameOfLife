from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from IPython.display import HTML
import multiprocessing
import numpy
import math

bp = 1
n = 100
m = 100
iteracije = 100

svet = []
svet = multiprocessing.Array('i', numpy.random.randint(2, size=(n*m)))

steps = []
steps.append(numpy.copy(svet).reshape((n, m)))

def ziva(y, x):
    c = 0
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if(j < 0 or i < 0 or j >= m or i >= n or (i == y and j == x)):
                continue
            c += svet[i*m+j]
    return c == 3 or (c == 2 and svet[y*m+x])


def obradi(segment):
    (prvi, poslednji) = indeksi(segment)
    niz = []
    for i in range(prvi, poslednji+1):
        x = i % m
        y = math.floor(i/m)
        niz.append(1 if ziva(y, x) else 0)
    return niz


def indeksi(i):
    pocetak = math.floor(n*m/bp*i)
    kraj = math.floor(n*m/bp*(i+1))-1
    return (pocetak, kraj)

pool = multiprocessing.Pool(bp)
for i in range(0, iteracije):
    rez = pool.map(obradi, list(range(0, bp)),)
    brojac = 0
    for y in range(0, len(rez)):
        for x in range(0, len(rez[y])):
            svet[brojac] = rez[y][x]
            brojac += 1
            
    steps.append(numpy.copy(svet).reshape((n, m)))
pool.close()
pool.join()

def animate(steps):
  def init():
    im.set_data(steps[0])
    return [im]
  
  
  def animate(i):
    im.set_data(steps[i])
    return [im]

  im = plt.matshow(steps[0], interpolation='None', animated=True)
  
  anim = FuncAnimation(im.get_figure(), animate, init_func=init,
                  frames=len(steps), interval=100, blit=True, repeat=False)
  return anim


anim = animate(steps)
HTML(anim.to_html5_video())