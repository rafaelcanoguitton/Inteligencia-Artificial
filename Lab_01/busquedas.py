#imports
from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import random

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

        self.boton1 = Button(root, text="Búsqueda ciega", command=lambda: flujo_principal(0))
        self.boton2 = Button(root, text="Búsqueda heurística", command=lambda: flujo_principal(1))
        self.boton1.pack(side="left")
        self.boton2.pack(side="right")
#Clase Grafo

class Graph():
    G = nx.Graph()
    nodos ={}
    cant_nodos= 0
    aristas=0
    #search_label=0
    size_x=0
    size_y=0
    
    #helper=0
    INICIO=0
    FIN=0

    def constructor_grafo_aleatorio(self,n):
        for i in range(0,n):
            temp_x=random.randint(0,self.size_x)
            temp_y=random.randint(0,self.size_y)
            self.nodos[i]=(temp_x,temp_y)
        self.G.add_nodes_from(self.nodos.keys())

    def constructor_grafo_cuadricula(self,n):
        for i in range(0,n):
            for j in range(0,n):
                self.nodos[j+i*n]=(j,i)
        self.G.add_nodes_from(self.nodos.keys())



def flujo_principal(valor):
    if(valor==0):
        print("Se ejecuta búsqueda a ciegas")
    elif(valor==1):
        print("Se ejecuta búsqueda heurística")
if __name__ == '__main__':
    root = Tk()
    root.title("Laboratorio 01")
    root.geometry("500x300")
    entry=tk.Entry(root)
    entry.place(x=50,y=50)
    entry2=tk.Entry(root)
    entry2.place(x=50,y=75)
    ventana=Ventana(master=root)
    ventana.mainloop()

