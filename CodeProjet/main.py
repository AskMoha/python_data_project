# -*- coding: utf-8 -*-
import csv

import networkx as nx

import matplotlib.pyplot as plt
import community
from matplotlib import cm

nbproc = 300
n1 = 0
n2 = 0
taille1=17
taille2=15


def maximum(liste):
    maxi = liste[0]
    for i in liste:
        if i >= maxi:
            maxi = i
    return maxi


def grandeurecartcolonne(j):
    compteur = 1
    datarecoit = []
    while compteur < nbproc:
        x = 0
        if data[compteur][j] != '-' and data[compteur][j] != '' and j >= 9 and data[compteur][j] != "traces":
            if "<" in data[compteur][j]:
                x = data[compteur][j].replace(",", ".")
                x = x.replace("<", "")
            if "<" not in data[compteur][j]:
                x = data[compteur][j].replace(",", ".")

        datarecoit.append(float(x))
        compteur = compteur + 1

    max = maximum(datarecoit)
    return max


def comapredeuxligne(i, k):
    compteur = 0
    j = 9

    while j < len(data[i]):
        if data[i][j] != '-' and data[i][j] != '' and j >= 9 and data[i][j] != "traces" and data[k][j] != '-' and \
                data[k][j] != '' and data[k][j] != 'traces' and k != i:
            if "<" in data[i][j]:
                x = data[i][j].replace(",", ".")
                x = x.replace("<", "")
            if "<" not in data[i][j]:
                x = data[i][j].replace(",", ".")

            if "<" in data[k][j]:
                y = data[k][j].replace(",", ".")
                y = y.replace("<", "")

            if "<" not in data[k][j]:
                y = data[k][j].replace(",", ".")

            z = grandeurecartcolonne(j)
            w = get_change(float(x), z)
            s = get_change(float(y), z)
            result = abs(w - s)
            if result <= taille1:
                compteur = compteur + 1

        j = j + 1

    return compteur


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


def onClick(event):
    (x, y) = (event.xdata, event.ydata)
    for i in G.nodes():
        node = pos[i]
        distance = pow(x - node[0], 2) + pow(y - node[1], 2)
        if distance < 0.0001:
            print("l'aliment choisi:")
            print(i)
            print("a pour voisins:")
            neighbor = list(G.neighbors(i))
            print(neighbor)


def on_press(event):
    global n1
    global n2
    if event.key == 'e':
        (x, y) = (event.xdata, event.ydata)
        for i in G.nodes():
            node = pos[i]
            distance = pow(x - node[0], 2) + pow(y - node[1], 2)
            if distance < 0.0001:
                n1 = i
                print("le premier aliment choisi est:")
                print(n1)
    if event.key == 'm':
        (x, y) = (event.xdata, event.ydata)
        for i in G.nodes():
            node = pos[i]
            distance = pow(x - node[0], 2) + pow(y - node[1], 2)
            if distance < 0.0001:
                n2 = i
                print("le second aliment choisi est:")
                print(n2)
    if event.key == 'x':
        if (n1 != 0 and n2 != 0):
            paths = list(nx.shortest_simple_paths(G, n1, n2))
            print("le chemin entre ces deux aliments est :")
            print(paths[0])


if __name__ == '__main__':
    with open('TableAliments.csv', newline='', encoding="ISO-8859-1") as csvfile:
        data = list(csv.reader(csvfile, delimiter=';'))

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('button_press_event', onClick)
    fig.canvas.mpl_connect('key_press_event', on_press)

    G = nx.Graph()
    compteur = 1
    result = 0
    liste = []
    while compteur < nbproc:

        if compteur != nbproc - 1:
            i = compteur + 1
            while i < nbproc:
                liste.append(comapredeuxligne(compteur, i))
                i = i + 1
        compteur = compteur + 1
    print(liste)

    compteur = 1
    k = 1
    while compteur < nbproc:
        G.add_node(data[compteur][7], test=data[compteur][7])

        if compteur != nbproc - 1:
            i = compteur + 1
            while i < nbproc:
                result = liste[k - 1]
                if result > taille2:
                    G.add_edge(data[compteur][7], data[i][7])
                i = i + 1
                k = k + 1

        compteur = compteur + 1

    partition = community.best_partition(G)
    pos = nx.fruchterman_reingold_layout(G)

    cmap = cm.get_cmap('Spectral', max(partition.values()) + 1)
    """"
    on peut ajouter les labels en ajoutant le paramètre with_labels="true" à nx.draw
    """
    nx.draw(G, pos, node_size=110, cmap=cmap, node_color=list(partition.values()), font_size=5)
    nx.draw_networkx_edges(G, pos, alpha=0.4)



    plt.show()
