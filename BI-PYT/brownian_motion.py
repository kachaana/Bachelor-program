#!/usr/bin/env python3

"""
Klasickým příkladem dvourozměrné náhodné procházky je Brownův pohyb: Pylové zrnko je tepelným pohybem molekul kapaliny v každém časovém okamžiku strkáno náhodnými směry o nějakou vzdálenost nějakou rychlostí. 
Zaznamenejte graficky pohyb pylového zrnka ze středu obrazovky k jejímu okraji (výpočet tedy končí dosažením libovolného ze čtyř okrajů). Barevně namapujte počet navštívení toho kterého místa.
Pohyb zrnka do všech směrů pokládejte za stejně pravděpodobný. Za směry berte sever–východ–jih–západ a navíc i čtyři diagonální.

Pylové zrnko se sice dále sráží (a tudíž mění směr) zcela náhodně, ale před další srážkou může urazit i podstatně delší dráhu než právě jednu jednotku.
Prakticky druhý požadavek můžete nepřekvapivě nasimulovat tak, že ke srážce s okolními molekulami dochází s jistou pravděpodobností menší než 1, takže zrnko může klidně několik kroků cestovat původním směrem, než dojde ke srážce a změně směru.

Řešte úlohu číslo 7 z „Náhody a pravděpodobnosti“ (podrobnosti k implementaci jsou v jí předcházejících úlohách od čísla 4), tedy Náhodnou procházku s různě dlouhým krokem (aka Brownův pohyb), tj. především:

* výstup je místo konzole do matplotlibu;
* náhodná procházka končí dosažením libovolného okraje grafu;
* různěkrát navštívená místa obarvěte různou barvou, ať to pěkně vypadá;
* ukládání (a načítání) historie pohybu neřešte, stačí pouze výsledný obrázek.
* Vyřešte tedy pouze jedno zobrazení „Brownova pohybu“ pro jedno spuštění skriptu, přičemž dbejte na obarvování (rozdělte počty navštívení toho kterého místa do několika tříd; možná trošku překvapivě jich není potřeba zase tak moc) a proměnnou délku kroku.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from enum import Enum
import random
import math

COLORS = ['w', 'r', 'g', 'y', 'b', 'm', 'r', 'c', 'k']

SIZE = 50
MAX_STEP = 3

matrix = [[0 for x in range(SIZE + 1)] for y in range(SIZE + 1)]

images = []


def random_step_size():
    return random.randint(1, MAX_STEP)


def change_color(x, y):
    matrix[x][y] += 1
    if matrix[x][y] >= 8:
        return 8
    else:
        return matrix[x][y]


def make_step(x, y, x_del, y_del, step):
    while step > 0:
        if check_borders(x, y) == 1:
            return x, y, 1
        x, y = x + x_del, y + y_del
        color = change_color(x, y)
        img = plt.plot(x, y, COLORS[color] + 's')
        images.append(images[-1] + img) if images else images.append(img)
        step -= 1
    return x, y, 0

# directions
#
#  8 1 2
#  7   3
#  6 5 4
#


def random_direction(x, y, step):
    z = 0
    dir = random.randint(1, 7)
    if dir == 1:
        return make_step(x, y, 0, -1, step)
    elif dir == 2:
        return make_step(x, y, 1, -1, step)
    elif dir == 3:
        return make_step(x, y, 1, 0, step)
    elif dir == 4:
        return make_step(x, y, 1, 1, step)
    elif dir == 5:
        return make_step(x, y, 0, 1, step)
    elif dir == 6:
        return make_step(x, y, -1, 1, step)
    return make_step(x, y, -1, 0, step)


def check_borders(x, y):
    if x == SIZE or y == SIZE or x == 0 or y == 0:
        return 1
    else:
        return 0


def main():
    fig = plt.figure()
    plt.axis([0, SIZE, 0, SIZE]) #xmin xmax ymin ymax
    plt.xticks([])
    plt.yticks([])
    x, y, z = random_direction(math.floor(SIZE / 2), math.floor(SIZE / 2), random_step_size())
    while z != 1:
        x, y, z = random_direction(x, y, random_step_size())
    animation = ArtistAnimation(fig, images, interval=100, repeat=0)
    plt.show()


if __name__ == "__main__":
    main()


