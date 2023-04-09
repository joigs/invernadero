class Robot:

    def __init__(self,x,y,piso,planta,key,entrando, destino_final,accion,quieto,id,tomar,orden):
        self.x=x #posicion x
        self.y=y #posicion y
        self.piso = piso
        self.planta = planta #la planta a la que se dirige
        self.key = key
        self.entrando = entrando #si es que entra a la base
        self.destino_final = destino_final #hacia donde se dirige
        self.accion = accion #si se esta moviendo
        self.quieto = quieto #hace que se quede quieto unos momentos al realizar un accion
        self.id = id
        self.tomar = tomar
        self.orden = orden

