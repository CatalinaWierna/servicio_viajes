import sqlite3
from peewee import *
from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox

db = SqliteDatabase('carpool.db')

class BaseModel(Model):
    class Meta:
        database = db

#Esto representa mi tabla de viajes
class Viaje(BaseModel):
    id_chofer = IntegerField(primary_key=True, unique=True)
    origen = CharField()
    destino = CharField()
    fecha = CharField()
    asientos_disp = IntegerField()

db.connect()
db.create_tables([Viaje])
class Base ():
    def __init__ (self,):pass

    #Alta de registros
    def agregar_viaje_BD(self,id_chofer,origen,destino,fecha,asientos_disp):
        try:
            viaje=Viaje.create(id_chofer=id_chofer,origen=origen,destino=destino,fecha=fecha,asientos_disp=asientos_disp)
            viaje.save()
        except ErroEnLaBaseDeDatos as e:
            e.mostrar_mensaje("Error al agregar el viaje")
    
    def viajes_en_BD (self,):
        return Viaje.select()
    
    def get_ids(self):
        try:
            return [viaje.id_chofer for viaje in Viaje.select()]
        except Viaje.DoesNotExist:
            return []
    
    def actualizar_asientos_viaje (self,nueva_cant_asientos, id_chofer):
        try:
            viaje = Viaje.get(Viaje.id_chofer == id_chofer)
            viaje.asientos_disp = nueva_cant_asientos
            viaje.save()
        except ErroEnLaBaseDeDatos as e:
            e.mostrar_mensaje("No se encontro el viaje")
    def eliminar_por_id_BD (self,id):
        viaje = Viaje.get_or_none(Viaje.id_chofer == id)
        if viaje is None:
            error = ErroEnLaBaseDeDatos("No se encontro el viaje")
            error.mostrar_mensaje("No se encontro el viaje")
        else:
            viaje.delete_instance()
class ErroEnLaBaseDeDatos(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
    def mostrar_mensaje(self,mensaje):
        messagebox.showerror("Error",mensaje)