#imports
from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import numpy as np
from queue import PriorityQueue 
import math
#Clase Ventana
#Sirve para tener una interfaz gráfica para la app
class Ventana(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        v = tk.IntVar()
        menu_msg = "" \
                   "Laboratorio 01: Búsqueda a ciegas vs búsqueda Heurística"
        self.menu_tktext = Label(root, text=menu_msg)
        self.menu_tktext.pack()

        self.boton1 = Button(root, text="Búsqueda ciega", command=lambda: flujo_principal(0,entry.get(),entry2.get()))
        self.boton2 = Button(root, text="Búsqueda heurística", command=lambda: flujo_principal(1,entry.get(),entry2.get()))
        self.boton1.pack(side="left")
        self.boton2.pack(side="right")
        
#Clase Grafo
class Graph():
    G = nx.Graph()
    coordinates ={} #para impresion
    size_x=0
    size_y=0
    table=np.zeros((size_x, size_y))

    def __init__(self, x, y):
        cont=0
        self.size_x=x
        self.size_y=y
        self.table=np.zeros((self.size_x, self.size_y))

        for i in range(0,self.size_x):
            for j in range(0,self.size_y):
                self.G.add_node(cont)
                self.table[i][j]=cont
                self.G.nodes[cont]['coords']=(i,j)
                self.coordinates[cont]=(i,j)
                cont+=1
        self.hacer_conexiones()

    def neighbors(self, rowNumber, columnNumber, radius):
        return [[self.table[i][j] if  i >= 0 and i < len(self.table) and j >= 0 and j < len(self.table[0]) else -1
                 for j in range(columnNumber-1-radius, columnNumber+radius)]
                    for i in range(rowNumber-1-radius, rowNumber+radius)]

    def hacer_conexiones(self):
        for k in list(self.G.nodes()):
            neigh=np.zeros((3, 3))
            neigh=self.neighbors(self.G.nodes[k]['coords'][0],self.G.nodes[k]['coords'][1],1)

            if(neigh[1][1] != -1):
                self.G.add_edge(k,neigh[1][1],color='green')

            if(neigh[1][2] != -1):
                self.G.add_edge(k,neigh[1][2],color='green')

            if(neigh[2][1] != -1):
                self.G.add_edge(k,neigh[2][1],color='green')

            if(neigh[1][2] != -1 and neigh[2][1] != -1):
                self.G.add_edge(neigh[1][2],neigh[2][1],color='green')

    def print_grafo(self):
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos=self.coordinates,node_size=16)
        edges=self.G.edges()
        colors=[self.G[u][v]['color']for u,v in edges]
        nx.draw_networkx_edges(self.G,pos=self.coordinates,edge_color=colors)
        plt.tight_layout()
        plt.show()
        
    def eliminar_nodos(self):
        cant_nodos=self.size_x*self.size_y
        nodos_borrados={}
        for i in range(int(cant_nodos*0.2)):
            while(True):
                try:
                    index=random.randint(0,cant_nodos-1)
                    self.G.remove_node(index)
                    nodos_borrados[i]=self.coordinates[index]
                except :
                    pass
                else:
                    break
        return nodos_borrados
    
    def heuristic(self, a, b):
        aX = (a)[0]
        aY = (a)[1]
        bX = (b)[0]
        bY = (b)[1]
        return math.sqrt((bX - aX) ** 2 + (bY - aY) ** 2)

    def A_star(self, StartX, StartY, EndX, EndY):
        #Hallar nodo en si
        INICIO=0
        FIN=0
        for i in self.coordinates:
            if(self.coordinates[i][0]==EndX and self.coordinates[i][1]==EndY):
                FIN=i
                break
        for i in self.coordinates:
            if(self.coordinates[i][0]==StartX and self.coordinates[i][1]==StartY):
                INICIO=i
                break
        Pawn=PriorityQueue()
        Pawn.put(INICIO,0)
        came_from={}
        score={}
        came_from[INICIO]=None
        score[INICIO]=0
        while not Pawn.empty():
            current=Pawn.get()
            if current==FIN:
                break
            for Next in self.G.neighbors(current):
                tentative_score=score[current]+self.heuristic(self.coordinates[current],self.coordinates[FIN])
                if Next not in score or tentative_score<score[Next]:
                    score[Next]=tentative_score
                    fscore=tentative_score+self.heuristic(self.coordinates[FIN],self.coordinates[Next])
                    Pawn.put(Next,fscore)
                    came_from[Next]=current
        returnPath={}
        returner=FIN
        pathsize=0
        while returner is not INICIO:
            returnPath.update({returner: came_from[returner]})
            #print(self.coordinates[returner])
            self.G.add_edge(returner,came_from[returner],color='red',weight=6)
            returner=came_from[returner]
            pathsize=pathsize+1
        #print(self.coordinates[INICIO])

        


def flujo_principal(valor,x,y):
    if(valor==0):
        print("Se ejecuta búsqueda a ciegas con x="+str(x)+" y y="+str(y))
    elif(valor==1):
        print("Se ejecuta búsqueda heurística con x="+str(x)+" y y="+str(y))
        
if __name__ == '__main__':
    root = Tk()
    root.title("Laboratorio 01")
    root.geometry("500x300")
    entry=tk.Entry(root)
    entry.insert(0,"Ingrese 'x'")
    entry.place(x=250,y=50)
    entry2=tk.Entry(root)
    entry2.insert(0,"Ingrese 'y'")
    entry2.place(x=250,y=75)
    ingrese1=Text(root)
    ventana=Ventana(master=root)
    entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
    entry2.bind("<FocusIn>", lambda args: entry2.delete('0', 'end'))
    #ventana.mainloop()
    grafo=Graph(20,20)
    nd_deleted=grafo.eliminar_nodos()
    ax=1
    ay=3
    se_ejecuta=True
    for i in nd_deleted:
        if nd_deleted[i][0]==ax and nd_deleted[i][1]==ay:
            print('Este nodo ya no existe uwu')
            se_ejecuta=False
            break
    if se_ejecuta:
        grafo.A_star(0,0,9,6)
        grafo.print_grafo()