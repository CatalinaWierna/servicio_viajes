import re
from modelo import *

class Ventanita():
    def __init__ (self,window):
        self.root = window

        colores = {
        "primario claro" : "#2A9D8F",
        "botones claro": "#E9C46A",
        "fondo claro" : "#264653",
        "texto claro" : "#FFFFFF",
        "texto botones claor" : "#BFBFBF"
        }
        nombre_app = "Servicio de Viajes"
        titulo_carga = "Cargar Viaje"

        self.id_boton_seleccionado = None
        self.lista_viajes = []
        self.viaje_seleccionado = False
        self.contador_fila = 0

        #Conexion Base de datos.
        self.base = Base()

        #Configuraciones visuales ventana
        self.root .title(nombre_app)
        self.root.geometry("1200x600")
        self.root.resizable(False,False)
        self.root.configure(bg=colores["fondo claro"])

        #Titulo principal de la app
        self.title_frame = Recuadro (self.root,400,50,colores["primario claro"],520,10,5,10)
        self.titel_Lable = Titulo (self.title_frame.retornar_frame(),nombre_app,("Arial", 16, "bold"),colores["texto claro"],colores["primario claro"])
        
        #Scroll viajes disponibles
        self.viajes_disponibles_title = Label(self.root,text="Viajes Disponibles", font=("Arial", 16 ), bg=colores["primario claro"], fg=colores["texto claro"])
        self.viajes_disponibles_title.place(y=120 , x=535)
        self.frame_viajes_disponibles = Frame(self.root,width=400,height=600, bg=colores["primario claro"])
        self.frame_viajes_disponibles.place(x=420,y=150)
        self.canvas = Canvas(self.frame_viajes_disponibles,bg=colores["primario claro"])
        self.canvas.grid(row=0, column=0)
        self.viajes_disponibles = Scrollbar(self.frame_viajes_disponibles, orient="vertical", command=self.canvas.yview)
        self.viajes_disponibles.grid(row=0, column=1, sticky=NS)
        self.canvas.config(yscrollcommand=self.viajes_disponibles.set)
        self.frame_interior = Frame(self.canvas,width=400,height=600,bg=colores["primario claro"])
        self.canvas.create_window((0, 0), window=self.frame_interior, anchor="nw")

        #Carga de Viajes
        self.frame_carga = Recuadro (self.root,200,175,colores["primario claro"],20,250)
        self.title_carga = Titulo (self.frame_carga.retornar_frame(),titulo_carga,("Arial", 14 ),colores["primario claro"],colores["texto claro"])
        self.title_origen = Titulo (self.frame_carga.retornar_frame(),"Origen",("Arial",11),colores["primario claro"],colores["texto claro"],4,0)
        self.title_origen = Titulo (self.frame_carga.retornar_frame(),"Destino",("Arial",11),colores["primario claro"],colores["texto claro"],8,0)
        self.title_origen = Titulo (self.frame_carga.retornar_frame(),"Fecha de Salida",("Arial",11),colores["primario claro"],colores["texto claro"],12,0)
        self.title_origen = Titulo (self.frame_carga.retornar_frame(),"Asientos Disponibles",("Arial",11),colores["primario claro"],colores["texto claro"],16,0)
        self.title_origen = Titulo (self.frame_carga.retornar_frame(),"ID Chofer",("Arial",11),colores["primario claro"],colores["texto claro"],20,0)


        origen = StringVar()
        destino = StringVar()
        fecha = StringVar()
        asientos_disp = IntVar()
        chofer_id = IntVar()
        self.entry_origen = Entrada (self.frame_carga.retornar_frame(),origen,4,1)
        self.entry_origen = Entrada (self.frame_carga.retornar_frame(),destino,8,1)
        self.entry_origen = Entrada (self.frame_carga.retornar_frame(),fecha,12,1)
        self.entry_origen = Entrada (self.frame_carga.retornar_frame(),asientos_disp,16,1)
        self.entry_origen = Entrada (self.frame_carga.retornar_frame(),chofer_id,20,1)
        
        self.boton_carga = Boton_Carga(self.frame_carga.retornar_frame(),"ACEPTAR",("Arial",8),colores["botones claro"],290,175, self.base,self, origen,destino,fecha,chofer_id,asientos_disp,self.frame_interior,self.canvas,self.lista_viajes)
        self.cargar_viajes_guardados(self.frame_interior,self.canvas,self.lista_viajes)

        #Reserva de Asientos
        self.frame_reserva = Recuadro (self.root,150,50,colores["primario claro"],890,174)
        self.title_reserva = Titulo (self.frame_reserva.retornar_frame(),"Reservar",("Arial",14),colores["primario claro"], colores["texto claro"])
        self.title_reservar_2 = Titulo (self.frame_reserva.retornar_frame(),"Asientos",("Arial", 14 ),colores["primario claro"], colores["texto claro"],0,1)

        self.titulo_reservar_cantidad = Titulo (self.frame_reserva.retornar_frame(),"Cantidad",("Arial", 11 ),colores["primario claro"], colores["texto claro"],4,0)
        self.cant_asientos_reservados = IntVar()
        self.entry_asientos_res = Entrada(self.frame_reserva.retornar_frame(),self.cant_asientos_reservados,4,1,18)
        #(self,frame,texto,fuente,color,info,tipo_confirmacion,base,fila,columna)
        self.boton_reservar = Boton_Reservar_Eliminar(self.frame_reserva.retornar_frame(),"RESERVAR",("Arial",8),colores["botones claro"],self.cant_asientos_reservados,"reservar",self.base,299,174,self,self.lista_viajes)

        
        #Eliminar Viaje
        self.frame_delete = Recuadro(self.root,150,175,colores["primario claro"],890,400)
        self.title_delete = Titulo(self.frame_delete.retornar_frame(),"Eliminar",("Arial", 14 ),colores["primario claro"],colores["texto claro"],0,0)
        self.title_delete_2 = Titulo(self.frame_delete.retornar_frame(),"Viaje",("Arial",14),colores["primario claro"],colores["texto claro"],0,1)
        self.title_id_delete = Titulo(self.frame_delete.retornar_frame(),"ID Chofer",("Arial",11),colores["primario claro"],colores["texto claro"],4,0)
        self.id_a_eliminar = IntVar()
        self.entry_id_delete = Entrada(self.frame_delete.retornar_frame(),self.id_a_eliminar,4,1)
        self.boton_delete = Boton_Reservar_Eliminar(self.frame_delete.retornar_frame(),"ELIMINAR",("Arial,",8),colores["botones claro"],self.id_a_eliminar,"eliminar",self.base,299,174,self,self.lista_viajes)

        #Filtrar Viajes
        self.frame_filtrar = Recuadro(self.root,265,50,colores["primario claro"],890,265)
        self.title_filtrar = Titulo(self.frame_filtrar.retornar_frame(),"Filtrar",("Arial",14),colores["primario claro"],colores["texto claro"],0,0)
        self.origen_filtrar = Titulo (self.frame_filtrar.retornar_frame(),"Origen",("Arial",11),colores["primario claro"],colores["texto claro"],4,0)
        self.destino_filtrar = Titulo(self.frame_filtrar.retornar_frame(),"Destino",("Arial",11),colores["primario claro"],colores["texto claro"],8,0)
        self.fecha_filtrar = Titulo(self.frame_filtrar.retornar_frame(),"Fecha",("Arial",11),colores["primario claro"],colores["texto claro"],12,0)
        self.origen_filtro = StringVar()
        self.entry_origen_filtro = Entrada(self.frame_filtrar.retornar_frame(),self.origen_filtro,4,1)
        self.destino_filtro = StringVar()
        self.entry_destino_filtro = Entrada(self.frame_filtrar.retornar_frame(),self.destino_filtro,8,1)
        self.fecha_filtro = StringVar()
        self.entry_fecha_filtro = Entrada(self.frame_filtrar.retornar_frame(),self.fecha_filtro,12,1)
        self.boton_filtrar = Boton_Filtrar(self.frame_filtrar.retornar_frame(),"FILTRAR",("Ariale",8),colores["botones claro"],self.origen_filtro,self.destino_filtro,self.fecha_filtro,299,174,11,self.lista_viajes)


    def cargar_viajes_guardados(self,frame,canvas,lista_viajes):
        for row in self.base.viajes_en_BD():
            self.boton = Boton_Viaje (row.origen,row.destino,row.fecha,row.asientos_disp,row.id_chofer,frame,canvas,self)
            self.contador_fila +=1
        self.frame_interior.update_idletasks()  
        self.canvas.config(scrollregion=self.canvas.bbox("all"))




class Recuadro ():
    def __init__ (self,frame,ancho,alto,color,posx,posy,x=0,y=0):
        self.frame = Frame(frame, padx=x, pady=y, width=ancho, height=alto, bg=color)
        self.frame.place(y=posy,x=posx)
    def retornar_frame (self):
        return self.frame

class Posicion_Widget ():
    def colocar_widget (self,widget,fila,columna,span=None,stick=None,y=None,ancho=None):
        widget.grid(row=fila, column=columna, columnspan=span, sticky=stick, pady=y)

class Titulo (Posicion_Widget):
    def __init__(self,frame,texto,fuente,color_texto,color_fondo,posx=0,posy=0):
        self.titulo = Label(frame,text=texto,font=fuente,bg=color_texto,fg=color_fondo)
        super().colocar_widget(self.titulo,posx,posy,None,W)

class Entrada (Posicion_Widget):
    def __init__(self,frame,variable,x,y,ancho = None):
        self.entrada = Entry(frame,width=ancho,textvariable=variable)
        super().colocar_widget(self.entrada,x,y,None,W)

class Boton_Carga(Posicion_Widget) :
    def __init__(self,frame,texto,fuente,color,fila,columna,base,ventanita,origen=None,destino=None,fecha=None,chofer_id=None,asientos_disp=None,frame_interior=None,canvas=None,id_boton_seleccionado=None,lista_viajes=None,viaje_seleccionado=None):
        self.ventanita = ventanita
        self.boton = Button (frame,text=texto,font=fuente,bg=color,command = lambda : self.cargar(origen,destino,fecha,chofer_id,asientos_disp,frame_interior,canvas,base,lista_viajes))
        super().colocar_widget(self.boton,fila,columna)
    
    def cargar (self,ori,dest,fec,id,asientos,frame,canvas,base,lista_viajes):
        origen = str(ori.get())
        destino = str(dest.get())
        fecha = str(fec.get())
        asientos_disp = int(asientos.get())
        id_chofer = int(id.get())
        if self.validar_fecha(fecha) and self.validar_id_chofer(id_chofer):
            if self.validar_ciudad(origen) and self.validar_ciudad(destino) and self.id_unico(id_chofer,base):
                base.agregar_viaje_BD(id_chofer,origen,destino,fecha,asientos_disp)
                self.ventanita.contador_fila += 1
                self.nuevo_boton = Boton_Viaje(origen,destino,fecha,asientos_disp,id_chofer,frame,canvas,self.ventanita)
        ori.set("")
        dest.set("")
        fec.set("")
        id.set("")
        asientos.set("")
    
    def validar_fecha(self,fecha):
        patron = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$'
        if re.match(patron, fecha):
            return True
        else:
            error = ErrorFechaInvalida()
            error.registrar_error()
            return False
    
    def validar_id_chofer(self,id_chofer):
        patron = r"^\d{4}$"
        if re.match(patron, str(id_chofer)):
            return True
        else:
            error = ErrorIDInvalido()
            error.registrar_error()
            return False
        
    def id_unico(self,id_chofer,base):
        ids_cargados = base.get_ids()
        if (ids_cargados != []):
            for row in ids_cargados:
                if row == id_chofer:
                    error = ErrorIDRepetido()
                    error.registrar_error()
                    return False
            return True
        return True
    def validar_ciudad(self,ciudad):
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
        if ciudad in ciudades_argentina:
            return True
        else:
            error = ErrorCiudadInvalida()
            error.registrar_error()
            return False

class Boton_Viaje(Posicion_Widget):
    def __init__(self,origen,destino,fecha,asientos_disp,id_chofer,frame,canvas,ventanita):
        self.ventanita = ventanita
        self.boton = Button(frame, text= origen+" a "+destino+". Fecha: "+fecha, width=55, height=2, bg="#E9C46A", command=lambda : self.seleccionar_viaje(self.boton,ventanita.viaje_seleccionado))
        super().colocar_widget(self.boton,self.ventanita.contador_fila,0,2,"ew",5)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        self.ventanita.lista_viajes.append([self.boton,[origen,destino,fecha,asientos_disp,id_chofer],True])
    
    def seleccionar_viaje(self, boton, viaje_seleccionado):
        if viaje_seleccionado:
            viaje_seleccionado.config(bg="#E9C46A")
        boton.config(bg="lightblue")
        self.ventanita.viaje_seleccionado = boton
        self.ventanita.id_boton_seleccionado = self.buscar_viaje_por_boton(boton)
    
    def buscar_viaje_por_boton(self,boton):
        for viaje in self.ventanita.lista_viajes:
            print (viaje)
            if(viaje[0]==boton):
                return viaje[1][4]

class Boton_Reservar_Eliminar (Posicion_Widget):
    def __init__ (self,frame,texto,fuente,color,info,tipo_confirmacion,base,fila,columna,ventanita,lista_viajes=None):
        self.ventanita = ventanita
        self.boton = Button (frame,text=texto,font=fuente,bg=color,command = lambda : self.confirmar(tipo_confirmacion,info,base,lista_viajes))
        super().colocar_widget(self.boton,fila,columna)
    
    def confirmar (self,tipo_confirmacion,info,base,lista_viajes):
        data = info.get()
        if askyesno(tipo_confirmacion,'Desea '+tipo_confirmacion+' el viaje'):
            if(tipo_confirmacion == "eliminar"):
                if self.eliminar_por_id(data,base,lista_viajes):
                    showinfo(tipo_confirmacion, 'Viaje '+tipo_confirmacion[:-1]+'do exitosamente')
            if(tipo_confirmacion == "reservar"):
                if self.reservar_asientos(data,base,lista_viajes):
                    showinfo(tipo_confirmacion, 'Asiento/s reservado/s exitosamente')
                else:
                    error = ErrorFaltaAsientos()
                    error.registrar_error()
        else:
            showinfo('No '+tipo_confirmacion, 'Volver a la pantalla principal')
        info.set("")
    
    def eliminar_por_id(self,id_buscar,base,lista_viajes):
        if not self.validar_id_chofer(id_buscar):
            return False
        else:
            base.eliminar_por_id_BD(id_buscar)
            for viaje in lista_viajes:
                if(viaje[1][4]==id_buscar):
                    viaje[0].destroy()
                    return True
            return False

    
    def reservar_asientos(self,data,base,lista_viajes):
        cant_asientos = data
        for viaje in lista_viajes:
            if(self.ventanita.id_boton_seleccionado == viaje[1][4]):
                if(viaje[1][3] > cant_asientos):
                        viaje[1][3] -= cant_asientos
                        base.actualizar_asientos_viaje(viaje[1][3], viaje[1][4])
                        return True
                else:
                    print(cant_asientos)
                    print(viaje[1][3])
                    if viaje[1][3] == cant_asientos:
                        lista_viajes.remove(viaje)
                        self.eliminar_por_id(viaje[1][4],base,lista_viajes)
                        viaje[0].destroy()
                        self.ventanita.viaje_seleccionado = False
                        return True
                    else :
                        return False
    def validar_id_chofer(self,id_chofer):
        patron = r"^\d{4}$"
        if re.match(patron, str(id_chofer)):
            return True
        else:
            return False

class Boton_Filtrar(Posicion_Widget):
    def __init__(self,frame,texto,fuente,color,origen,destino,fecha,fila,columna,ancho=None,lista_viajes=None):
        self.boton = Button (frame,text=texto,font=fuente,bg=color,width=ancho,command = lambda : self.filtrar(origen,destino,fecha,lista_viajes))
        super().colocar_widget(self.boton,fila,columna)
    
    def filtrar(self,ori,dest,fec,lista_viajes):
        origen = ori.get()
        destino = dest.get()
        fecha = fec.get()
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

class ErrorFaltaAsientos(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: no hay suficientes asientos disponibles")

class ErrorFechaInvalida(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: la fecha ingresada no es valida. La fecha debe tener formato DD-MM-AAAA")

class ErrorIDInvalido(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: el ID ingresado no es valido. El ID debe tener cuatro digitos")

class ErrorIDRepetido(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: el ID ingresado ya existe")

class ErrorCiudadInvalida(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: el origen o destino no es valido.")

class ErrorBaseDatos(Exception):
    def registrar_error(self):
        messagebox.showerror("Error","Error: no se pudo registrar la operacio, vuelva a intentarlo")
