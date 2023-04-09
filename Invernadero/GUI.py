import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sprites
import mapa
import funciones
from robot import *
import time
from functools import partial
import save

# configuracion de la ventana
ventana = tk.Tk()
ventana.title("Invernadero")
width = ventana.winfo_screenwidth()
height = ventana.winfo_screenheight() - 80
ventana.geometry("%dx%d" % (width, height))
height = int(height / 10)
pixel = height
while (pixel % 20 != 0):
    pixel -= 1
height = pixel * 10
ventana.resizable(False, False)
# aqui se crean los subventanas

tabsInvernadero = ttk.Notebook(ventana)
tab0 = ttk.Frame(tabsInvernadero)
tab1 = ttk.Frame(tabsInvernadero)
tab2 = ttk.Frame(tabsInvernadero)
tabsInvernadero.add(tab0, text='Invernadero')
tabsInvernadero.add(tab1, text='Tablas')
tabsInvernadero.add(tab2, text='¿Como funciona?')
tabsInvernadero.pack(side=tk.BOTTOM, fill="both", expand=True)
frameizquierda = tk.Frame(tab0, relief="sunken")
frameinformacion = ttk.Frame(frameizquierda)
frameizquierda.pack(side=tk.LEFT, fill='y')
framePlantaSelect = ttk.Frame(frameizquierda)
framehumedadplanta = ttk.Frame(frameinformacion)
framehumedadplanta.pack(side=tk.TOP)
frameMovimiento = ttk.Frame(frameizquierda)
lblplantaselec = tk.Label(framePlantaSelect, text='Planta seleccionada : ', fg="black", font=("Verdana", 10))
frameComofunciona = ttk.Frame(tab2)

imagen = tk.PhotoImage(file="./assets/Instrucciones.png")
ComocHacelbl = tk.Label(frameComofunciona, image=imagen).pack(fill=tk.BOTH)
frameComofunciona.pack(fill=tk.BOTH)

lblplantaselec.pack(side=tk.LEFT)

cb1 = ttk.Combobox(frameMovimiento,
                   values=("Cebolla", "Ajo", "Espinaca", "Alcachofa", "Zanahoria", "Albahaca", "Calabaza", "Remolacha"),
                   width=8,
                   state="disabled")

frameTabs = ttk.Frame(tab0)
tab_control = ttk.Notebook(frameTabs)
tab00 = ttk.Frame(tab_control)
tab01 = ttk.Frame(tab_control)
tab02 = ttk.Frame(tab_control)
tab03 = ttk.Frame(tab_control)
tab_control.add(tab00, text='Exterior')
tab_control.add(tab01, text='Piso 1')
tab_control.add(tab02, text='Piso 2')
tab_control.add(tab03, text='Piso 3')
tab_control.pack(side=tk.LEFT)

inicio = time.time()


def key(event):
    print("pressed", repr(event.char))


global mouse


def callback(event):
    botonCancelar.config(state="normal")
    RegarPlanta.config(state="normal")
    MedirHumedad.config(state="normal")
    if tab_control.tab("current", "text") == "Exterior":
        cb1.config(state="readonly")
    else:
        cb1.config(state="disabled")
    global inicio
    tiempo = time.time() - inicio
    for i in range(len(stats0)):  # reduccion de la humedad de la tierra con el paso del tiempo
        if (stats0[i] >= 0):
            stats0[i] -= 0.005 * (tiempo % 5)
        if (stats0[i] < 0):
            stats0[i] = 0

    for i in range(len(stats)):  # reduccion de la humedad de la tierra con el paso del tiempo
        if (stats[i] >= 0):
            stats[i] -= 0.005 * (tiempo % 5)
        if (stats[i] < 0):
            stats[i] = 0

    for i in range(len(stats2)):  # reduccion de la humedad de la tierra con el paso del tiempo
        if (stats2[i] >= 0):
            stats2[i] -= 0.005 * (tiempo % 5)
        if (stats2[i] < 0):
            stats2[i] = 0

    botonBlanco.config(state="normal")
    inicio += tiempo
    mouse = funciones.matriz(event.x, event.y, pixel)

    # al hacer click en el exterior
    if (mouse in numbers0 and tab_control.tab("current", "text") == "Exterior"):

        monitor2.config(text=(mouse + 200))
        monitor2.config(fg="black", font=("Verdana", 14))
        monitor3.config(text=tipo0[mouse], fg="black", font=("Verdana", 10))
        Salida1.config(text=mouse + 200, fg="black", font=("Verdana", 14))
        EliminarPlanta.config(state="normal")

    else:
        EliminarPlanta.config(state="disabled")
    if (mouse in numbers0Macetas and mouse not in numbers0 and tab_control.tab("current", "text") == "Exterior"):
        AgregarPlanta.config(state="normal")
    else:
        AgregarPlanta.config(state="disabled")
    # al hacer click en el primer piso
    if (mouse in numbers1 and tab_control.tab("current", "text") == "Piso 1"):
        monitor2.config(text=mouse, fg="black", font=("Verdana", 10))
        monitorh1.config(text=info[mouse], fg="black", font=("Verdana", 10))
        monitorh2.config(text=mouse, fg="black", font=("Verdana", 10))
        Salida1.config(text=mouse, fg="black", font=("Verdana", 10))
        monitor3.config(text=tipo[mouse], fg="black", font=("Verdana", 10))

    # al hacer click en el segundo piso
    if (mouse in numbers2 and tab_control.tab("current", "text") == "Piso 2"):
        monitor2.config(text=(mouse + 100), fg="black", font=("Verdana", 10))
        monitorh1.config(text=(info2[mouse]), fg="black", font=("Verdana", 10))
        monitorh2.config(text=mouse + 100, fg="black", font=("Verdana", 10))
        Salida1.config(text=mouse + 100, fg="black", font=("Verdana", 10))
        monitor3.config(text=tipo[mouse], fg="black", font=("Verdana", 10))

    # boton MoverPlanta
    if tab_control.tab("current", "text") == "Exterior":
        if (mouse in numbers0Macetas) and (mouse not in numbers0):
            Salida2.config(text=mouse + 200)
    if tab_control.tab("current", "text") == "Piso 1":
        if (mouse in numbers1Macetas) and (mouse not in numbers1):
            Salida2.config(text=mouse)
    if tab_control.tab("current", "text") == "Piso 2":
        if (mouse in numbers2Macetas) and (mouse not in numbers2):
            Salida2.config(text=mouse + 100)
    if (Salida1.cget("text") != "" and Salida2.cget("text") != ""):
        MoverPlanta.config(state="normal")


monitorh0 = tk.Label(framehumedadplanta, text="Humedad de la planta ", fg="black", font=("Verdana", 10))
monitorh2 = tk.Label(framehumedadplanta, text="?", fg="black", font=("Verdana", 10))
monitorh1 = tk.Label(frameinformacion, text="?", fg="black", font=("Verdana", 10))

monitorh0.pack(side=tk.LEFT)
monitorh2.pack(side=tk.LEFT)
monitorh1.pack(side=tk.TOP)
monitor1 = tk.Label(frameizquierda, text="Ninguna orden activa", fg="black", font=("Verdana", 10))
monitor2 = tk.Label(framePlantaSelect, text="?", fg="black", font=("Verdana", 10))

framesalidas = ttk.Frame(frameMovimiento)
framesalida1 = ttk.Frame(framesalidas)
framesalida2 = ttk.Frame(framesalidas)

frameTipoPlanta = ttk.Frame(framesalidas)
monitor3 = tk.Label(frameTipoPlanta, fg="black", font=("Verdana", 10))
lblTipoPlanta = tk.Label(frameTipoPlanta, text=" La planta seleccionada es", fg="black", font=("Verdana", 10))
framesalida1.pack(side=tk.TOP)
framesalida2.pack(side=tk.TOP)
lblsalida1 = tk.Label(framesalida1, text="Planta: ", fg="black", font=("Verdana", 10))
lblsalida2 = tk.Label(framesalida2, text="Maceta: ", fg="black", font=("Verdana", 10))
Salida1 = tk.Label(framesalida1, text="", font=("Verdana", 10))
Salida2 = tk.Label(framesalida2, text="", font=("Verdana", 10))

# variables:

numbers0Macetas = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

numbers1Macetas = [1, 2, 3, 4, 5, 6, 7, 8, 10, 19, 20, 22, 23, 24, 26, 27, 29, 30, 32, 37,
                   39, 40, 42, 47, 49, 50, 52, 57, 59, 60, 62, 67, 69, 70, 72, 73, 74, 75, 76, 77, 79,
                   80, 89, 91, 92, 93, 96, 97, 98]

numbers2Macetas = [23, 24, 25, 26, 32, 37, 42, 47, 52, 55, 57, 62, 67, 73, 74, 75, 76]

lblsalida1.pack(side=tk.LEFT)
Salida1.pack(side=tk.LEFT)
lblsalida2.pack(side=tk.LEFT)
Salida2.pack(side=tk.LEFT)
lblTipoPlanta.pack(side=tk.LEFT)
monitor3.pack(side=tk.LEFT)

# piso 0 en tab00
canvas0 = tk.Canvas(tab00, width=height, height=height)
canvas0.bind("<Key>", key)
canvas0.bind("<Button-1>", callback)
canvas0.pack(side=tk.LEFT)

# piso1 en tab01

canvas1 = tk.Canvas(tab01, width=height, height=height)
canvas1.bind("<Key>", key)
canvas1.bind("<Button-1>", callback)
canvas1.pack(side=tk.LEFT)

# piso2 en tab02
canvas2 = tk.Canvas(tab02, width=height, height=height)
canvas2.bind("<Key>", key)
canvas2.bind("<Button-1>", callback)
canvas2.pack(side=tk.LEFT)
# piso3 en tab03
canvas3 = tk.Canvas(tab03, width=height, height=height)
canvas3.bind("<Key>", key)
canvas3.bind("<Button-1>", callback)
canvas3.pack(side=tk.LEFT)

# colocar la matriz de fondo y microcontroller
img1 = (Image.open("./assets/matriz0.png"))
img2 = (Image.open("./assets/matriz1.png"))
img3 = (Image.open("./assets/matriz2.png"))
resized_image1 = img1.resize((height, height), Image.Resampling.LANCZOS)
resized_image2 = img2.resize((height, height), Image.Resampling.LANCZOS)
resized_image3 = img3.resize((height, height), Image.Resampling.LANCZOS)
matriz0 = ImageTk.PhotoImage(resized_image1)
matriz1 = ImageTk.PhotoImage(resized_image2)
matriz2 = ImageTk.PhotoImage(resized_image3)
canvas0.create_image(0, 0, anchor="nw", image=matriz0)
canvas1.create_image(0, 0, anchor="nw", image=matriz1)
canvas2.create_image(0, 0, anchor="nw", image=matriz2)

imgA = ImageTk.PhotoImage(Image.open("./assets/ESP32.png"))
panel4 = tk.Label(canvas3, image=imgA)
panel4.pack(side=tk.TOP)
panel4.config(width=420, height=220)

# lista que contiene los espacios de la matriz que son plantas

numbers0 = []
numbers1 = []
numbers2 = []
# dibujar el mapa
mapa0 = save.consultarDatosM(0)
x = 0
y = 0
c = 0
new_image0 = []
planta = tuple()
plantas0 = []

imagen_planta = sprites.cargarimagen(pixel, "planta")

for fila in mapa0:
    for muro in fila:
        if muro == "X":
            new_image0.append(sprites.cargarimagen(pixel, "planta"))
            id = canvas0.create_image(x, y, anchor="nw", image=new_image0[c])
            planta = funciones.matriz(x, y, pixel), id
            plantas0.append(planta)
            numbers0.append(planta[0])
        elif muro == "Y":
            new_image0.append(sprites.cargarimagen(pixel, "grifo"))
            canvas0.create_image(x, y, anchor="nw", image=new_image0[c])
        elif muro == "Z":
            new_image0.append(sprites.cargarimagen(pixel, "paredb"))
            canvas0.create_image(x, y, anchor="nw", image=new_image0[c])
        elif muro == "P":
            new_image0.append(sprites.cargarimagen(pixel, "puerta"))
            canvas0.create_image(x, y, anchor="nw", image=new_image0[c])
        else:
            new_image0.append("")
        x += pixel
        c += 1

    x = 0
    y += pixel

mapa1 = save.consultarDatosM(1)
x = 0
y = 0
c = 0
new_image1 = []
plantas = []

for fila in mapa1:
    for muro in fila:
        if muro == "X":
            new_image1.append(sprites.cargarimagen(pixel, "planta"))
            id = canvas1.create_image(x, y, anchor="nw", image=new_image1[c])
            planta = funciones.matriz(x, y, pixel), id
            plantas.append(planta)
            numbers1.append(planta[0])
        elif muro == "Y":
            new_image1.append(sprites.cargarimagen(pixel, "grifo"))
            canvas1.create_image(x, y, anchor="nw", image=new_image1[c])
        elif muro == "Z":
            new_image1.append(sprites.cargarimagen(pixel, "paredb"))
            canvas1.create_image(x, y, anchor="nw", image=new_image1[c])
        elif muro == "P":
            new_image1.append(sprites.cargarimagen(pixel, "puerta"))
            aux = canvas1.create_image(x, y, anchor="nw", image=new_image1[c])
        else:
            new_image1.append(sprites.cargarimagen(1, "transparente"))
            canvas1.create_image(0, 0, anchor="nw", image=new_image1[c])
        x += pixel
        c += 1

    x = 0
    y += pixel

mapa2 = save.consultarDatosM(2)
x = 0
y = 0
c = 0
plantas2 = []
new_image2 = []
for fila in mapa2:
    for muro in fila:
        if muro == "X":
            new_image2.append(sprites.cargarimagen(pixel, "planta"))
            id = canvas2.create_image(x, y, anchor="nw", image=new_image2[c])
            planta = funciones.matriz(x, y, pixel), id
            plantas2.append(planta)
            numbers2.append(planta[0])
        elif muro == "Y":
            new_image2.append(sprites.cargarimagen(pixel, "grifo"))
            canvas2.create_image(x, y, anchor="nw", image=new_image2[c])
        elif muro == "Z":
            new_image2.append(sprites.cargarimagen(pixel, "paredb"))
            canvas2.create_image(x, y, anchor="nw", image=new_image2[c])
        else:
            new_image2.append("")
        x += pixel
        c += 1

    x = 0
    y += pixel

tiposdeplantas = [("Cebolla", 4.52),
                  ("Ajo", 2.34),
                  ("Espinaca", 3.6),
                  ("Alcachofa", 7.3),
                  ("Zanahoria", 2.3),
                  ("Albahaca", 6.7),
                  ("Calabaza", 3.7),
                  ("Remolacha", 12.3)]

stats0 = []  # asignarle humedades a las plantas
info0 = []
tipo0 = []
humedadesperada0 = []
c = 0
for i in range(100):
    if (c < len(plantas)):
        if i in numbers0:
            stats0.append(round(random.uniform(0, 2), 3))
            info0.append("?")
            tipo_rand = (random.choice(tiposdeplantas))
            tipo0.append(tipo_rand[0])
            humedadesperada0.append(tipo_rand[1])
            c += 1
        else:
            stats0.append(-1)
            info0.append(-1)
            tipo0.append("")
            humedadesperada0.append("")
    else:
        stats0.append(-1)
        info0.append(-1)
        tipo0.append("")
        humedadesperada0.append("")

stats = []  # asignarle humedades a las plantas
info = []
tipo = []
humedadesperada = []
c = 0
for i in range(99):
    if (c < len(plantas)):
        if i in numbers1:
            temp = save.consultarDatos(i)
            stats.append(round(random.uniform(0, 2), 3))
            info.append("?")
            tipo.append(temp[2])
            humedadesperada.append(temp[1])
            c += 1
        else:
            stats.append(-1)
            info.append(-1)
            tipo.append("")
            humedadesperada.append("")
    else:
        stats.append(-1)
        info.append(-1)
        tipo.append("")
        humedadesperada.append("")

stats2 = []  # asignarle humedades a las plantas
info2 = []
tipo2 = []
humedadesperada2 = []
c = 0
for i in range(77):
    if (c < len(plantas2)):
        if i in numbers2:
            temp = save.consultarDatos2(i + 100)
            stats2.append(round(random.uniform(0, 2), 3))
            info2.append("?")
            tipo2.append(temp[2])
            humedadesperada2.append(temp[1])
            c += 1
        else:
            stats2.append(-1)
            info2.append(-1)
            tipo2.append("")
            humedadesperada2.append("")
    else:
        stats2.append(-1)
        info2.append(-1)
        tipo2.append("")
        humedadesperada2.append("")

fotorobot = []

# walle

# (x,y,piso,planta,key,entrando, destino_final,accion,quieto,id,tomar,orden)

walle = Robot(3 * pixel, 3 * pixel, 1, 1, "right", False, 0, False, 20, 0, False, 'null')
fotorobot.append(sprites.cargarimagen(pixel, "walle"))
walle.id = canvas1.create_image(walle.x, walle.y, anchor='nw', image=fotorobot[0])

# eva

eva = Robot(6 * pixel, 3 * pixel, 1, 1, "left", False, 0, False, 20, 0, False, 'null')
fotorobot.append(sprites.cargarimagen(pixel, "eva"))
eva.id = canvas1.create_image(eva.x, eva.y, anchor='nw', image=fotorobot[1])

respaldo_planta = []
pm = ""
abortar = False


# movimiento
def movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio):
    global destino_finalRespaldo
    global respaldo_planta
    global abortar
    if (robo.piso == 1):
        destino = 18
        destino1 = 88
        destino2 = 81
        destino3 = 11
    if (robo.piso == 2):
        destino = 36
        destino1 = 66
        destino2 = 63
        destino3 = 33
    if (abortar == True):
        if (robo.tomar == False or robo.tomar == "regado"):
            if (robo.tomar == False):
                robo.tomar = "regado"
            if (robo.tomar == "regado" and robo.orden == "mover"):
                robo.planta = plantainicio
        else:
            robo.destino_final = 35
            robo.tomar = "casa"

    if (robo.piso == 0):
        auxiliar = funciones.matriz(robo.x, robo.y, pixel)
        if (robo.tomar != "casa"):
            robo.destino_final = robo.planta - 10
        else:
            robo.destino_final = 35

        if auxiliar == (robo.destino_final - 200):
            # al tomar la planta
            if (robo.tomar == True):
                aux = int((robo.planta - 200) / 10)
                mapa0[aux] = funciones.reemplazar(mapa0[aux], (robo.planta - 200) % 10, robo.tomar)
                id = funciones.buscar_id(plantas0, robo.planta - 200)
                canvas0.delete(id)
                robo.tomar = "regado"
                respaldo_planta = [info0[robo.planta - 200], stats0[robo.planta - 200], tipo0[robo.planta - 200],
                                   humedadesperada0[robo.planta - 200]]
                info0[robo.planta - 200] = -1
                stats0[robo.planta - 200] = -1
                tipo0[robo.planta - 200] = ""
                humedadesperada0[robo.planta - 200] = ""
                plantas0.remove((robo.planta - 200, id))
                numbers0.remove(robo.planta - 200)
                auxpm = robo.planta
                robo.planta = pm
                pm = auxpm
                if (auxiliar == 84 or auxiliar == 85) and robo.planta < 200:
                    robo.key = "up"

                if (auxiliar < 84 and (robo.planta >= auxiliar + 210 or robo.planta < 200)):
                    robo.key = "right"

                if (auxiliar > 85 and robo.planta <= auxiliar + 210):
                    robo.key = "left"

            # al dejar la planta
            elif (robo.tomar == "regado"):

                aux = int((robo.planta - 200) / 10)
                mapa0[aux] = funciones.reemplazar(
                    mapa0[aux], (robo.planta - 200) % 10, robo.tomar)
                posicion = funciones.black_matriz(robo.planta - 200, pixel)
                id = canvas0.create_image(posicion[0], posicion[1], anchor="nw", image=imagen_planta)
                planta = (robo.planta - 200), id
                plantas0.append(planta)
                robo.destino_final = 35
                robo.tomar = "casa"
                info0[robo.planta - 200] = respaldo_planta[0]
                stats0[robo.planta - 200] = respaldo_planta[1]
                tipo0[robo.planta - 200] = respaldo_planta[2]
                humedadesperada0[robo.planta - 200] = respaldo_planta[3]
                numbers0.append(robo.planta - 200)
                if (auxiliar == 84 or auxiliar == 85):
                    robo.key = "up"

                if (auxiliar < 84):
                    robo.key = "right"

                if (auxiliar > 85):
                    robo.key = "left"

        elif (robo.destino_final > 200):
            if (auxiliar == 75 or auxiliar == 74):
                robo.key = "down"

            elif (auxiliar < robo.destino_final - 200):
                robo.key = "right"

            elif (auxiliar > robo.destino_final - 200):
                robo.key = "left"

        elif (robo.destino_final < 200):
            if (auxiliar == 84 or auxiliar == 85):
                robo.key = "up"

            elif (auxiliar < 84):
                robo.key = "right"

            elif (auxiliar > 85):
                robo.key = "left"

    if (robo.piso == 1):
        # elegir el lugar al que se dirigira el robot para llegar a la planta
        if (robo.tomar == True or robo.tomar == "regado"):
            if (robo.planta < 9):
                robo.destino_final = robo.planta + 10
            elif (robo.planta % 10 == 9):
                robo.destino_final = robo.planta - 1
            elif (robo.planta > 90):
                robo.destino_final = robo.planta - 10
            elif (robo.planta % 10 == 0):
                robo.destino_final = robo.planta + 1
            elif (robo.planta >= 22 and robo.planta <= 27):
                robo.destino_final = robo.planta - 10
            elif (robo.planta % 10 == 7 and robo.planta != 7 and robo.planta != 97):
                robo.destino_final = robo.planta + 1
            elif (robo.planta >= 72 and robo.planta <= 77):
                robo.destino_final = robo.planta + 10
            elif (robo.planta % 10 == 2 and robo.planta != 2 and robo.planta != 92):
                robo.destino_final = robo.planta - 1
            destino_finalRespaldo = robo.destino_final

        elif (robo.tomar == False and robo.orden == "regar" and robo.destino_final != 34):  # esta parte daba problemas, tener cuidado
            robo.destino_final = 35

        if funciones.matriz(robo.x, robo.y, pixel) == robo.destino_final:

            robo.quieto = 0
            aux = int(robo.planta / 10)

            # al tomar la planta
            if (robo.tomar == True and (robo.orden == "regar" or robo.orden == "mover")):
                aux = int(robo.planta / 10)
                mapa1[aux] = funciones.reemplazar(mapa1[aux], robo.planta % 10, robo.tomar)
                id = funciones.buscar_id(plantas, robo.planta)
                canvas1.delete(id)
                robo.tomar = False
                if (robo.orden == "mover"):
                    save.actualizarDatosM(1, mapa1)
                    save.actualizarDatos(robo.planta, 0, " ")
                    respaldo_planta = [info[robo.planta], stats[robo.planta], tipo[robo.planta],
                                       humedadesperada[robo.planta]]
                    info[robo.planta] = -1
                    stats[robo.planta] = -1
                    tipo[robo.planta] = ""
                    humedadesperada[robo.planta] = ""
                    plantas.remove((robo.planta, id))
                    numbers1.remove(robo.planta)
                    auxpm = robo.planta
                    robo.planta = pm
                    pm = auxpm
                    robo.tomar = "regado"



            # al dejar la planta
            elif (robo.tomar == "regado" and robo.destino_final != 35 and robo.destino_final != 34 and (
                    robo.orden == "regar" or robo.orden == "mover")):
                aux = int(robo.planta / 10)
                mapa1[aux] = funciones.reemplazar(
                    mapa1[aux], robo.planta % 10, robo.tomar)
                posicion = funciones.black_matriz(robo.planta, pixel)
                id = canvas1.create_image(posicion[0], posicion[1], anchor="nw", image=imagen_planta)
                planta = robo.planta, id
                plantas.append(planta)
                robo.destino_final = 35
                robo.tomar = "casa"
                if (robo.orden == "mover"):
                    save.actualizarDatosM(1, mapa1)
                    info[robo.planta] = respaldo_planta[0]
                    stats[robo.planta] = respaldo_planta[1]
                    tipo[robo.planta] = respaldo_planta[2]
                    humedadesperada[robo.planta] = respaldo_planta[3]
                    numbers1.append(robo.planta)
                    save.actualizarDatos(robo.planta, humedadesperada[robo.planta], tipo[robo.planta])
                    for item in TablaPiso1.get_children():
                        TablaPiso1.delete(item)
                    for i in range(100):
                        if i in numbers1:
                            TablaPiso1.insert(parent='', index='end', iid=i, text='',
                                              values=(i, info[i], humedadesperada[i], tipo[i]))
            # cuando esta en el grifo
            elif (robo.destino_final == 35 and robo.tomar != "casa" and robo.orden == "regar"):
                robo.key = "left"
                robo.destino_final = 34
            elif (robo.destino_final == 34 and robo.tomar != "casa" and robo.orden == "regar"):
                robo.entrando = False
                robo.destino_final = destino_finalRespaldo
                robo.tomar = "regado"
                stats[robo.planta] = humedadesperada[robo.planta] + 0.3
                info[robo.planta] = str(stats[robo.planta]) + " aproximadamente cuando se rego"
            for i in range(100):
                if i in numbers1:
                    TablaPiso1.delete(i)
                    TablaPiso1.insert(parent='', index='end', iid=i, text='',
                                      values=(i, info[i], humedadesperada[i], tipo[i]))
            # al medir la planta
            if (robo.orden == "medir" and robo.tomar == True):
                RegarTodo.config(state="normal")
                info[robo.planta] = stats[robo.planta]
                robo.destino_final = 35
                robo.tomar = "casa"
                for i in range(100):
                    if i in numbers1:
                        TablaPiso1.delete(i)
                        TablaPiso1.insert(parent='', index='end', iid=i, text='',
                                          values=(i, info[i], humedadesperada[i], tipo[i]))


        # walle esta saliendo, se mueve a la derecha para llegar a 35
        elif (robo.accion == True and robo.tomar != False and (
                funciones.matriz(robo.x, robo.y, pixel) == 33 or funciones.matriz(robo.x, robo.y, pixel) == 34) and (
                      robo.orden == "regar" or robo.orden == "mover")):
            robo.destino_final = 15

            robo.key = "right"

        # eva esta saliendo, se mueve a la izquierda para llegar a 35
        elif (robo.accion == True and robo.tomar == True and funciones.matriz(robo.x, robo.y,
                                                                              pixel) == 36 and robo.orden == "medir"):
            robo.destino_final = 15

            robo.key = "left"


        # robo sale subiendo hacia 15
        elif (robo.entrando == False and funciones.traducir(robo.x, pixel) == 5 and funciones.traducir(robo.y,
                                                                     pixel) > 1 and funciones.matriz(
                robo.x, robo.y, pixel) != 85):

            robo.key = "up"

        # robo entra a la base hacia 35
        elif ((robo.destino_final == 35 or (
                robo.destino_final > 100 and robo.destino_final < 200)) and funciones.traducir(robo.x,
                                                        pixel) == 5 and funciones.matriz(
                robo.x, robo.y, pixel) != 85 and funciones.matriz(robo.x, robo.y, pixel) != 45):

            robo.key = "down"
            robo.entrando = True

        # movimiento en sentido horario
        elif ((robo.orden == "regar") == (robo.tomar == "regado")) and (robo.planta > 200) or (
                ((robo.planta % 10 >= 5) and (robo.tomar == "regado" or robo.tomar == True)) or (
                (robo.planta % 10 < 5) and (robo.tomar == False or robo.tomar == "casa"))):

            # robo esta en la fila 2, se mueve a la derecha
            if (funciones.traducir(robo.x, pixel) < destino % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino / 10)):

                robo.key = "right"

            # robo esta en la columna 8, se mueve hacia abajo
            elif (funciones.traducir(robo.x, pixel) == destino1 % 10 and funciones.traducir(robo.y, pixel) < int(
                    destino1 / 10)):

                robo.key = "down"

            # robo esta en la fila 8, se mueve hacia la izquierda
            elif (funciones.traducir(robo.x, pixel) > destino2 % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino2 / 10)):

                robo.key = "left"

            # robo esta en la columna 2, se mueve hacia arriba
            elif (funciones.traducir(robo.x, pixel) == destino3 % 10 and funciones.traducir(robo.y, pixel) > int(
                    destino3 / 10)):

                robo.key = "up"

        # movimiento en sentido antihorario
        elif (((robo.planta % 10 < 5) and (robo.tomar == "regado" or robo.tomar == True)) or (
                (robo.planta % 10 >= 5) and (robo.tomar == False or robo.tomar == "casa"))):
            # robo esta en la fila 2, se mueve a la izquierda
            if (funciones.traducir(robo.x, pixel) < destino % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino / 10)):

                robo.key = "left"

            # robo esta en la columna 8, se mueve hacia arriba
            elif (funciones.traducir(robo.x, pixel) == destino1 % 10 and funciones.traducir(robo.y, pixel) < int(
                    destino1 / 10)):

                robo.key = "up"

            # robo esta en la fila 8, se mueve hacia la derecha
            elif (funciones.traducir(robo.x, pixel) > destino2 % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino2 / 10)):

                robo.key = "right"

            # robo esta en la columna 2, se mueve hacia abajo
            elif (funciones.traducir(robo.x, pixel) == destino3 % 10 and funciones.traducir(robo.y, pixel) > int(
                    destino3 / 10)):

                robo.key = "down"

            if (funciones.matriz(robo.x, robo.y, pixel) == destino3):
                robo.key = "down"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino2):
                robo.key = "right"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino1):
                robo.key = "up"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino):
                robo.key = "left"

        # walle esta entrando por la puerta
        if (funciones.matriz(robo.x, robo.y, pixel) == 94 or funciones.matriz(robo.x, robo.y,
                                                                              pixel) == 95) and robo.key != "down":
            robo.key = "up"

        if (robo.orden == "regar" or robo.orden == "mover"):
            # walle se mueve desde 35 a 33
            if (robo.tomar == "casa" and (
                    funciones.matriz(robo.x, robo.y, pixel) == 35 or funciones.matriz(robo.x, robo.y, pixel) == 34)):
                robo.destino_final = 33
                robo.quieto = 23
                robo.key = "left"

            # walle termina su accion
            if (robo.tomar == "casa" and funciones.matriz(robo.x, robo.y, pixel) == 33):
                robo.accion = False

        if (robo.orden == "medir"):
            # eva se mueve de 35 a 36
            if (robo.tomar == "casa" and funciones.matriz(robo.x, robo.y, pixel) == 35):
                robo.destio_final = 36
                robo.quieto = 23
                robo.key = "right"

            # eva termina su accion
            if (robo.tomar == "casa" and funciones.matriz(robo.x, robo.y, pixel) == 36):
                robo.accion = False

        # robo entra al elevador
        if (robo.planta > 100 and robo.planta < 200 and robo.tomar == True):
            if (funciones.matriz(robo.x, robo.y, pixel) == 33 or funciones.matriz(robo.x, robo.y, pixel) == 34):
                robo.key = "right"
            if (funciones.matriz(robo.x, robo.y, pixel) == 35):
                robo.key = "down"

        # walle sale de la piramide
        if (robo.orden == "mover" and (funciones.matriz(robo.x, robo.y, pixel) == 84 or funciones.matriz(robo.x, robo.y,
                                                                          pixel) == 85) and robo.destino_final > 200):
            robo.key = "down"

    if (robo.piso == 2):
        # elegir el lugar al que se dirigira el robot para llegar a la planta
        if (robo.tomar == True or robo.tomar == "regado"):
            if (robo.planta < 128):
                robo.destino_final = robo.planta + 10
            elif (robo.planta % 10 == 7):
                robo.destino_final = robo.planta - 1
            elif (robo.planta > 172):
                robo.destino_final = robo.planta - 10
            elif (robo.planta % 10 == 2):
                robo.destino_final = robo.planta + 1
        elif (robo.tomar == False and robo.orden == "regar"):
            robo.destino_final = 154

        if funciones.matriz(robo.x, robo.y, pixel) == (robo.destino_final - 100):

            robo.quieto = 0
            aux = int((robo.planta - 100) / 10)

            # al tomar la planta
            if (robo.tomar == True and (robo.orden == "regar" or robo.orden == "mover")):
                aux = int((robo.planta - 100) / 10)
                mapa2[aux] = funciones.reemplazar(mapa2[aux], (robo.planta - 100) % 10, robo.tomar)
                id = funciones.buscar_id(plantas2, robo.planta - 100)
                canvas2.delete(id)
                robo.tomar = False
                if (robo.orden == "mover"):
                    save.actualizarDatosM(2, mapa2)
                    save.actualizarDatos2(robo.planta, 0, " ")
                    respaldo_planta = [info2[robo.planta - 100], stats2[robo.planta - 100], tipo2[robo.planta - 100],
                                       humedadesperada2[robo.planta - 100]]
                    info2[robo.planta - 100] = -1
                    stats2[robo.planta - 100] = -1
                    tipo2[robo.planta - 100] = ""
                    humedadesperada2[robo.planta - 100] = ""
                    plantas2.remove((robo.planta - 100, id))
                    numbers2.remove(robo.planta - 100)
                    auxpm = robo.planta
                    robo.planta = pm
                    pm = auxpm
                    robo.tomar = "regado"




            # al dejar la planta
            elif (robo.tomar == "regado" and robo.destino_final != 154 and (
                    robo.orden == "regar" or robo.orden == "mover")):
                aux = int((robo.planta - 100) / 10)
                mapa2[aux] = funciones.reemplazar(
                    mapa2[aux], (robo.planta - 100) % 10, robo.tomar)
                posicion = funciones.black_matriz(robo.planta - 100, pixel)
                id = canvas2.create_image(posicion[0], posicion[1], anchor="nw", image=imagen_planta)
                planta = (robo.planta - 100), id
                plantas2.append(planta)
                robo.destino_final = 35
                robo.tomar = "casa"
                if (robo.orden == "mover"):
                    save.actualizarDatosM(2, mapa2)
                    info2[robo.planta - 100] = respaldo_planta[0]
                    stats2[robo.planta - 100] = respaldo_planta[1]
                    tipo2[robo.planta - 100] = respaldo_planta[2]
                    humedadesperada2[robo.planta - 100] = respaldo_planta[3]
                    numbers2.append(robo.planta - 100)
                    save.actualizarDatos2(robo.planta, humedadesperada2[robo.planta - 100], tipo2[robo.planta - 100])
                    for item in TablaPiso2.get_children():
                        TablaPiso2.delete(item)
                    for i in range(100):
                        if i in numbers2:
                            TablaPiso2.insert(parent='', index='end', iid=i, text='',
                                              values=(i + 100, info2[i], humedadesperada2[i], tipo2[i]))

            # cuando esta en el grifo
            elif (robo.destino_final == 154 and robo.tomar != "casa" and robo.orden == "regar"):
                robo.entrando = False
                robo.destino_final = destino_finalRespaldo
                robo.tomar = "regado"
                stats2[robo.planta - 100] = humedadesperada2[robo.planta - 100] + 2
                info2[robo.planta - 100] = str(stats2[robo.planta - 100]) + " aproximadamente"
                if (robo.planta > 160):
                    robo.key = "down"
                elif ((robo.planta - 100) % 10 < 5):
                    robo.key = "left"
                elif ((robo.planta - 100) % 10 >= 5):
                    robo.key = "right"
                for i in range(100):
                    if i in numbers2:
                        TablaPiso2.delete(i)
                        TablaPiso2.insert(parent='', index='end', iid=i, text='',
                                          values=(i + 100, info2[i], humedadesperada2[i], tipo2[i]))
            # al medir la planta
            if (robo.orden == "medir" and robo.tomar == True):
                RegarTodo.config(state="normal")
                info2[robo.planta - 100] = stats2[robo.planta - 100]
                robo.destino_final = 35
                robo.tomar = "casa"
                for i in range(100):
                    if i in numbers2:
                        TablaPiso2.delete(i)
                        TablaPiso2.insert(parent='', index='end', iid=i, text='',
                                          values=(i + 100, info2[i], humedadesperada2[i], tipo2[i]))


        # robo entra hacia el elevador
        elif ((robo.destino_final > 200 or robo.destino_final < 100) and funciones.traducir(robo.x,
                                                                    pixel) == 5 and funciones.matriz(
                robo.x, robo.y, pixel) != 35):

            robo.key = "up"
            robo.entrando = True


        elif (robo.destino_final == 154 and funciones.matriz(robo.x, robo.y, pixel) == 64):
            robo.key = "up"

        # sentido antihorario
        elif (((robo.planta % 10 >= 5) and (robo.tomar == "regado" or robo.tomar == True)) or (
                (robo.planta % 10 < 5) and (robo.tomar == False or robo.tomar == "casa"))):
            # robo esta en la fila 2, se mueve a la izquierda
            if (funciones.traducir(robo.x, pixel) < destino % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino / 10)):
                robo.key = "left"

            # robo esta en la columna 8, se mueve hacia arriba
            elif (funciones.traducir(robo.x, pixel) == destino1 % 10 and funciones.traducir(robo.y, pixel) < int(
                    destino1 / 10)):

                robo.key = "up"

            # robo esta en la fila 8, se mueve hacia la derecha
            elif (funciones.traducir(robo.x, pixel) > destino2 % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino2 / 10)):

                robo.key = "right"

            # robo esta en la columna 2, se mueve hacia abajo
            elif (funciones.traducir(robo.x, pixel) == destino3 % 10 and funciones.traducir(robo.y, pixel) > int(
                    destino3 / 10)):
                robo.key = "down"

            if (funciones.matriz(robo.x, robo.y, pixel) == destino3):
                robo.key = "down"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino2):
                robo.key = "right"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino1):
                robo.key = "up"
            if (funciones.matriz(robo.x, robo.y, pixel) == destino):
                robo.key = "left"

        # sentido horario
        elif (((robo.planta % 10 < 5) and (robo.tomar == "regado" or robo.tomar == True)) or (
                (robo.planta % 10 >= 5) and (robo.tomar == False or robo.tomar == "casa"))):

            # robo esta en la fila 2, se mueve a la derecha
            if (funciones.traducir(robo.x, pixel) < destino % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino / 10)):

                robo.key = "right"

            # robo esta en la columna 8, se mueve hacia abajo
            elif (funciones.traducir(robo.x, pixel) == destino1 % 10 and funciones.traducir(robo.y, pixel) < int(
                    destino1 / 10)):

                robo.key = "down"

            # robo esta en la fila 8, se mueve hacia la izquierda
            elif (funciones.traducir(robo.x, pixel) > destino2 % 10 and funciones.traducir(robo.y, pixel) == int(
                    destino2 / 10)):

                robo.key = "left"

            # robo esta en la columna 2, se mueve hacia arriba
            elif (funciones.traducir(robo.x, pixel) == destino3 % 10 and funciones.traducir(robo.y, pixel) > int(
                    destino3 / 10)):

                robo.key = "up"

    # ajustar imagenes por el movimiento
    robo.quieto += 1
    if (robo.quieto > 20 and robo.accion == True):
        if (robo.orden == "regar" or robo.orden == "mover"):  # movimieto de walle
            if robo.key == "left":
                robo.x += -pixel
                walle = robo
                izquierda(walle)
                robo = walle
            elif robo.key == "right":
                robo.x += pixel
                walle = robo
                derecha(walle)
                robo = walle
            elif robo.key == "up":
                robo.y += -pixel
                walle = robo
                arriba(walle)
                robo = walle
            elif robo.key == "down":
                robo.y += pixel
                walle = robo
                abajo(walle)
                robo = walle
        elif (robo.orden == "medir"):  # movimiento de eva
            if robo.key == "left":
                robo.x += -pixel
                eva = robo
                izquierda(eva)
                robo = eva
            elif robo.key == "right":
                robo.x += pixel
                eva = robo
                derecha(eva)
                robo = eva
            elif robo.key == "up":
                robo.y += -pixel
                eva = robo
                arriba(eva)
                robo = eva
            elif robo.key == "down":
                robo.y += pixel
                eva = robo
                abajo(eva)
                robo = eva

    if (robo.piso == 0):
        # walle entra a la piramide
        if (robo.destino_final < 200 and (
                funciones.matriz(robo.x, robo.y, pixel) == 74 or funciones.matriz(robo.x, robo.y, pixel) == 75)):
            canvas0.delete(robo.id)
            robo.id = canvas1.create_image(robo.x, robo.y + (2 * pixel), anchor="nw", image=fotorobot[0])
            robo.piso = 1
            robo.key = "up"
            robo.y += 2 * pixel

    if (robo.piso == 1):
        # el robot cambia de piso

        if (funciones.matriz(robo.x, robo.y, pixel) == 45 and robo.destino_final > 100):
            canvas1.delete(robo.id)
            if (robo.orden == "medir"):
                robo.id = canvas2.create_image(robo.x, robo.y, anchor='nw', image=fotorobot[1])
            else:
                robo.id = canvas2.create_image(robo.x, robo.y, anchor='nw', image=fotorobot[0])
            robo.piso = 2
            robo.key = "down"

        # walle sale de la piramide
        if ((robo.planta > 200 and robo.tomar != "casa") and (
                funciones.matriz(robo.x, robo.y, pixel) == 94 or funciones.matriz(robo.x, robo.y, pixel) == 95)):
            canvas1.delete(robo.id)
            robo.id = canvas0.create_image(robo.x, robo.y - (2 * pixel), anchor='nw', image=fotorobot[0])
            robo.piso = 0
            robo.key = "down"
            robo.y -= 2 * pixel
    elif (robo.piso == 2):
        # robo baja al primer piso
        if (funciones.matriz(robo.x, robo.y, pixel) == 45 and (robo.destino_final < 100 or robo.destino_final > 200)):
            canvas2.delete(robo.id)
            if (robo.orden == "medir"):
                robo.id = canvas1.create_image(robo.x, robo.y, anchor='nw', image=fotorobot[1])
            else:
                robo.id = canvas1.create_image(robo.x, robo.y, anchor='nw', image=fotorobot[0])
            robo.piso = 1
            robo.key = "up"

    return robo


# movimiento de la imagen del robot a la izquierda
def izquierda(robo):
    if (robo.piso == 0):
        canvas0.move(robo.id, -20, 0)
        ventana.update()
        coords = canvas0.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas0.after(200, izquierda(robo))
    if (robo.piso == 1):
        canvas1.move(robo.id, -20, 0)
        ventana.update()
        coords = canvas1.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas1.after(200, izquierda(robo))
    if (robo.piso == 2):
        canvas2.move(robo.id, -20, 0)
        ventana.update()
        coords = canvas2.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas2.after(200, izquierda(robo))


# movimiento de la imagen del robot a la derecha
def derecha(robo):
    if (robo.piso == 0):
        canvas0.move(robo.id, 20, 0)
        ventana.update()
        coords = canvas0.coords(robo.id)
        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas0.after(200, derecha(robo))
    if (robo.piso == 1):
        canvas1.move(robo.id, 20, 0)
        ventana.update()
        coords = canvas1.coords(robo.id)
        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas1.after(200, derecha(robo))
    if (robo.piso == 2):
        canvas2.move(robo.id, 20, 0)
        ventana.update()
        coords = canvas2.coords(robo.id)
        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas2.after(200, derecha(robo))


# movimiento de la imagen del robot hacia arriba
def arriba(robo):
    if (robo.piso == 0):
        canvas0.move(robo.id, 0, -20)
        ventana.update()
        coords = canvas0.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas0.after(200, arriba(robo))
    if (robo.piso == 1):
        canvas1.move(robo.id, 0, -20)
        ventana.update()
        coords = canvas1.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas1.after(200, arriba(robo))
    if (robo.piso == 2):
        canvas2.move(robo.id, 0, -20)
        ventana.update()
        coords = canvas2.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas2.after(200, arriba(robo))


# movimiento de la imagen del robot hacia abajo
def abajo(robo):
    if (robo.piso == 0):
        canvas0.move(robo.id, 0, 20)
        ventana.update()
        coords = canvas0.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas0.after(200, abajo(robo))
    if (robo.piso == 1):
        canvas1.move(robo.id, 0, 20)
        ventana.update()
        coords = canvas1.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas1.after(200, abajo(robo))
    if (robo.piso == 2):
        canvas2.move(robo.id, 0, 20)
        ventana.update()
        coords = canvas2.coords(robo.id)

        if (funciones.exactitud(coords[0], coords[1], pixel) == False):
            canvas2.after(200, abajo(robo))


def clear():
    Salida1.config(text="")
    Salida2.config(text="")
    cb1.config(state="disabled")
    botonCancelar.config(state="disabled")
    RegarPlanta.config(state="disabled")
    MoverPlanta.config(state="disabled")
    MedirHumedad.config(state="disabled")
    AgregarPlanta.config(state="disabled")
    EliminarPlanta.config(state="disabled")


# Define los parametros de movimiento
def Orden(mapa0, mapa1, mapa2, walle, eva, pm):
    botonABORTAR.config(state="normal")
    Salida1.config(text="")
    Salida2.config(text="")
    text = listbox.get(0)
    plantainicio = 0
    control = False
    if (text[0:5] == "Regar" and text != "Regar plantas con humedad baja"):
        walle.orden = "regar"
        robo = walle
        robo.planta = int(text[6:9])
    if text == "Regar plantas con humedad baja":
        for i in numbers1:
            if (info[i] != "?"):
                aux = str(info[i])
                aux = aux[:4]
                aux = float(aux)
                if (aux < humedadesperada[i]):
                    control = True
                    walle.orden = "regar"
                    robo = walle
                    robo.planta = i
                    monitor1.config(text="regando planta " + str(robo.planta))
                    robo.accion = True
                    robo.tomar = True
                    robo.entrando = False

                    while (walle.accion == True):
                        walle = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                        robo = walle
                    walle.orden = 'null'

        for i in numbers2:
            if (info2[i] != "?"):
                aux = str(info2[i])
                aux = aux[:4]
                aux = float(aux)
                if (aux < humedadesperada2[i]):
                    control = True
                    walle.orden = "regar"
                    robo = walle
                    robo.planta = i + 100
                    monitor1.config(text="regando planta " + str(robo.planta))
                    robo.accion = True
                    robo.tomar = True
                    robo.entrando = False
                    while (walle.accion == True):
                        walle = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                        robo = walle
                    walle.orden = 'null'
        if (control == False):
            robo = walle
            messagebox.showinfo("Message", "ninguna planta con humedad conocida necesita regarse")
            robo.orden = "null"
        control = False
    elif (text[0:5] == "Mover"):
        walle.orden = "mover"
        robo = walle
        plantainicio = ""
        control = True
        for i in range(5, len(text)):
            if text[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if (control == True):
                    plantainicio = plantainicio + text[i]
                else:
                    pm = str(pm) + text[i]
            if (text[i] == "a"):
                control = False
        plantainicio = int(plantainicio)
        pm = int(pm)
        robo.planta = plantainicio


    elif (text[0:5] == "Medir" and text != "Medir humedad de todo"):
        eva.orden = "medir"
        robo = eva
        robo.planta = int(text[14:17])

    if text == "Medir humedad de todo":
        if (plantas or plantas2):
            for i in numbers1:
                eva.orden = "medir"
                robo = eva
                robo.planta = i
                monitor1.config(text="midiendo humedad de " + str(robo.planta))
                robo.accion = True
                robo.tomar = True
                robo.entrando = False

                while (eva.accion == True):
                    eva = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                    robo = eva
                eva.orden = 'null'

            for i in numbers2:
                eva.orden = "medir"
                robo = eva
                robo.planta = i + 100
                monitor1.config(text="midiendo humedad de " + str(robo.planta))
                robo.accion = True
                robo.tomar = True
                robo.entrando = False
                while (eva.accion == True):
                    eva = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                    robo = eva
                eva.orden = 'null'
        else:
            messagebox.showinfo("Message", "No hay plantas en el invernadero")
            listbox.delete(0)
            robo = eva
            robo.orden = "null"

    # evitar que se haga una accion con una planta que ya no esta
    plantaerror = False
    if (robo.orden == "mover"):
        if (robo.planta < 100 and (robo.planta not in numbers1 or pm in numbers1)):
            plantaerror = True
        if (robo.planta > 100 and robo.planta < 200 and (
                (robo.planta - 100) not in numbers2 or (pm - 100) in numbers2)):
            plantaerror = True
        if (robo.planta > 200 and ((robo.planta - 200) not in numbers0) or (pm - 200) in numbers0):
            plantaerror = True
    else:
        if (robo.planta < 100 and robo.planta not in numbers1):
            plantaerror = True
        if (robo.planta > 100 and robo.planta < 200 and (robo.planta - 100) not in numbers2):
            plantaerror = True
        if (robo.planta > 200 and (robo.planta - 200) not in numbers0):
            plantaerror = True

    if (plantaerror == False and text != "Medir humedad de todo" and text != "Regar plantas con humedad baja"):
        monitor1.config(text=listbox.get(0))
        # definir que robot se va a mover
        robo.accion = True
        robo.tomar = True
        robo.entrando = False
        monitor2.configure(text="")

        while (walle.accion == True or eva.accion == True):
            if (eva.orden == 'null'):
                walle = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                robo = walle
            else:
                eva = movimiento(mapa0, mapa1, mapa2, robo, pm, plantainicio)
                robo = eva
        walle.orden = 'null'
        eva.orden = 'null'
        pm = ""
        listbox.delete(0)
        monitor1.config(text="")
        global abortar
        if not listbox.get(0):
            AgregarPlanta.config(state="disabled")
            EliminarPlanta.config(state="disabled")
            monitor1.config(text="Ninguna orden activa")
            botonABORTAR.config(state="disabled")
            abortar = False
        else:
            monitor1.config(text=listbox.get(0))
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)

    elif (text != "Medir humedad de todo" and text != "Regar plantas con humedad baja"):
        messagebox.showinfo("Message", 'La operacion: "' + listbox.get(
            0) + '" no pudo ser completada, ya que anteriormente se realizo un movimiento que lo impide')
        listbox.delete(0)
        walle.orden = 'null'
        eva.orden = 'null'
        pm = ""
        if not listbox.get(0):
            AgregarPlanta.config(state="disabled")
            EliminarPlanta.config(state="disabled")
            monitor1.config(text="Ninguna orden activa")
            botonABORTAR.config(state="disabled")
            abortar = False
        else:
            monitor1.config(text=listbox.get(0))
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)

    if (text == "Medir humedad de todo" or text == "Regar plantas con humedad baja"):
        listbox.delete(0)
        if not listbox.get(0):
            monitor1.config(text="Ninguna orden activa")
            botonABORTAR.config(state="disabled")
            abortar = False
        else:
            monitor1.config(text=listbox.get(0))
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)

# funciones para botones y botones


# funcionesBotones
def Subir():
    idxs = listbox.curselection()
    if (str(idxs) != "(1,)"):
        for pos in idxs:
            if pos == 0:
                continue
            listbox.selection_clear(0, tk.END)
            text = listbox.get(pos)
            listbox.delete(pos)
            listbox.insert(pos - 1, text)
            listbox.selection_set(pos - 1)


def Bajar():
    idxs = listbox.curselection()
    if (str(idxs) != "(0,)"):
        for pos in idxs:
            text = listbox.get(pos)
            listbox.delete(pos)
            listbox.insert(pos + 1, text)
            listbox.selection_set(pos + 1)


def borrarelemento():
    for i in listbox.curselection():
        listbox.delete(i)


def updatecanvas3():
    progress['value'] += 20
    canvas3.update_idletasks()
    if progress['value'] <= 100:
        canvas3.after(400, updatecanvas3)


def open():
    progress['value'] = 20
    canvas3.update_idletasks()
    canvas3.after(400, updatecanvas3)
    posMalla = "Estado actual de la Malla = abierto       "
    labelmalla.config(text=posMalla)


def mid():
    progress['value'] = 20
    canvas3.update_idletasks()
    canvas3.after(400, updatecanvas3)
    posMalla = "Estado actual de la Malla = intermedio"
    labelmalla.config(text=posMalla)


def closed():
    progress['value'] = 20
    canvas3.update_idletasks()
    canvas3.after(400, updatecanvas3)
    posMalla = "Estado actual de la Malla = cerrado      "
    labelmalla.config(text=posMalla)


def switch1():
    global is_on1
    # Determin is on or off
    if is_on1:
        on_button1.config(image=off)
        is_on1 = False
    else:
        on_button1.config(image=on)
        is_on1 = True


def switch2():
    global is_on2
    # Determin is on or off
    if is_on2:
        on_button2.config(image=off)
        is_on2 = False
    else:
        on_button2.config(image=on)
        is_on2 = True


def switch3():
    global is_on3
    # Determin is on or off
    if is_on3:
        on_button3.config(image=off)
        is_on3 = False
    else:
        on_button3.config(image=on)
        is_on3 = True


def switch4():
    global is_on4
    # Determin is on or off
    if is_on4:
        on_button4.config(image=off)
        is_on4 = False
    else:
        on_button4.config(image=on)
        is_on4 = True


is_on1 = True
is_on2 = True
is_on3 = True
is_on4 = True


def Regar_planta(mapa0, mapa1, mapa2, walle, eva, pm):
    if (monitor2.cget("text") != ""):
        aux = int(monitor2.cget("text"))
        if ((aux < 100 and info[aux] != "?") or ((aux > 100 and aux < 200) and info2[aux - 100] != "?")):
            texto = "Regar "
            texto = texto + str(monitor2.cget("text"))
            listbox.insert(tk.END, texto)
            clear()
            if not listbox.get(1):
                Orden(mapa0, mapa1, mapa2, walle, eva, pm)
        else:
            if (aux > 200):
                messagebox.showinfo("Message", "Operacion no valida fuera del invernadero")
            else:
                messagebox.showinfo("Message",
                                    "Humedad de la planta desconocida, se recomienda medir la humedad primero")


def Mover_planta(mapa0, mapa1, mapa2, walle, eva, pm):
    global posrecogida
    global posentrega
    posrecogida = str(Salida1.cget("text"))
    posentrega = str(Salida2.cget("text"))
    mover = "Mover "
    a = " a "
    texto = (mover + posrecogida + a + posentrega)
    listbox.insert(tk.END, texto)
    clear()
    if not listbox.get(1):
        Orden(mapa0, mapa1, mapa2, walle, eva, pm)


def Medir_humedad(mapa0, mapa1, mapa2, walle, eva, pm):
    if (monitor2.cget("text") != ""):
        aux = int(monitor2.cget("text"))
        if (aux < 200):
            texto = "Medir Humedad "
            texto = texto + str(monitor2.cget("text"))
            listbox.insert(tk.END, texto)
            clear()
            if not listbox.get(1):
                Orden(mapa0, mapa1, mapa2, walle, eva, pm)
        else:
            messagebox.showinfo("Message", "Operacion no valida fuera del invernadero")


advertencia = True


def Medir_all(mapa0, mapa1, mapa2, walle, eva, pm):
    clear()
    global advertencia
    if advertencia == False:
        texto = "Medir humedad de todo"
        listbox.insert(tk.END, texto)
        if not listbox.get(1):
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)
    if advertencia == True:
        messagebox.showinfo("Message",
                            "Esta orden tardara un tiempo elevado, dependiendo de la cantidad de plantas puede ser de hasta 9 minutos, en caso de querer continuar de todas formas vuelva a seleccionar esta opcion")
        advertencia = False


advertencia2 = True


def Regar_all(mapa0, mapa1, mapa2, walle, eva, pm):
    clear()
    global advertencia2
    if advertencia2 == False:
        texto = "Regar plantas con humedad baja"
        listbox.insert(tk.END, texto)
        if not listbox.get(1):
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)
    if advertencia2 == True:
        messagebox.showinfo("Message",
                            "Esta orden puede tardar, en caso de querer continuar de todas formas vuelva a seleccionar esta opcion")
        advertencia2 = False


# tiposdeplantas = [("Cebolla",4.52),
#                   ("Ajo",2.34),
#                   ("Espinaca",3.6),
#                   ("Alcachofa",7.3),
#                   ("Zanahoria",2.3),
#                   ("Albahaca",6.7),
#                   ("Calabaza",3.7) ,
#                   ("Remolacha",12.3)]

def Agregar_planta():
    if (not listbox.get(0)):
        nueva = 0

        if (cb1.get() == ""):
            messagebox.showinfo("Message", "Debe de seleccionar el tipo de planta")

        else:
            nueva = int(Salida2.cget("text")) - 200
            posicion = funciones.black_matriz(nueva, pixel)
            id = canvas0.create_image(posicion[0], posicion[1], anchor="nw", image=imagen_planta)
            planta = nueva, id
            plantas0.append(planta)
            info0[nueva] = "?"
            tipo0[nueva] = cb1.get()  # cambiar, se debe poner manualmente
            stats0[nueva] = round(random.uniform(0, 2), 3)
            if (cb1.get() == "Cebolla"):
                humedadesperada0[nueva] = 4.52
            elif (cb1.get() == "Ajo"):
                humedadesperada0[nueva] = 2.34
            elif (cb1.get() == "Espinaca"):
                humedadesperada0[nueva] = 3.6
            elif (cb1.get() == "Alcachofa"):
                humedadesperada0[nueva] = 7.3
            elif (cb1.get() == "Zanahoria"):
                humedadesperada0[nueva] = 2.3
            elif (cb1.get() == "Albahaca"):
                humedadesperada0[nueva] = 6.7
            elif (cb1.get() == "Calabaza"):
                humedadesperada0[nueva] = 3.7
            elif (cb1.get() == "Remolacha"):
                humedadesperada0[nueva] = 12.3

        numbers0.append(nueva)
        AgregarPlanta.config(state="disabled")
        clear()

    else:
        messagebox.showinfo("Message", "espere a que los robots terminen sus funciones")


def Eliminar_planta():
    if (not listbox.get(0)):
        vieja = int(Salida1.cget("text")) - 200
        id = funciones.buscar_id(plantas0, vieja)
        canvas0.delete(id)
        info0[vieja] = -1
        stats0[vieja] = -1
        tipo0[vieja] = ""
        humedadesperada0[vieja] = ""
        plantas0.remove((vieja, id))
        numbers0.remove(vieja)
        EliminarPlanta.config(state="disabled")
        clear()
    else:
        messagebox.showinfo("Message", "espere a que los robots terminen sus funciones")


def abort():
    global abortar
    abortar = True


# FramesVentana
framegeneral = ttk.Frame(frameizquierda)
framelisybotones = ttk.Frame(framegeneral)
frameListbox = ttk.Frame(framelisybotones)
frameminimover = ttk.Frame(frameMovimiento)
frameminiagregar = ttk.Frame(frameMovimiento)
frameWalle = ttk.Frame(framegeneral)
frameEva = ttk.Frame(framegeneral)
framecalefactor = ttk.Frame(canvas3)
frameinvernadero = ttk.Frame(canvas3)

# Lista de Instrcciones robots
listbox = tk.Listbox()
scrollbar = ttk.Scrollbar(frameListbox, orient=tk.VERTICAL)
listbox = tk.Listbox(frameListbox, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

# imagenesBotones

on = tk.PhotoImage(file="./assets/on.png")
off = tk.PhotoImage(file="./assets/off.png")

framelbls = ttk.Frame(framecalefactor)
framebtns = ttk.Frame(framecalefactor)


def PruebaMov(mapa0, mapa1, mapa2, walle, eva, pm):
    if (not listbox.get(0)):
        global abortar
        listbox.insert(tk.END, "prueba de movimiento")
        robo = walle
        robo.orden = "regar"
        robo.accion = True
        robo.tomar = True
        robo.entrando = False
        robo.planta = 92

        while (walle.accion == True):

            walle = movimiento(mapa0, mapa1, mapa2, robo, 1, 1)
            robo = walle
            if (funciones.matriz(robo.x, robo.y, pixel) == 51):
                abortar = True
        walle.orden = 'null'
        abortar = False

        robo = eva
        robo.orden = "medir"
        robo.accion = True
        robo.tomar = True
        robo.entrando = False
        robo.planta = 92

        while (eva.accion == True):

            eva = movimiento(mapa0, mapa1, mapa2, robo, 1, 1)
            robo = eva
            if (funciones.matriz(robo.x, robo.y, pixel) == 51):
                abortar = True
        eva.orden = 'null'
        abortar = False
        listbox.delete(0)
        if (listbox.get(0)):
            monitor1.config(text=listbox.get(0))
            Orden(mapa0, mapa1, mapa2, walle, eva, pm)
    else:
        messagebox.showinfo("Message",
                            'esta operacion solo se puede realizar si los robots no estan ejecutando otra orden')


# botones
probarR = tk.Button(framecalefactor, text="probar movimiento robots",
                    command=partial(PruebaMov, mapa0, mapa1, mapa2, walle, eva, pm))
probarR.pack(side=tk.BOTTOM)
moveUpButton = tk.Button(framelisybotones, text="subir", command=Subir)
movedownButton = tk.Button(framelisybotones, text="Bajar", command=Bajar)
BorrarInsW = tk.Button(framelisybotones, text="Borrar Instruccion", command=borrarelemento)
botonBlanco = tk.Button(frameEva, text="medir humedad de todo",
                        command=partial(Medir_all, mapa0, mapa1, mapa2, walle, eva, pm))
on_button1 = tk.Button(framebtns, image=on, bd=0, command=switch1)
on_button2 = tk.Button(framebtns, image=on, bd=0, command=switch2)
on_button3 = tk.Button(framebtns, image=on, bd=0, command=switch3)
on_button4 = tk.Button(framebtns, image=on, bd=0, command=switch4)
open_button = tk.Button(frameinvernadero, text="Abrir", command=open)
mid_button = tk.Button(frameinvernadero, text="Semi-Cerrar", command=mid)
close_button = tk.Button(frameinvernadero, text="Cerrar", command=closed)
RegarPlanta = tk.Button(frameWalle, text="Regar Planta",
                        command=partial(Regar_planta, mapa0, mapa1, mapa2, walle, eva, pm), state="disabled")
RegarTodo = tk.Button(frameWalle, text="Regar Todo", command=partial(Regar_all, mapa0, mapa1, mapa2, walle, eva, pm),
                      state="disabled")
MedirHumedad = tk.Button(frameEva, text="Medir Humedad",
                         command=partial(Medir_humedad, mapa0, mapa1, mapa2, walle, eva, pm), state="disabled")
MoverPlanta = tk.Button(frameminimover, text="Mover Planta",
                        command=partial(Mover_planta, mapa0, mapa1, mapa2, walle, eva, pm), state="disabled")
botonCancelar = tk.Button(frameminimover, text="Cancelar Movimiento", command=clear, state="disabled")
AgregarPlanta = tk.Button(frameminiagregar, text="Agregar planta", command=Agregar_planta, state="disabled")
EliminarPlanta = tk.Button(frameminiagregar, text="Eliminar planta", command=Eliminar_planta, state="disabled")
botonABORTAR = tk.Button(frameizquierda, text="ABORTAR", state="disabled", command=partial(abort), width=10, height=1,
                         foreground="#000000", background="#ff0000",
                         font=("Times", 12))
# walle Ventana
img1 = ImageTk.PhotoImage(Image.open("./assets/walleHD.png"))
panel1 = tk.Label(frameWalle, image=img1)
panel1.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
listbox.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
frameWalle.pack(side=tk.LEFT)

# eva Ventana
img2 = ImageTk.PhotoImage(Image.open("./assets/evaHD.png"))
panel2 = tk.Label(frameEva, image=img2)
panel2.pack(side=tk.TOP)
frameEva.pack(side=tk.LEFT)
# generales:
frameListbox.pack(side=tk.TOP)
framelisybotones.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

progress = ttk.Progressbar(canvas3, orient=tk.HORIZONTAL,
                           length=100, mode='determinate')
posMalla = "Estado actual de la Malla =____________"
# botones on off

lblblanca = tk.Label(framelbls, height=3)
lblcalefactor = tk.Label(framelbls, height=3)
lblbombaAgua = tk.Label(framelbls, height=3)
lblVentana = tk.Label(framelbls, height=3)
lblPuerta = tk.Label(framelbls, height=3)
lblblanca.config(text=" ")
lblcalefactor.config(text="Estado actual calefactor:")
lblbombaAgua.config(text="Estado actual Bomba de agua:")
lblPuerta.config(text="Estado actual Puerta:")
lblVentana.config(text="Estado actual Ventana:")

lblcalefactor.pack(side=tk.TOP)
lblbombaAgua.pack(side=tk.TOP)
lblPuerta.pack(side=tk.TOP)
lblVentana.pack(side=tk.TOP)

on_button1.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
on_button2.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
on_button3.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
on_button4.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

framecalefactor.pack(side=tk.BOTTOM)
framebtns.pack(side=tk.RIGHT)
framelbls.pack(side=tk.LEFT)
labelmalla = tk.Label(frameinvernadero)

progress.pack(pady=10)
labelmalla.pack(padx=200)
open_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
mid_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
close_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
frameinvernadero.pack(side=tk.RIGHT)
labelmalla.config(text=posMalla)

# fin botones invernadero


# botones seleccion de tarea


# walle, eva y  listbox
# listbox
BorrarInsW.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
moveUpButton.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
movedownButton.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# walle
RegarPlanta.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
RegarTodo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# eva

MedirHumedad.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
botonBlanco.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# mover planta

MoverPlanta.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
botonCancelar.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
AgregarPlanta.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
EliminarPlanta.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
framesalidas.pack(side=tk.TOP)
frameTipoPlanta.pack(side=tk.TOP)
frameminimover.pack(side=tk.LEFT)
frameminiagregar.pack(side=tk.LEFT)
cb1.pack(side=tk.LEFT)

frameTabs.pack()

TablasFrame = ttk.Frame(tab1)
TablasFrame.pack()

frameTabla1 = ttk.Frame(TablasFrame)
lbltabla1 = tk.Label(frameTabla1, text='Tabla piso 1')
lbltabla1.config(fg="black", font=("Verdana", 10))
lbltabla1.pack(side=tk.TOP)

frameTabla2 = ttk.Frame(TablasFrame)
lbltabla2 = tk.Label(frameTabla2, text='Tabla piso 2')
lbltabla2.config(fg="black", font=("Verdana", 10))
lbltabla2.pack(side=tk.TOP)

TablaPiso1 = ttk.Treeview(frameTabla1, selectmode='browse', height=pixel)
verscrlbar = ttk.Scrollbar(frameTabla1, orient='vertical', command=TablaPiso1.yview)
verscrlbar.pack(side=tk.LEFT, fill='y')
TablaPiso1.configure(yscrollcommand=verscrlbar.set)
TablaPiso1['columns'] = ('plant_id', 'plant_humidity', 'expected_humidity', 'type_plant')

TablaPiso1.column("#0", width=0, stretch=tk.NO)
TablaPiso1.column("type_plant", anchor=tk.CENTER, width=80)
TablaPiso1.column("plant_id", anchor=tk.CENTER, width=80)
TablaPiso1.column("plant_humidity", anchor=tk.CENTER, width=80)
TablaPiso1.column("expected_humidity", anchor=tk.CENTER, width=80)
TablaPiso1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
frameTabla1.pack(side=tk.LEFT)
frameTabla2.pack(side=tk.LEFT)
TablaPiso1.heading("#0", text="", anchor=tk.CENTER)
TablaPiso1.heading("type_plant", text="Tipo Planta", anchor=tk.CENTER)
TablaPiso1.heading("plant_id", text="Planta", anchor=tk.CENTER)
TablaPiso1.heading("plant_humidity", text="Humedad", anchor=tk.CENTER)
TablaPiso1.heading("expected_humidity", text="Humedad esperada", anchor=tk.CENTER)

TablaPiso2 = ttk.Treeview(frameTabla2, height=pixel)
TablaPiso2['columns'] = ('plant_id', 'plant_humidity', 'expected_humidity', 'type_plant')
TablaPiso2.column("#0", width=0, stretch=tk.NO)
TablaPiso2.column("type_plant", anchor=tk.CENTER, width=80)
TablaPiso2.column("plant_id", anchor=tk.CENTER, width=80)
TablaPiso2.column("plant_humidity", anchor=tk.CENTER, width=80)
TablaPiso2.column("expected_humidity", anchor=tk.CENTER, width=80)
TablaPiso2.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
TablaPiso2.heading("#0", text="", anchor=tk.CENTER)
TablaPiso2.heading("type_plant", text="Tipo Planta", anchor=tk.CENTER)
TablaPiso2.heading("plant_id", text="Planta", anchor=tk.CENTER)
TablaPiso2.heading("plant_humidity", text="Humedad", anchor=tk.CENTER)
TablaPiso2.heading("expected_humidity", text="Humedad esperada", anchor=tk.CENTER)

for i in range(100):
    if i in numbers1:
        TablaPiso1.insert(parent='', index='end', iid=i, text='',
                          values=(i, "?", humedadesperada[i], tipo[i]))

for i in range(100):
    if i in numbers2:
        TablaPiso2.insert(parent='', index='end', iid=i, text='',
                          values=(i + 100, "?", humedadesperada2[i], tipo2[i]))

monitor2.pack(side=tk.TOP)

framePlantaSelect.pack(side=tk.TOP)
monitor1.pack(side=tk.TOP)
framegeneral.pack(side=tk.TOP)
framegeneral.config(border=10)
frameMovimiento.pack(side=tk.TOP)
frameMovimiento.config(border=10)
frameinformacion.pack(side=tk.TOP)
frameinformacion.config(border=20)

botonABORTAR.pack(side=tk.TOP)

ventana.mainloop()

