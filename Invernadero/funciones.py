

def traducir(x,pixel):
    valor = int(x/pixel)
    return valor

def matriz(x,y,pixel):
    lugar = traducir(x,pixel) + (10*traducir(y,pixel))
    return lugar

def black_matriz(planta,pixel):
    posicion= (int(planta%10)*pixel),(int(planta/10)*pixel)
    return posicion

def exactitud(x,y,pixel):
    if (x%pixel==0 and y%pixel==0):
        return True
    else:
        return False

def reemplazar(linea, y, tomar): #linea es la posicion en el arreglo, y es el caracter a cambiar
    aux2 = list(linea)
    if(tomar== True):
        aux2[y] = ' '
    elif(tomar== "regado"):
        aux2[y] = 'X'
    linea = "".join(aux2)
    return linea

def buscar_id(plantas,planta):
    id = 0
    for i in range (len(plantas)):
        if (planta == plantas[i][0]):
            id = plantas[i][1]
    return id





