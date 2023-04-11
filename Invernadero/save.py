import sqlite3

def conectar():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    return con, cur

def insertarDatos(plant_id, expected_humidity, type_plant):
    con, cur = conectar()
    sentencia = "INSERT INTO planta(plant_id, expected_humidity, type_plant) VALUES(?,?,?)"
    datos = (plant_id, expected_humidity, type_plant)
    cur.execute(sentencia,datos)
    con.commit()
    con.close()

def insertarDatos2(plant_id, expected_humidity, type_plant):
    con, cur = conectar()
    sentencia = "INSERT INTO planta2(plant_id, expected_humidity, type_plant) VALUES(?,?,?)"
    datos = (plant_id, expected_humidity, type_plant)
    cur.execute(sentencia,datos)
    con.commit()
    con.close()

def consultarDatos(plant_id):
    con, cur = conectar()
    m = ""
    resultado = cur.execute("SELECT * FROM planta WHERE plant_id = ?",(plant_id,))
    for fila in resultado:
        m = [fila[0],fila[1],fila[2]]
    con.close()
    return m

def consultarDatos2(plant_id):
    con, cur = conectar()
    m = ""
    resultado = cur.execute("SELECT * FROM planta2 WHERE plant_id = ?",(plant_id,))
    for fila in resultado:
        m = [fila[0],fila[1],fila[2]]
    con.close()
    return m

def consultarDatosM(piso):
    con, cur = conectar()
    m = ""
    resultado = cur.execute("SELECT * FROM mapas WHERE piso = ?",(piso,))
    for fila in resultado:
        m = [fila[1],
             fila[2],
             fila[3],
             fila[4],
             fila[5],
             fila[6],
             fila[7],
             fila[8],
             fila[9],
             fila[10]
             ]
    con.close()
    return m

def actualizarDatos(plant_id, expected_humidity, type_plant):
    con, cur = conectar()
    cur.execute("UPDATE planta SET expected_humidity = ?, type_plant = ? WHERE plant_id = ?",(expected_humidity,type_plant,plant_id))
    con.commit()
    con.close()
    print("datos actualizados correctamente")
    return True

def actualizarDatos2(plant_id, expected_humidity, type_plant):
    con, cur = conectar()
    cur.execute("UPDATE planta2 SET expected_humidity = ?, type_plant = ? WHERE plant_id = ?",(expected_humidity,type_plant,plant_id))
    con.commit()
    con.close()
    print("datos actualizados correctamente")
    return True

def actualizarDatosM(piso,mapa):
    con, cur = conectar()
    cur.execute("UPDATE mapas SET '1' = ?, '2' = ?, '3' = ?, '4' = ?, '5' = ?, '6' = ?, '7' = ?, '8' = ?, '9' = ?, '10' = ? WHERE piso = ?",
                (mapa[0],mapa[1],mapa[2],mapa[3],mapa[4],mapa[5],mapa[6],mapa[7],mapa[8],mapa[9],piso))
    con.commit()
    con.close()
    print("datos del mapa actualizados correctamente")
    return True
