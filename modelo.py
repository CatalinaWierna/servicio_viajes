import sqlite3
def primer_acceso ():
    try:
        acceso_bd()
        crear_tabla()
    except:
        print("Hay un error")

def acceso_bd():
    con = sqlite3.connect("carpool.db")
    return con

def crear_tabla():
    con = acceso_bd()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS viajes (
            id_chofer               INTEGER      PRIMARY KEY,
            origen                TEXT,
            destino       TEXT,
            fecha INTEGER TEXT,
            asientos_disp INTEGER
        )
    """
    cursor.execute(sql)
    con.commit()

def viajes_en_BD ():
    con= acceso_bd()
    cursor = con.cursor()
    sql = "SELECT * FROM viajes"
    cursor.execute(sql)
    return cursor.fetchall()

def eliminar_por_id_BD (id):
    con= acceso_bd()
    cursor = con.cursor()
    data = (id, )
    sql="DELETE FROM viajes WHERE id_chofer = ?;"
    cursor.execute(sql,data)
    con.commit()

def actualizar_asientos_viaje (nueva_cant_asientos, id_chofer):
    con= acceso_bd()
    cursor = con.cursor()
    data = (nueva_cant_asientos,id_chofer)
    sql="UPDATE viajes SET asientos_disp = ? WHERE id_chofer = ?;"
    cursor.execute(sql,data)
    con.commit()

def agregar_viaje_BD(id,origen,destino,fecha,asientos_disp): 
    con = acceso_bd()
    cursor = con.cursor()
    data = (int(id),origen, destino,fecha, asientos_disp)
    sql ="INSERT INTO viajes(id_chofer,origen,destino,fecha,asientos_disp) VALUES(?, ?, ?, ?, ?);"
    cursor.execute(sql,data)
    con.commit()