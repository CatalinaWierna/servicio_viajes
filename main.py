from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox
import sqlite3

"""VARIABLES GLOBALES----------------------------------------------------------------------------------------------------------------------------------------------"""
nombre_app = "Servicio de Viajes"
titulo_carga = "Cargar Viaje"
titulo_seleccionar = "Viaje Seleccionado"
lista_viajes = []
id_boton_seleccionado =0
viaje_seleccionado = None
contador_fila = 0

colores = {
    "primario claro" : "#2A9D8F",
    "botones claro": "#E9C46A",
    "fondo claro" : "#264653",
    "texto claro" : "#FFFFFF",
    "texto botones claor" : "#BFBFBF"
}

ciudades_argentina = [
    "Buenos Aires",
    "Córdoba",
    "Rosario",
    "Mendoza",
    "La Plata",
    "San Miguel de Tucumán",
    "Mar del Plata",
    "Salta",
    "Santa Fe",
    "San Juan",
    "Resistencia",
    "Neuquén",
    "Posadas",
    "Santiago del Estero",
    "Corrientes",
    "Bahía Blanca",
    "San Salvador de Jujuy",
    "Paraná",
    "Formosa",
    "San Luis"
]
"""FUNCIONES -------------------------------------------------------------------------------------------------------------------------------------------------------"""

def acceso_bd():
    con = sqlite3.connect("carpool.db")
    return con

def confirmar(tipo_confirmacion,data):
    global boton_seleccionado
    proceso_Exitoso = True
    if askyesno(tipo_confirmacion,'Desea '+tipo_confirmacion+' el viaje'):
        if(tipo_confirmacion == "eliminar"):
            eliminar_por_id(data)
        if(tipo_confirmacion == "reservar"):
            proceso_Exitoso = reservar_asientos(data,id_boton_seleccionado)
        if(proceso_Exitoso):
            showinfo(tipo_confirmacion, 'Viaje '+tipo_confirmacion[:-1]+'do exitosamente')
    else:
        showinfo('No '+tipo_confirmacion, 'Volver a la pantalla principal')
    proceso_Exitoso = True


def agregar_tabla(origen,destino,fecha,id_chofer,asientos_disp,frame,canvas):
    if origen in ciudades_argentina and destino in ciudades_argentina:
        con = acceso_bd()
        cursor = con.cursor()
        data = (int(id_chofer), str(origen), str(destino), str(fecha), int(asientos_disp))
        sql ="INSERT INTO viajes(id_chofer,origen,destino,fecha,asientos_disp) VALUES(?, ?, ?, ?, ?);"
        cursor.execute(sql,data)
        con.commit()
        agregar_scroll_viaje(origen,destino,fecha,asientos_disp,id_chofer,frame,canvas)
    else:
        messagebox.showerror("Error","Error: el origen o destino no esta disponible")

def agregar_scroll_viaje(origen,destino,fecha,asientos_disp,id_chofer,frame,canvas):
    global viaje_seleccionado, contador_fila
    viaje_btn = Button(frame, text= origen+" a "+destino+". Fecha: "+fecha, width=55, height=2, bg=colores["botones claro"], command=lambda:seleccionar_viaje(viaje_btn))
    viaje_btn.grid(row=contador_fila, column=0, columnspan=2, sticky="ew", pady=5)
    contador_fila +=1
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    lista_viajes.append([viaje_btn,[origen,destino,fecha,asientos_disp,id_chofer],True])
     
def seleccionar_viaje(viaje_btn):
        global viaje_seleccionado,id_boton_seleccionado
        if viaje_seleccionado:
            viaje_seleccionado.config(bg=colores["botones claro"])
        viaje_btn.config(bg="lightblue")
        id_boton_seleccionado = buscar_viaje_por_boton(viaje_btn)
        print(id_boton_seleccionado)
        viaje_seleccionado = viaje_btn


def eliminar_por_id (id_buscar):
    con= acceso_bd()
    cursor = con.cursor()
    data = (id_buscar, )
    sql="DELETE FROM viajes WHERE id_chofer = ?;"
    cursor.execute(sql,data)
    con.commit()
    for viaje in lista_viajes:
        if(viaje[1][4]==id_buscar):
            viaje[0].destroy()


def actualizar_asientos_viaje (nueva_cant_asientos, id_chofer):
    con= acceso_bd()
    cursor = con.cursor()
    data = (nueva_cant_asientos,id_chofer)
    sql="UPDATE viajes SET asientos_disp = ? WHERE id_chofer = ?;"
    cursor.execute(sql,data)
    con.commit()

def cargar_viajes_guardados(frame,canvas):
    con= acceso_bd()
    cursor = con.cursor()
    sql = "SELECT * FROM viajes"
    cursor.execute(sql)
    filas = cursor.fetchall()
    for row in filas:
        agregar_scroll_viaje(row[1],row[2],row[3],row[4],row[0],frame,canvas)
        
def filtrar(origen="", destino="", fecha=""):
    global lista_viajes
    for x in lista_viajes:
        mostrar = True

        if origen and x[1][0] != origen:
            mostrar = False
        if destino and x[1][1] != destino:
            mostrar = False
        if fecha and x[1][2] != fecha:
            mostrar = False

        if mostrar:
            if not x[2]:  
                x[0].grid(pady=5)
                x[2] = True
        else:
            if x[2]:  
                x[0].grid_remove()  
                x[2]= False 

def buscar_viaje_por_boton(btn_viaje):
    for viaje in lista_viajes:
        if(viaje[0]==btn_viaje):
            return viaje[1][4]


def reservar_asientos(cant_asientos,id_chofer):
    for viaje in lista_viajes:
        if viaje[1][4] == id_chofer :
            if(viaje[1][3] > cant_asientos):
                viaje[1][3] -= cant_asientos
                actualizar_asientos_viaje (viaje[1][3], id_chofer)
                return True
            else:
                if viaje[1][3] == cant_asientos:
                    lista_viajes.remove(viaje)
                    eliminar_por_id(id_chofer)
                    viaje[0].destroy()
                    return True
                else :
                    messagebox.showerror("Error","Error: no hay suficientes asientos disponibles")
                    return False



"""INICIO DE LA INTERFAZ GRAFICA------------------------------------------------------------------------------------------------------------------------"""


root = Tk()
root .title(nombre_app)

root.geometry("1200x600")
root.resizable(False,False)
root.configure(bg=colores["fondo claro"])

"""TITULO DE LA APP"""
title_frame = Frame(root, padx=5, pady=10, width=400, height=50, bg=colores["primario claro"])
title_frame.place(y=10,x=520)  

title_label = Label(title_frame, text=nombre_app, font=("Arial", 16, "bold"),fg=colores["texto claro"], bg = colores["primario claro"])
title_label.grid()



"""Viajes disponibles"""
viajes_disponibles_title = Label(root,text="Viajes Disponibles", font=("Arial", 16 ), bg=colores["primario claro"], fg=colores["texto claro"])
viajes_disponibles_title.place(y=120 , x=535)

frame_viajes_disponibles = Frame(root,width=400,height=600, bg=colores["primario claro"])
frame_viajes_disponibles.place(x=420,y=150)
canvas = Canvas(frame_viajes_disponibles,bg=colores["primario claro"])
canvas.grid(row=0, column=0)
viajes_disponibles = Scrollbar(frame_viajes_disponibles, orient="vertical", command=canvas.yview)
viajes_disponibles.grid(row=0, column=1, sticky=NS)
canvas.config(yscrollcommand=viajes_disponibles.set)
frame_interior = Frame(canvas,width=400,height=600,bg=colores["primario claro"])
canvas.create_window((0, 0), window=frame_interior, anchor="nw")


viaje_seleccionado = None
contador_fila = 0


"""CARGA DE VIAJES"""
#Titulo y Frame principales
load_frame = Frame(root,width=200,height=175,bg=colores["primario claro"])
load_frame.place(x=20,y=350)

load_title = Label(load_frame,text=titulo_carga, font=("Arial", 14 ),bg=colores["primario claro"], fg=colores["texto claro"])
load_title.grid(column=0,sticky=W)


#Labels de la carga
load_origen_label = Label(load_frame,text="Origen",font=("Arial",11),bg=colores["primario claro"], fg=colores["texto claro"])
load_origen_label.grid(row=4,column=0,sticky=W)

load_destino_label = Label(load_frame,text="Destino",font=("Arial",11),bg=colores["primario claro"], fg=colores["texto claro"])
load_destino_label.grid(row=8,column=0,sticky=W)

load_fecha_label = Label(load_frame,text="Fecha de Salida",font=("Arial",11),bg=colores["primario claro"], fg=colores["texto claro"])
load_fecha_label.grid(row=12,column=0,sticky=W)

load_asientosDisp_label = Label(load_frame,text="Asientos Disponibles",font=("Arial",11),bg=colores["primario claro"], fg=colores["texto claro"])
load_asientosDisp_label.grid(row=16,column=0,sticky=W)

load_choferId_label = Label(load_frame,text="ID Chofer",font=("Arial",11),bg=colores["primario claro"], fg=colores["texto claro"])
load_choferId_label.grid(row=20,column=0,sticky=W)

#Entrys de la carga

origen = StringVar()
destino = StringVar()
fecha = StringVar()
asientos_disp = IntVar()
chofer_id = IntVar()

entry_origen_label = Entry(load_frame,textvariable=origen)
entry_origen_label.grid(row=4,column=1)

entry_destino_label = Entry(load_frame,textvariable=destino)
entry_destino_label.grid(row=8,column=1)

entry_fecha_label = Entry(load_frame,textvariable=fecha)
entry_fecha_label.grid(row=12,column=1,sticky=W)

entry_asientosDisp_label = Entry(load_frame,textvariable=asientos_disp)
entry_asientosDisp_label.grid(row=16,column=1)

entry_choferId_label = Entry(load_frame,textvariable=chofer_id)
entry_choferId_label.grid(row=20,column=1)

#Boton para finalizar carga

load_button = Button(load_frame,text="ACEPTAR", font=("Arial",8), bg=colores["botones claro"],command=lambda:agregar_tabla(origen.get(),destino.get(),fecha.get(),chofer_id.get(),asientos_disp.get(),frame_interior,canvas))
load_button.grid(row=290,column=174)

cargar_viajes_guardados(frame_interior,canvas)

"""Reservar Asientos"""
frame_selected = Frame(width=150,height=50, bg=colores["primario claro"])
frame_selected.place(x=890,y=300)
selected_title = Label(frame_selected,text="Reservar", font=("Arial", 14 ), bg=colores["primario claro"], fg=colores["texto claro"])
selected_title.grid(row=0,column=0,sticky=W)
selected_title = Label(frame_selected,text="Asientos", font=("Arial", 14 ), bg=colores["primario claro"], fg=colores["texto claro"])
selected_title.grid(row=0,column=1,sticky=W)

load_asientos_label = Label(frame_selected,text="Cantidad",font=("Arial",11), bg=colores["primario claro"], fg=colores["texto claro"])
load_asientos_label.grid(row=4,column=0,sticky=W)
cant_asientos_reserva = IntVar()
entry_asientos_label = Entry(frame_selected, width=18, textvariable=cant_asientos_reserva)
entry_asientos_label.grid(row=4,column=1)

load_button = Button(frame_selected,text="RESERVAR", font=("Arial",8), command=lambda:confirmar("reservar",cant_asientos_reserva.get()),bg=colores["botones claro"])
load_button.grid(row=299,column=174)



"""Eliminar Viaje"""
frame_delete = Frame(root,width=150,height=175, bg=colores["primario claro"])
frame_delete.place(x=890,y=400)
selected_title = Label(frame_delete,text="Eliminar", font=("Arial", 14 ), bg=colores["primario claro"],fg=colores["texto claro"])
selected_title.grid(column=0,sticky=W)
selected_title = Label(frame_delete,text="Viaje", font=("Arial", 14 ),bg=colores["primario claro"],fg=colores["texto claro"])
selected_title.grid(column=1,sticky=W,row=0)

load_choferId_label = Label(frame_delete,text="ID Chofer ",font=("Arial",11),bg=colores["primario claro"],fg=colores["texto claro"])
load_choferId_label.grid(row=4,column=0,sticky=W)

id_a_eliminar = IntVar()
entry_choferId_label = Entry(frame_delete,textvariable = id_a_eliminar)
entry_choferId_label.grid(row=4,column=1)


load_button = Button(frame_delete,text="ELIMINAR", font=("Arial",8),width=9, command=lambda:confirmar("eliminar", id_a_eliminar.get()),bg=colores["botones claro"])
load_button.grid(row=299,column=174)



"""Filtrar Viajes"""
#Titulo y Frame del filtro
frame_filtro = Frame(root ,width=265,height=50, bg=colores["primario claro"])
frame_filtro.place(x=890,y=150)

load_title = Label(frame_filtro,text="Filtrar", font=("Arial", 14 ), bg= colores["primario claro"], fg=colores["texto claro"])
load_title.grid(column=0,sticky=W)

#Labels del filtro
load_origen_label_filtro = Label(frame_filtro,text="Origen",font=("Arial",11), bg= colores["primario claro"], fg=colores["texto claro"])
load_origen_label_filtro.grid(row=4,column=0,sticky=W)

load_destino_label_filtro = Label(frame_filtro,text="Destino",font=("Arial",11), bg= colores["primario claro"], fg=colores["texto claro"])
load_destino_label_filtro.grid(row=8,column=0,sticky=W)

load_fecha_label_filtro = Label(frame_filtro,text="Fecha",font=("Arial",11), bg= colores["primario claro"], fg=colores["texto claro"])
load_fecha_label_filtro.grid(row=12,column=0,sticky=W)


#Entrys del flitro
origen_filtro = StringVar()
destino_filtro = StringVar()
fecha_filtro = StringVar()

entry_origen_label_filtro = Entry(frame_filtro,textvariable=origen_filtro)
entry_origen_label_filtro.grid(row=4,column=1)

entry_destino_label_filtro = Entry(frame_filtro,textvariable=destino_filtro)
entry_destino_label_filtro.grid(row=8,column=1)

entry_fecha_label_filtro = Entry(frame_filtro,textvariable=fecha_filtro)
entry_fecha_label_filtro.grid(row=12,column=1,sticky=W)

load_button = Button(frame_filtro,text="FILTRAR", font=("Arial",8),width=11, bg=colores["botones claro"],command=lambda:filtrar(origen = origen_filtro.get(),destino =destino_filtro.get(),fecha = fecha_filtro.get()))
load_button.grid(row=299,column=174)

root.mainloop()
