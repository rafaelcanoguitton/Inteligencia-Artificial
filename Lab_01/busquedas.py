#imports
from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import math
import numpy as np

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
                self.G.add_edge(k,neigh[1][1])

            if(neigh[1][2] != -1):
                self.G.add_edge(k,neigh[1][2])

            if(neigh[2][1] != -1):
                self.G.add_edge(k,neigh[2][1])

            if(neigh[1][2] != -1 and neigh[2][1] != -1):
                self.G.add_edge(neigh[1][2],neigh[2][1])

    def print_grafo(self):
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        nx.draw_networkx(self.G,pos=self.coordinates,with_labels=False,node_size=16)
        plt.show()
        
    def eliminar_nodos(self):
        #self.G.remove_node(24)
        cant_nodos=self.size_x*self.size_y
        #self.G.remove_node(random.randint(0,cant_nodos-2))
        for i in range(int(cant_nodos*0.2)):
            while(True):
                try:
                    self.G.remove_node(random.randint(0,cant_nodos-1))
                except :
                    pass
                else:
                    break

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
            print ("Camino encontrado hill-climbing: ",path)
            pos=nx.get_node_attributes(self.G,'coords')
            nx.draw(self.G,pos, node_color = color_map,with_labels=True)
            plt.show()

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
    
    coords_inicio=(3,16)
    coords_llegada=(15,2)
    ini=coords_inicio[0]*100+coords_inicio[1]
    objetivo=coords_llegada[0]*100+coords_llegada[1]
    
    grafo=Graph(100,100)
    #grafo.eliminar_nodos()
    #grafo.print_grafo()
    grafo.hill_climbing(10000,ini,objetivo)