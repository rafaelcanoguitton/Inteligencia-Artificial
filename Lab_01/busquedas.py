#imports
from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
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
    coordinates ={}
    size_x=100
    size_y=100
    table=np.zeros((size_x, size_y))

    def constructor_grafo_aleatorio(self):
        cont=0
        for i in range(0,self.size_x):
            for j in range(0,self.size_y):
                self.G.add_node(cont)
                self.table[i][j]=cont
                self.G.nodes[cont]['coords']=(i,j)
                self.coordinates[cont]=(i,j)
                cont+=1

    def neighbors(self, rowNumber, columnNumber, radius):
        return [[self.table[i][j] if  i >= 0 and i < len(self.table) and j >= 0 and j < len(self.table[0]) else -1
                 for j in range(columnNumber-1-radius, columnNumber+radius)]
                    for i in range(rowNumber-1-radius, rowNumber+radius)]

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
        #nx.draw(self.G,pos=self.coordinates)
        # nx.draw(self.G, node_color='#A0CBE2',edge_color='#BB0000',width=2,edge_cmap=plt.cm.Blues,with_labels=False)
        # plt.show()
        # plt.figure(figsize=(self.size_x,self.size_y))
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
    
    grafo=Graph()
    grafo.constructor_grafo_aleatorio()
    grafo.hacer_conexiones()
    grafo.eliminar_nodos()
    grafo.print_grafo()
