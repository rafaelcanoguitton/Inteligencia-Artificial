#imports
from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import math
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

        self.boton1 = Button(root, text="Búsqueda ciega", command=lambda: flujo_principal(0,entry.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
        self.boton2 = Button(root, text="Búsqueda heurística(A*)", command=lambda: flujo_principal(1,entry.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
        self.boton3 = Button(root, text="Búsqueda heurística(Hill Climbing", command=lambda: flujo_principal(2,entry.get(),entry2.get(),entry3.get(),entry4.get(),entry5.get()))
        self.boton1.pack(side="left")
        self.boton3.pack(side="left")
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
                self.G.nodes[cont]['path']=False
                self.coordinates[cont]=(i,j)
                cont+=1
        self.hacer_conexiones()

    def neighbors(self, rowNumber, columnNumber, radius):
        return [[self.table[i][j] if  i >= 0 and i < len(self.table) and j >= 0 and j < len(self.table[0]) else -1
                 for j in range(columnNumber-1-radius, columnNumber+radius)]
                    for i in range(rowNumber-1-radius, rowNumber+radius)]

    
    def get_key(self,val,dist_neighbors): 
        for key, value in dist_neighbors.items(): 
             if val == value: 
                 return key 
        return "key doesn't exist"

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
    
##################################################################################################################################################
#Heuristic
    def hill_climbing(self, n_nodos, nodo_ini, nodo_objetivo):
        distancia_nodo_objetivo={}

        for i in range(0,n_nodos):
            if i != n_nodos:
                distancia_nodo_objetivo[i]=(round(math.sqrt(((self.G.nodes[i]['coords'][1]-self.G.nodes[nodo_objetivo]['coords'][1])**2)+((self.G.nodes[nodo_objetivo]['coords'][0]-self.G.nodes[i]['coords'][0])**2)),2))

        nodo_inicial = nodo_ini
        nodo_final = nodo_objetivo
        nodo_cam = self.G.nodes[nodo_inicial]
        cont=nodo_inicial
        i = 0
        path = []
        path.append(nodo_inicial)
        while cont != nodo_final:
            dist_neighbors = {}
            menor = 0
            key = 0
            hijo = 0
            for edges in self.G.edges(cont):
                hijo = edges[1]
                if (self.G.nodes[hijo]['path'] != True):
                    dist_neighbors[hijo]=distancia_nodo_objetivo[hijo]
                    if (hijo == nodo_final or distancia_nodo_objetivo[hijo] == 0 ):
                        menor = distancia_nodo_objetivo[hijo]
                        break
                    if menor == 0:
                        menor = distancia_nodo_objetivo[hijo]
                    if distancia_nodo_objetivo[hijo] < menor and distancia_nodo_objetivo[hijo] != 0 and nodo_cam['path']!= True:
                        menor = distancia_nodo_objetivo[hijo]
            key = self.get_key(menor,dist_neighbors)
            if key == "key doesn't exist":
                print ("Camino no encontrado")
                path_find = False
                break
            else:
                path_find = True
                path.append(key)
                nodo_cam['path']=True
                nodo_cam = self.G.nodes[key]
                cont=key
                self.G.nodes[nodo_inicial]['path'] = True

        self.G.nodes[nodo_final]['path'] = True
        color_map = []
        for i in range (0,n_nodos):
            if self.G.nodes[i]['path'] == True :
                color_map.append('red')
            else:
                color_map.append('green')    

        if path_find:
            #print ("Camino encontrado hill-climbing: ",path)
            pos=nx.get_node_attributes(self.G,'coords')
            plt.figure(num=None, figsize=(20, 20), dpi=80)
            plt.axis('off')
            nx.draw(self.G,pos,node_size=16, node_color = color_map)
            edges=self.G.edges()
            colors=[self.G[u][v]['color']for u,v in edges]
            nx.draw_networkx_edges(self.G,pos=self.coordinates,edge_color=colors)
            plt.tight_layout()
            plt.show()

###################################################################################################################################################
#Ciega
    def DFS(self,StartX, StartY, EndX, EndY):
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
        path = []
        nodossinhijos = []
        path.append(INICIO)
        nodossinhijos.append(INICIO)
        current = path[0]
        while current != FIN:
            vecinos = []
            for i in self.G.neighbors(current):
                if i not in path and i not in nodossinhijos:
                    vecinos.append(i)
            if len(vecinos) > 0:
                current = vecinos[0]
                path.append(current)
            else:
                nodossinhijos.append(current)
                path.pop(-1)

        returnPath = path
        returnPath.reverse()
        returner = returnPath[0]
        i = 0
        while i < len(returnPath) - 1:
            if i == 0 or i == len(returnPath) - 2:
                self.G.add_edge(returner, returnPath[i + 1], color='blue')
            else:
                self.G.add_edge(returner, returnPath[i + 1], color='red')
            returner = returnPath[i + 1]
            i = i + 1
        return len(returnPath)

def flujo_principal(valor,x,y,sx,sy,n):
    if(valor==1):
        grafo=Graph(int(n),int(n))
        nd_deleted=grafo.eliminar_nodos()
        ax=int(x)
        ay=int(y)
        se_ejecuta=True
        for i in nd_deleted:
            if nd_deleted[i][0]==ax and nd_deleted[i][1]==ay:
                window = Tk()
                window.title("Error")
                lbl=Label(window,text="El nodo final fue eliminado por favor ecoja otro :( ")
                lbl.grid(column=0,row=0)
                window.mainloop()
                se_ejecuta=False
                break
        for i in nd_deleted:
            if nd_deleted[i][0]==int(sx) and nd_deleted[i][1]==int(sy):
                window = Tk()
                window.title("Error")
                lbl=Label(window,text="El nodo inicial fue eliminado por favor ecoja otro :( ")
                lbl.grid(column=0,row=0)
                window.mainloop()
                se_ejecuta=False
                break
        if se_ejecuta:
            grafo.A_star(int(sx),int(sy),ax,ay)
            grafo.print_grafo()
    elif(valor==0):
        grafo=Graph(int(n),int(n))
        nd_deleted=grafo.eliminar_nodos()
        ax=int(x)
        ay=int(y)
        se_ejecuta=True
        for i in nd_deleted:
            if nd_deleted[i][0]==ax and nd_deleted[i][1]==ay:
                window = Tk()
                window.title("Error")
                lbl=Label(window,text="El nodo final fue eliminado por favor ecoja otro :( ")
                lbl.grid(column=0,row=0)
                window.mainloop()
                se_ejecuta=False
                break
        for i in nd_deleted:
            if nd_deleted[i][0]==int(sx) and nd_deleted[i][1]==int(sy):
                window = Tk()
                window.title("Error")
                lbl=Label(window,text="El nodo inicial fue eliminado por favor ecoja otro :( ")
                lbl.grid(column=0,row=0)
                window.mainloop()
                se_ejecuta=False
                break
        if se_ejecuta:
            grafo.DFS(int(sx),int(sy),ax,ay)
            grafo.print_grafo()
    elif(valor==2):
        grafo=Graph(int(n),int(n))
        #nd_deleted=grafo.eliminar_nodos()
        ax=int(x)
        ay=int(y)
        se_ejecuta=True
        #for i in nd_deleted:
        #    if nd_deleted[i][0]==ax and nd_deleted[i][1]==ay:
        #        window = Tk()
        #        window.title("Error")
        #        lbl=Label(window,text="El nodo final fue eliminado por favor ecoja otro :( ")
        #        lbl.grid(column=0,row=0)
        #        window.mainloop()
        #        se_ejecuta=False
        #        break
        #for i in nd_deleted:
        #    if nd_deleted[i][0]==int(sx) and nd_deleted[i][1]==int(sy):
        #        window = Tk()
        #        window.title("Error")
        #        lbl=Label(window,text="El nodo inicial fue eliminado por favor ecoja otro :( ")
        #        lbl.grid(column=0,row=0)
        #        window.mainloop()
        #        se_ejecuta=False
        #        break
        if se_ejecuta:
            coords_inicio=(int(sx),int(sy))
            coords_llegada=(ax,ay)
            ini=coords_inicio[0]*int(n)+coords_inicio[1]
            objetivo=coords_llegada[0]*int(n)+coords_llegada[1]
            aux=int(n)*int(n)
            grafo.hill_climbing(aux,ini,objetivo)
        
if __name__ == '__main__':
    root = Tk()
    root.title("Laboratorio 01")
    root.geometry("550x300")
    entry=tk.Entry(root)
    entry.insert(0,"Ingrese 'xFIN'")
    entry.place(x=350,y=50)
    entry2=tk.Entry(root)
    entry2.insert(0,"Ingrese 'yFIN'")
    entry2.place(x=350,y=75)
    
    entry3=tk.Entry(root)
    entry3.insert(0,"Ingrese 'xINICIO'")
    entry3.place(x=180,y=50)
    entry4=tk.Entry(root)
    entry4.insert(0,"Ingrese 'yINICIO'")
    entry4.place(x=180,y=75)

    entry5=tk.Entry(root)
    entry5.insert(0,"Ingrese 'n'")
    entry5.place(x=0,y=65)

    ventana=Ventana(master=root)
    entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
    entry2.bind("<FocusIn>", lambda args: entry2.delete('0', 'end'))
    entry3.bind("<FocusIn>", lambda args: entry3.delete('0', 'end'))
    entry4.bind("<FocusIn>", lambda args: entry4.delete('0', 'end'))
    entry5.bind("<FocusIn>", lambda args: entry5.delete('0', 'end'))
    ventana.mainloop()
    