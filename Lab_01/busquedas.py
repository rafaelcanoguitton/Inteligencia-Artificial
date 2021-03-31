#imports
from tkinter import *
import tkinter as tk


#Clase Grafo

#class Graph(object):






def flujo_principal(valor):
    if(valor==0):
        print("Se ejecuta búsqueda a ciegas")
    elif(valor==1):
        print("Se ejecuta búsqueda heurística")
if __name__ == '__main__':
    menu_msg="" \
             "Laboratorio 01: Búsqueda a ciegas vs búsqueda Heurística"
    root = Tk()
    root.title("Laboratorio 01")
    root.geometry("500x300")

    v = tk.IntVar()
    #radioButton1 = Radiobutton(root, variable=v, value=0, text="Is calata?", command=lambda: print(v.get()))
    #radioButton2 = Radiobutton(root, variable=v, value=1, text="Is tu vieja?", command=lambda: print(v.get()))

    #radioButton1.pack()
    #radioButton2.pack()

    menu_tktext = Label(root,text=menu_msg)
    menu_tktext.pack()

    boton1 = Button(root,  text="Búsqueda ciega", command=lambda: flujo_principal(0))
    boton2 = Button(root,  text="Búsqueda heurística", command=lambda : flujo_principal(1))
    boton1.pack(side="left")
    boton2.pack(side="right")
    root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/