from tkinter import *
from tkinter import ttk

import psycopg2

def conectarABaseDeDatos():
    return psycopg2.connect(
                                dbname = "refugios",
                                user = "postgres",
                                password = "",
                                host = "localhost",
                                port = "5432")



'''-------------------PROCEDIMIENTOS PARA REFUGIOS---------------------------'''
#------------------Actualizacion de la tabla refugios-------------------------------
def actualizarTablaRefugio():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaRefugios.delete(*tablaRefugios.get_children())
    query = '''select * from refugio'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (id_refugio, direccion,cantidad_perros) in row:
        tablaRefugios.insert('',0,text=id_refugio, values= (str(direccion),cantidad_perros))
    coneccion.commit()
    coneccion.close()

#------------------Ventana insercion-refugios------------------------------
def guardarRefugio(direccion):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO refugio (direccion) VALUES(%s)'''
    cursor.execute(query, (direccion,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaRefugio()

def insertarRefugio():
    ins_refugio = Tk()
    ins_refugio.title("Insertar refugio")
    ins_refugio.resizable(0,0)

    can_ins_v = Canvas(ins_refugio, height = "150", width = "245") 
    can_ins_v.pack()

    frame =  Frame(ins_refugio)
    frame.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    texto = Label(frame, text="\nIngrese los datos del refugio")
    texto.grid(row=0, column = 0,padx= 0, pady=6,columnspan=2)
    
    lb_nombre = Label(frame, text = "Dirección")
    lb_nombre.grid(row=1, column = 0,padx= 0, pady=6)

    entrada_refugio = Entry(frame)
    entrada_refugio.grid(row = 1, column = 1,padx= 0, pady=6)

    boton_insertar = Button(frame, text="Agregar", command = lambda:guardarRefugio(entrada_refugio.get()))
    boton_insertar.grid(row=2,column=1,sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ins_refugio.mainloop()
    
#------------------Ventana actualizacion-refugios--------------------------
def actualizarRefugio(id,nuevaDireccion,ventanaActRef):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE refugio SET direccion=%s WHERE ID_refugio=%s'''
    cursor.execute(query, (nuevaDireccion,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActRef.destroy()
    actualizarTablaRefugio()

def ventanaActualizarRefuigio():
    try:
        tablaRefugios.item(tablaRefugios.selection())['values'][0]
    except IndexError:
        return
    id= tablaRefugios.item(tablaRefugios.selection())['text']
    direccionVieja= tablaRefugios.item(tablaRefugios.selection())['values'][0]

    actualizar_refugio = Tk()
    actualizar_refugio.title("Actualizar Refugio")
    actualizar_refugio.resizable(0,0)

    canvasActualizarRefugio= Canvas(actualizar_refugio, height = "130", width = "300")
    canvasActualizarRefugio.pack()

    FrameActualizarRefugio = Frame(actualizar_refugio)
    FrameActualizarRefugio.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDRefugio= Label(FrameActualizarRefugio, text="ID Refugio")
    labelIDRefugio.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDRefugio= Entry(FrameActualizarRefugio,textvariable= StringVar(actualizar_refugio, value=id),state='readonly')
    entryIDRefugio.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelDireccionRefugio= Label(FrameActualizarRefugio, text='Dirección')
    labelDireccionRefugio.grid(row=2, column = 0,padx= 0, pady=6)
    entryDireccionRefugio= Entry(FrameActualizarRefugio,textvariable= StringVar(actualizar_refugio, value=direccionVieja))
    entryDireccionRefugio.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    boton_actualizarRefugio = Button(FrameActualizarRefugio, text="Actualizar", command = lambda:actualizarRefugio(id,entryDireccionRefugio.get(),actualizar_refugio))
    boton_actualizarRefugio.grid(row=3,column=1,sticky=W+E)
    actualizar_refugio.mainloop()

#------------------Ventana eliminacion-refugios----------------------------
def EliminarRefugio():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaRefugios.item(tablaRefugios.selection())['values'][0]
    except IndexError:
        return
    id= tablaRefugios.item(tablaRefugios.selection())['text']
    query= '''DELETE FROM refugio WHERE ID_refugio=%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaRefugio()

#------------------Ventana busqueda-refugios-------------------------------
def busquedaRefugio(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM refugio WHERE ID_refugio=%s'''
    cursor.execute(query, (id,))
    refugioEncontrado= cursor.fetchone()
    listboxBusRefugio= Listbox(frame,width= 20, height=1)
    listboxBusRefugio.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusRefugio.insert(END,refugioEncontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarRefugio():
    bus_refugio = Tk()
    bus_refugio.title("Buscar Refugio")
    bus_refugio.resizable(0,0)

    canvasBuscarRefugio= Canvas(bus_refugio, height = "170", width = "260")
    canvasBuscarRefugio.pack()

    FrameBuscarRefugio = Frame(bus_refugio)
    FrameBuscarRefugio.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarRefugio = Label(FrameBuscarRefugio, text="Ingrese los datos de búsqueda")
    labelBuscarRefugio.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelIdBusRefugio = Label(FrameBuscarRefugio, text = "ID Refugio")
    labelIdBusRefugio.grid(row=1, column = 0,padx= 0, pady=6)

    entryBuscarRefugio= Entry(FrameBuscarRefugio)
    entryBuscarRefugio.grid(row = 1, column = 1,padx= 0, pady=6)

    listboxBusRefugio= Listbox(FrameBuscarRefugio,width= 20, height=1)
    listboxBusRefugio.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarRefugio = Button(FrameBuscarRefugio, text="Buscar",command=lambda:busquedaRefugio(FrameBuscarRefugio,entryBuscarRefugio.get()))
    botonBuscarRefugio.grid(row=2,column=1,sticky=W+E)
    botonBuscarRefugio.config(cursor="hand2")
    bus_refugio.mainloop()



'''-------------------PROCEDIMIENTOS PARA PATROCINIOS------------------------'''
#------------------Ventana insercion-patrocinios------------------------------
def actualizarTablaPatrocinios():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaPatrocinios.delete(*tablaPatrocinios.get_children())
    query = '''SELECT * FROM patrocinios'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (id_patrocinador, id_refugio,id_patrocinio) in row:
        tablaPatrocinios.insert(parent="",index="end", text=id_patrocinio,values=(id_refugio,id_patrocinador))
    coneccion.commit()
    coneccion.close()

def guardarPatrocinios(id_patrocinador, id_refugio):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO patrocinios VALUES(%s, %s)'''
    cursor.execute(query, (id_patrocinador, id_refugio))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPatrocinios()

def insertarPatrocinios():
    ven_insertar = Tk()
    ven_insertar.title("Insertar patrocinios")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("350x160")

    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0, columnspan=2)
    lb_id_patrocinador = Label(ven_insertar, text="ID del patrocinador")

    lb_id_patrocinador.grid(row=1, column=0, padx=5, pady=5)
    entrada_id_patrocinador = Entry(ven_insertar)
    entrada_id_patrocinador.grid(row=1, column=1)

    lb_id_refugio = Label(ven_insertar, text="ID del refugio")
    lb_id_refugio.grid(row=2, column=0, padx=5, pady=5)
    entrada_id_refugio = Entry(ven_insertar)
    entrada_id_refugio.grid(row=2, column=1)

    boton_insertar = Button(ven_insertar,
                            text="Agregar",
                            command=lambda:guardarPatrocinios(entrada_id_patrocinador.get(),
                                                            entrada_id_refugio.get()))
    boton_insertar.grid(row=3, column=1,sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()
#------------------Ventana actualizacion-patrocinios--------------------------
def actualizarPatrocinio(id,nuevoIDPatrocinador,nuevoIDRefugio,ventanaActPatri):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE patrocinios SET id_patrocinador=%s, id_refugio  =%s WHERE id_patrocinio=%s'''
    cursor.execute(query, (nuevoIDPatrocinador,nuevoIDRefugio,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActPatri.destroy()
    actualizarTablaPatrocinios()

def ventanaActualizarPatrocinio():
    try:
        tablaPatrocinios.item(tablaPatrocinios.selection())['values'][0]
    except IndexError:
        return
    id= tablaPatrocinios.item(tablaPatrocinios.selection())['text']
    IDRefugioViejo= tablaPatrocinios.item(tablaPatrocinios.selection())['values'][0]
    IDPatrocinadorViejo= tablaPatrocinios.item(tablaPatrocinios.selection())['values'][1]
    
    actualizar_patrocinio = Tk()
    actualizar_patrocinio.title("Actualizar Patrocinio")
    actualizar_patrocinio.resizable(0,0)

    canvasActualizarPatrocinio= Canvas(actualizar_patrocinio, height = "160", width = "310")
    canvasActualizarPatrocinio.pack()

    FrameActualizarPatrocinio = Frame(actualizar_patrocinio)
    FrameActualizarPatrocinio.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDPatrocinio= Label(FrameActualizarPatrocinio, text="ID Patrocinador")
    labelIDPatrocinio.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDPatrocinio= Entry(FrameActualizarPatrocinio,textvariable= StringVar(actualizar_patrocinio, value=id),state='readonly')
    entryIDPatrocinio.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIDRefugio= Label(FrameActualizarPatrocinio, text='ID Refugio')
    labelIDRefugio.grid(row=2, column = 0,padx= 0, pady=6)
    entryIDRefugio= Entry(FrameActualizarPatrocinio,textvariable= StringVar(actualizar_patrocinio, value=IDRefugioViejo))
    entryIDRefugio.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIDPatrocinador= Label(FrameActualizarPatrocinio, text='ID Patrocinador')
    labelIDPatrocinador.grid(row=6, column = 0,padx= 0, pady=6)
    entryIDPatrocinador= Entry(FrameActualizarPatrocinio,textvariable= StringVar(actualizar_patrocinio, value=IDPatrocinadorViejo))
    entryIDPatrocinador.grid(row=6, column = 1,padx= 0, pady=6, sticky=W+E)


    boton_actualizarPatrocinio = Button(FrameActualizarPatrocinio, text="Actualizar",
                                        command = lambda:actualizarPatrocinio(id,
                                        entryIDPatrocinador.get(),
                                        entryIDRefugio.get(),
                                        actualizar_patrocinio))
    
    boton_actualizarPatrocinio.grid(row=8,column=1,sticky=W+E)
    actualizar_patrocinio.mainloop()

#------------------Ventana eliminacion-patrocinios----------------------------
def EliminarPatrocinio():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaPatrocinios.item(tablaPatrocinios.selection())['values'][0]
    except IndexError:
        return
    id= tablaPatrocinios.item(tablaPatrocinios.selection())['text']
    query= '''DELETE FROM patrocinios WHERE id_patrocinio =%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPatrocinios()

#------------------Ventana busqueda-patrocinios-------------------------------
def busquedaPatrocinio(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM patrocinios WHERE id_patrocinio=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusPatrocinio= Listbox(frame,width= 20, height=1)
    listboxBusPatrocinio.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusPatrocinio.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarPatrocinio():
    bus_Patrocinio = Tk()
    bus_Patrocinio.title("Buscar Patrocinio")
    bus_Patrocinio.resizable(0,0)

    canvasBuscarPatrocinio= Canvas(bus_Patrocinio, height = "160", width = "300")
    canvasBuscarPatrocinio.pack()

    FrameBuscarPatrocinio = Frame(bus_Patrocinio)
    FrameBuscarPatrocinio.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarPatrocinio = Label(FrameBuscarPatrocinio, text="Ingrese los datos de búsqueda")
    labelBuscarPatrocinio.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelIdBusPatrocinio = Label(FrameBuscarPatrocinio, text = "ID Patrocinio")
    labelIdBusPatrocinio.grid(row=1, column = 0,padx= 0, pady=6)

    entryBuscarPatrocinio= Entry(FrameBuscarPatrocinio)
    entryBuscarPatrocinio.grid(row = 1, column = 1,padx= 0, pady=6)

    listboxBusPatrocinio= Listbox(FrameBuscarPatrocinio,width= 20, height=1)
    listboxBusPatrocinio.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarPatrocinio = Button(FrameBuscarPatrocinio, text="Buscar",command=lambda:busquedaPatrocinio(FrameBuscarPatrocinio,entryBuscarPatrocinio.get()))
    botonBuscarPatrocinio.grid(row=2,column=1,sticky=W+E)
    botonBuscarPatrocinio.config(cursor="hand2")
    bus_Patrocinio.mainloop()


'''-------------------PROCEDIMIENTOS PARA PATROCINADORES---------------------'''
#------------------Ventana insercion-patrocinadores------------------------------
def actualizarTablaPatrocinadores():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaPatrocinadores.delete(*tablaPatrocinadores.get_children())
    query = '''SELECT * FROM patrocinador'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (nombre, telefono, id_patrocinador) in row:
        tablaPatrocinadores.insert(parent="",index="end", text=id_patrocinador,values=(nombre, telefono))
    coneccion.commit()
    coneccion.close()

def guardarPatrocinador(nombre, telefono):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO patrocinador VALUES(%s, %s)'''
    cursor.execute(query, (nombre, telefono))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPatrocinadores()

def insertarPatrocinador():
    ven_insertar = Tk()
    ven_insertar.title("Insertar patrocinador")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("280x150")
    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0,columnspan=2)
    lb_nombre = Label(ven_insertar, text="Nombre")

    lb_nombre.grid(row=1, column=0, padx=5, pady=5)
    entrada_nombre = Entry(ven_insertar)
    entrada_nombre.grid(row=1, column=1)

    lb_telefono = Label(ven_insertar, text="Teléfono")
    lb_telefono.grid(row=2, column=0, padx=5, pady=5)
    entrada_telefono = Entry(ven_insertar)
    entrada_telefono.grid(row=2, column=1)

    boton_insertar = Button(ven_insertar,
                            text="Agregar",
                            command=lambda:guardarPatrocinador(entrada_nombre.get(),
                                                            entrada_telefono.get()))
    boton_insertar.grid(row=3, column=1,sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()

#------------------Ventana actualizacion-patrocinadores--------------------------
def actualizarPatrocinador(id,nuevoNombre,nuevoTelefono,ventanaActPatr):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE patrocinador SET nombre=%s,telefono=%s WHERE id_patrocinador=%s'''
    cursor.execute(query, (nuevoNombre,nuevoTelefono,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActPatr.destroy()
    actualizarTablaPatrocinadores()

def ventanaActualizarPatrocinador():
    try:
        tablaPatrocinadores.item(tablaPatrocinadores.selection())['values'][0]
    except IndexError:
        return
    id= tablaPatrocinadores.item(tablaPatrocinadores.selection())['text']
    nombreViejo= tablaPatrocinadores.item(tablaPatrocinadores.selection())['values'][0]
    telefonoViejo= tablaPatrocinadores.item(tablaPatrocinadores.selection())['values'][1]
    
    actualizar_patrocinador = Tk()
    actualizar_patrocinador.title("Actualizar Patrocinador")
    actualizar_patrocinador.resizable(0,0)

    canvasActualizarPatrocinador= Canvas(actualizar_patrocinador, height = "185", width = "300")
    canvasActualizarPatrocinador.pack()

    FrameActualizarPatrocinador = Frame(actualizar_patrocinador)
    FrameActualizarPatrocinador.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDPatrocinador= Label(FrameActualizarPatrocinador, text="ID Patrocinador")
    labelIDPatrocinador.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDPatrocinador= Entry(FrameActualizarPatrocinador,textvariable= StringVar(actualizar_patrocinador, value=id),state='readonly')
    entryIDPatrocinador.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelNombrePatrocinador= Label(FrameActualizarPatrocinador, text='Nombre')
    labelNombrePatrocinador.grid(row=2, column = 0,padx= 0, pady=6)
    entryNombrePatrocinador= Entry(FrameActualizarPatrocinador,textvariable= StringVar(actualizar_patrocinador, value=nombreViejo))
    entryNombrePatrocinador.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelTelefonoPatrocinador= Label(FrameActualizarPatrocinador, text='Télefono')
    labelTelefonoPatrocinador.grid(row=6, column = 0,padx= 0, pady=6)
    entryTelefonoPatrocinador= Entry(FrameActualizarPatrocinador,textvariable= StringVar(actualizar_patrocinador, value=telefonoViejo))
    entryTelefonoPatrocinador.grid(row=6, column = 1,padx= 0, pady=6, sticky=W+E)


    boton_actualizarPatrocinador = Button(FrameActualizarPatrocinador, text="Actualizar",
                                        command = lambda:actualizarPatrocinador(id,
                                        entryNombrePatrocinador.get(),
                                        entryTelefonoPatrocinador.get(),
                                        actualizar_patrocinador))
    
    boton_actualizarPatrocinador.grid(row=8,column=1,sticky=W+E)
    actualizar_patrocinador.mainloop()

#------------------Ventana eliminacion-patrocinadores----------------------------
def EliminarPatrocinador():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaPatrocinadores.item(tablaPatrocinadores.selection())['values'][0]
    except IndexError:
        return
    id= tablaPatrocinadores.item(tablaPatrocinadores.selection())['text']
    query= '''DELETE FROM patrocinador WHERE id_patrocinador =%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPatrocinadores()

#------------------Ventana busqueda-patrocinadores-------------------------------
def busquedaPatrocinadores(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM patrocinador WHERE id_patrocinador=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusPatrocinador= Listbox(frame,width=40, height=1)
    listboxBusPatrocinador.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusPatrocinador.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarPatrocinador():
    bus_Patrocinador = Tk()
    bus_Patrocinador.title("Buscar Patrocinador")
    bus_Patrocinador.resizable(0,0)

    canvasBuscarPatrocinador= Canvas(bus_Patrocinador, height = "160", width = "500")
    canvasBuscarPatrocinador.pack()

    FrameBuscarPatrocinador = Frame(bus_Patrocinador)
    FrameBuscarPatrocinador.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarPatrocinador= Label(FrameBuscarPatrocinador, text="Ingrese los datos de búsqueda")
    labelBuscarPatrocinador.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelBuscarIDPatrocinador = Label(FrameBuscarPatrocinador, text = "ID Patrocinador")
    labelBuscarIDPatrocinador.grid(row=1, column = 0,padx= 0, pady=6,sticky=E)

    entryBuscarPatrocinador= Entry(FrameBuscarPatrocinador)
    entryBuscarPatrocinador.grid(row = 1, column = 1,padx= 0, pady=6,sticky=W+E)

    listboxBusPatrocinador= Listbox(FrameBuscarPatrocinador,width=50, height=1)
    listboxBusPatrocinador.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarPatrocinador = Button(FrameBuscarPatrocinador, text="Buscar",command=lambda:busquedaPatrocinadores(FrameBuscarPatrocinador,entryBuscarPatrocinador.get()))
    botonBuscarPatrocinador.grid(row=2,column=1,sticky=W+E)
    botonBuscarPatrocinador.config(cursor="hand2")
    bus_Patrocinador.mainloop()


'''-------------------PROCEDIMIENTOS PARA VOLUNTARIOS------------------------'''
#------------------Ventana insercion-voluntarios---------------------------
def actualizarTablaVoluntario():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaVoluntarios.delete(*tablaVoluntarios.get_children())
    query = '''SELECT * FROM voluntario'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (nombre,apellido,fecha_registro,fecha_nacimiento,telefono,id_refugio,id_voluntario) in row:
        tablaVoluntarios.insert(parent="",
                                index="end",
                                text=id_voluntario,
                                values=(nombre, apellido, fecha_registro, fecha_nacimiento, telefono, id_refugio))
    coneccion.commit()
    coneccion.close()

def guardarVoluntario(nombre, apellido, fecha_registro, fecha_nacimiento, telefono, id_refugio):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO voluntario VALUES(%s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (nombre, apellido, fecha_registro, fecha_nacimiento, telefono, id_refugio))
    coneccion.commit()
    coneccion.close()
    actualizarTablaVoluntario()

def insertarVoluntario():
    ven_insertar = Tk()
    ven_insertar.title("Insertar voluntario")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("350x315")
    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0,columnspan=2)
    lb_nombre = Label(ven_insertar, text="Nombre")

    lb_nombre.grid(row=1, column=0, padx=5, pady=5)
    entrada_nombre = Entry(ven_insertar)
    entrada_nombre.grid(row=1, column=1)

    lb_apellido = Label(ven_insertar, text="Apellido")
    lb_apellido.grid(row=2, column=0, padx=5, pady=5)
    entrada_apellido = Entry(ven_insertar)
    entrada_apellido.grid(row=2, column=1)

    lb_fecha_registro = Label(ven_insertar, text="Fecha de registro")
    lb_fecha_registro.grid(row=3, column=0, padx=5, pady=5)
    entrada_fecha_registro = Entry(ven_insertar)
    entrada_fecha_registro.grid(row=3, column=1)

    lb_fecha_nacimiento = Label(ven_insertar, text="Fecha  de nacimiento")
    lb_fecha_nacimiento.grid(row=4, column=0, padx=5, pady=5)
    entrada_fecha_nacimiento = Entry(ven_insertar)
    entrada_fecha_nacimiento.grid(row=4, column=1)

    lb_telefono = Label(ven_insertar, text="Teléfono")
    lb_telefono.grid(row=5, column=0, padx=5, pady=5)
    entrada_telefono = Entry(ven_insertar)
    entrada_telefono.grid(row=5, column=1)

    lb_id_refugio = Label(ven_insertar, text="ID del refugio")
    lb_id_refugio.grid(row=6, column=0, padx=5, pady=5)
    entrada_id_refugio = Entry(ven_insertar)
    entrada_id_refugio.grid(row=6, column=1)


    boton_insertar = Button(ven_insertar,
                            text="Agregar",
                            command=lambda:guardarVoluntario(entrada_nombre.get(),
                                                            entrada_apellido.get(),
                                                            entrada_fecha_registro.get(),
                                                            entrada_fecha_nacimiento.get(),
                                                            entrada_telefono.get(),
                                                            entrada_id_refugio.get()))
    boton_insertar.grid(row=7, column=1,sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()

#------------------Ventana actualizacion-voluntarios--------------------------
def actualizarVoluntario(id,nuevoNombre,nuevoApellido,nuevaFechaReg,nuevaFechaNac,
                         nuevoTelefono,nuevoRefugio,ventanaActVol):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE voluntario SET nombre=%s,
                                    apellido=%s,
                                    fecha_registro=%s,
                                    fecha_nacimiento=%s,
                                    telefono=%s,
                                    id_refugio=%s 
                                    WHERE id_voluntario=%s'''
    cursor.execute(query, (nuevoNombre,nuevoApellido,nuevaFechaReg,nuevaFechaNac,
                         nuevoTelefono,nuevoRefugio,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActVol.destroy()
    actualizarTablaVoluntario()

def ventanaActualizarVoluntario():
    try:
        tablaVoluntarios.item(tablaVoluntarios.selection())['values'][0]
    except IndexError:
        return
    id= tablaVoluntarios.item(tablaVoluntarios.selection())['text']
    nombreViejo= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][0]
    apellidoViejo= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][1]
    fechaRegVieja= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][2]
    fechaNacVieja= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][3]
    telefonoViejo= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][4]
    idRefugiViejo= tablaVoluntarios.item(tablaVoluntarios.selection())['values'][5]

    actualizar_voluntario = Tk()
    actualizar_voluntario.title("Actualizar Voluntario")
    actualizar_voluntario.resizable(0,0)

    canvasActualizarVoluntario= Canvas(actualizar_voluntario, height = "320", width = "300")
    canvasActualizarVoluntario.pack()

    FrameActualizarVoluntario = Frame(actualizar_voluntario)
    FrameActualizarVoluntario.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDVoluntario= Label(FrameActualizarVoluntario, text="ID Voluntario")
    labelIDVoluntario.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=id),state='readonly')
    entryIDVoluntario.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelNombreVoluntario= Label(FrameActualizarVoluntario, text='Nombre')
    labelNombreVoluntario.grid(row=2, column = 0,padx= 0, pady=6)
    entryNombreVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=nombreViejo))
    entryNombreVoluntario.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelApellidoVoluntario= Label(FrameActualizarVoluntario, text='Apellido')
    labelApellidoVoluntario.grid(row=3, column = 0,padx= 0, pady=6)
    entryApellidoVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=apellidoViejo))
    entryApellidoVoluntario.grid(row=3, column = 1,padx= 0, pady=6, sticky=W+E)

    labelfechaRegVoluntario= Label(FrameActualizarVoluntario, text='Fecha registro')
    labelfechaRegVoluntario.grid(row=4, column = 0,padx= 0, pady=6)
    entryfechaRegVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=fechaRegVieja))
    entryfechaRegVoluntario.grid(row=4, column = 1,padx= 0, pady=6, sticky=W+E)

    labelfechaNacVoluntario= Label(FrameActualizarVoluntario, text='Fecha nacimiento')
    labelfechaNacVoluntario.grid(row=5, column = 0,padx= 0, pady=6)
    entryfechaNacVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=fechaNacVieja))
    entryfechaNacVoluntario.grid(row=5, column = 1,padx= 0, pady=6, sticky=W+E)
    
    labelTelefonoVoluntario= Label(FrameActualizarVoluntario, text='Télefono')
    labelTelefonoVoluntario.grid(row=6, column = 0,padx= 0, pady=6)
    entryTelefonoVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=telefonoViejo))
    entryTelefonoVoluntario.grid(row=6, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIDRefugioVoluntario= Label(FrameActualizarVoluntario, text='ID Refugio')
    labelIDRefugioVoluntario.grid(row=7, column = 0,padx= 0, pady=6)
    entryIDRefugioVoluntario= Entry(FrameActualizarVoluntario,textvariable= StringVar(actualizar_voluntario, value=idRefugiViejo))
    entryIDRefugioVoluntario.grid(row=7, column = 1,padx= 0, pady=6, sticky=W+E)

    boton_actualizarVoluntario = Button(FrameActualizarVoluntario, text="Actualizar",
                                        command = lambda:actualizarVoluntario(id,
                                        entryNombreVoluntario.get(),
                                        entryApellidoVoluntario.get(),
                                        entryfechaRegVoluntario.get(),
                                        entryfechaNacVoluntario.get(),
                                        entryTelefonoVoluntario.get(),
                                        entryIDRefugioVoluntario.get(),
                                        actualizar_voluntario))
    
    boton_actualizarVoluntario.grid(row=8,column=1,sticky=W+E)
    actualizar_voluntario.mainloop()

#------------------Ventana eliminacion-voluntarios----------------------------
def EliminarVoluntario():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaVoluntarios.item(tablaVoluntarios.selection())['values'][0]
    except IndexError:
        return
    id= tablaVoluntarios.item(tablaVoluntarios.selection())['text']
    query= '''DELETE FROM voluntario WHERE id_voluntario=%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaVoluntario()

#------------------Ventana busqueda-voluntarios-------------------------------
def busquedaVoluntario(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM voluntario WHERE id_voluntario=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusVoluntario= Listbox(frame,width=40, height=1)
    listboxBusVoluntario.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusVoluntario.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarVoluntario():
    bus_Voluntario = Tk()
    bus_Voluntario.title("Buscar Voluntario")
    bus_Voluntario.resizable(0,0)

    canvasBuscarVoluntario= Canvas(bus_Voluntario, height = "160", width = "475")
    canvasBuscarVoluntario.pack()

    FrameBuscarVoluntario = Frame(bus_Voluntario)
    FrameBuscarVoluntario.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarVoluntario = Label(FrameBuscarVoluntario, text="Ingrese los datos de búsqueda")
    labelBuscarVoluntario.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelIdBusVoluntario = Label(FrameBuscarVoluntario, text = "ID Voluntario")
    labelIdBusVoluntario.grid(row=1, column = 0,padx= 0, pady=6,sticky=E)

    entryBuscarVoluntario= Entry(FrameBuscarVoluntario)
    entryBuscarVoluntario.grid(row = 1, column = 1,padx= 0, pady=6,sticky=E+W)

    listboxBusVoluntario= Listbox(FrameBuscarVoluntario,width=50, height=1)
    listboxBusVoluntario.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarVoluntario = Button(FrameBuscarVoluntario, text="Buscar",command=lambda:busquedaVoluntario(FrameBuscarVoluntario,entryBuscarVoluntario.get()))
    botonBuscarVoluntario.grid(row=2,column=1,sticky=W+E)
    botonBuscarVoluntario.config(cursor="hand2")
    bus_Voluntario.mainloop()



'''-------------------PROCEDIMIENTOS PARA PERROS-----------------------------'''
#------------------Ventana insercion-perros------------------------------
def actualizarTablaPerro():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaPerros.delete(*tablaPerros.get_children())
    query = '''SELECT * FROM perro'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (adoptado,raza,edad,nombre,fecha_ingreso,id_refugio,id_perro) in row:
        tablaPerros.insert(parent="",
                                index="end",
                                text=id_perro,
                                values=(adoptado,nombre,fecha_ingreso,raza,edad,id_refugio))
    coneccion.commit()
    coneccion.close()

def guardarPerro(adoptado,raza,edad,nombre,fecha_ingreso,id_refugio):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO perro VALUES(%s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (adoptado,raza,edad,nombre,fecha_ingreso,id_refugio))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPerro()

def insertarPerro():
    ven_insertar = Tk()
    ven_insertar.title("Insertar perro")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("315x290")

    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0, columnspan=2)
    
    lb_nombre = Label(ven_insertar, text="Nombre")
    lb_nombre.grid(row=1, column=0, padx=5, pady=5)
    entrada_nombre = Entry(ven_insertar)
    entrada_nombre.grid(row=1, column=1)

    lb_adoptado = Label(ven_insertar, text="Adoptado")
    lb_adoptado.grid(row=2, column=0, padx=5, pady=5)
    entrada_adoptado = Entry(ven_insertar)
    entrada_adoptado.grid(row=2, column=1)

    lb_fecha_ingreso = Label(ven_insertar, text="Fecha de ingreso")
    lb_fecha_ingreso.grid(row=3, column=0, padx=5, pady=5)
    entrada_fecha_ingreso = Entry(ven_insertar)
    entrada_fecha_ingreso.grid(row=3, column=1)

    lb_raza = Label(ven_insertar, text="Raza")
    lb_raza.grid(row=4, column=0, padx=5, pady=5)
    entrada_raza = Entry(ven_insertar)
    entrada_raza.grid(row=4, column=1)

    lb_edad = Label(ven_insertar, text="Edad")
    lb_edad.grid(row=5, column=0, padx=5, pady=5)
    entrada_edad = Entry(ven_insertar)
    entrada_edad.grid(row=5, column=1)

    lb_id_refugio = Label(ven_insertar, text="ID del refugio")
    lb_id_refugio.grid(row=6, column=0, padx=5, pady=5)
    entrada_id_refugio = Entry(ven_insertar)
    entrada_id_refugio.grid(row=6, column=1)


    boton_insertar = Button(ven_insertar,
                            text="Agregar",
                            command=lambda:guardarPerro(entrada_adoptado.get(),
                                                            entrada_raza.get(),
                                                            entrada_edad.get(),
                                                            entrada_nombre.get(),
                                                            entrada_fecha_ingreso.get(),
                                                            entrada_id_refugio.get()))
    boton_insertar.grid(row=7, column=1, sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()

#------------------Ventana actualizacion-perros--------------------------
def actualizarPerro(id,estadoAdopcion,nuevoNombre,nuevaFechaIngreso,nuevaRaza,nuevaEdad,nuevoIDRefugio,ventanaActPerro):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE perro SET adoptado=%s,
                                raza=%s,
                                edad=%s,
                                nombre=%s,
                                fecha_ingreso=%s, 
                                id_refugio=%s
                                WHERE id_perro=%s'''
    cursor.execute(query, (estadoAdopcion,nuevaRaza,nuevaEdad,nuevoNombre,nuevaFechaIngreso,nuevoIDRefugio,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActPerro.destroy()
    actualizarTablaPerro()

def ventanaActualizarPerro():
    try:
        tablaPerros.item(tablaPerros.selection())['values'][0]
    except IndexError:
        return
    id= tablaPerros.item(tablaPerros.selection())['text']
    estadoAdopcion= tablaPerros.item(tablaPerros.selection())['values'][0]
    nombreViejo= tablaPerros.item(tablaPerros.selection())['values'][1]
    fechaIngVieja= tablaPerros.item(tablaPerros.selection())['values'][2]
    razaVieja= tablaPerros.item(tablaPerros.selection())['values'][3]
    edadVieja= tablaPerros.item(tablaPerros.selection())['values'][4]
    idRefugioViejo= tablaPerros.item(tablaPerros.selection())['values'][5]

    actualizar_perro = Tk()
    actualizar_perro.title("Actualizar Perro")
    actualizar_perro.resizable(0,0)

    canvasActualizarPerro= Canvas(actualizar_perro, height = "320", width = "300")
    canvasActualizarPerro.pack()

    FrameActualizarPerro = Frame(actualizar_perro)
    FrameActualizarPerro.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDPerro= Label(FrameActualizarPerro, text="ID Perro")
    labelIDPerro.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDPerro= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=id),state='readonly')
    entryIDPerro.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelEstadoAdopcion= Label(FrameActualizarPerro, text='Adoptado')
    labelEstadoAdopcion.grid(row=2, column = 0,padx= 0, pady=6)
    entryEstadoAdopcion= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=estadoAdopcion))
    entryEstadoAdopcion.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelNombreViejo= Label(FrameActualizarPerro, text='Nombre')
    labelNombreViejo.grid(row=3, column = 0,padx= 0, pady=6)
    entryNombreViejo= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=nombreViejo))
    entryNombreViejo.grid(row=3, column = 1,padx= 0, pady=6, sticky=W+E)

    labelFechaIngVieja= Label(FrameActualizarPerro, text='Fecha Ingreso')
    labelFechaIngVieja.grid(row=4, column = 0,padx= 0, pady=6)
    entryFechaIngVieja= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=fechaIngVieja))
    entryFechaIngVieja.grid(row=4, column = 1,padx= 0, pady=6, sticky=W+E)

    labelRazaVieja= Label(FrameActualizarPerro, text='Raza')
    labelRazaVieja.grid(row=5, column = 0,padx= 0, pady=6)
    entryRazaVieja= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=razaVieja))
    entryRazaVieja.grid(row=5, column = 1,padx= 0, pady=6, sticky=W+E)
    
    labelEdadVieja= Label(FrameActualizarPerro, text='Edad')
    labelEdadVieja.grid(row=6, column = 0,padx= 0, pady=6)
    entryEdadVieja= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=edadVieja))
    entryEdadVieja.grid(row=6, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIDRefugioPerro= Label(FrameActualizarPerro, text='ID Refugio')
    labelIDRefugioPerro.grid(row=7, column = 0,padx= 0, pady=6)
    entryIDRefugioPerro= Entry(FrameActualizarPerro,textvariable= StringVar(actualizar_perro, value=idRefugioViejo))
    entryIDRefugioPerro.grid(row=7, column = 1,padx= 0, pady=6, sticky=W+E)

    boton_actualizarPerro = Button(FrameActualizarPerro, text="Actualizar",
                                        command = lambda:actualizarPerro(id,
                                        entryEstadoAdopcion.get(),
                                        entryNombreViejo.get(),
                                        entryFechaIngVieja.get(),
                                        entryRazaVieja.get(),
                                        entryEdadVieja.get(),
                                        entryIDRefugioPerro.get(),
                                        actualizar_perro))
    
    boton_actualizarPerro.grid(row=8,column=1,sticky=W+E)
    actualizar_perro.mainloop()

#------------------Ventana eliminacion-perros----------------------------
def EliminarPerro():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaPerros.item(tablaPerros.selection())['values'][0]
    except IndexError:
        return
    id= tablaPerros.item(tablaPerros.selection())['text']
    query= '''DELETE FROM perro WHERE id_perro =%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaPerro()

#------------------Ventana busqueda-perros-------------------------------

def busquedaPerro(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM perro WHERE id_perro=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusPerro= Listbox(frame,width=40, height=1)
    listboxBusPerro.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusPerro.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarPerro():
    bus_perro = Tk()
    bus_perro.title("Buscar Perro")
    bus_perro.resizable(0,0)

    canvasBuscarPerro= Canvas(bus_perro, height = "160", width = "475")
    canvasBuscarPerro.pack()

    FrameBuscarPerro = Frame(bus_perro)
    FrameBuscarPerro.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarPerro = Label(FrameBuscarPerro, text="Ingrese los datos de búsqueda")
    labelBuscarPerro.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelIdBusPerro= Label(FrameBuscarPerro, text = "ID Perro")
    labelIdBusPerro.grid(row=1, column = 0,padx= 0, pady=6,sticky=E)

    entryBuscarPerro= Entry(FrameBuscarPerro)
    entryBuscarPerro.grid(row = 1, column = 1,padx= 0, pady=6, sticky=W+E)

    listboxBusPerro= Listbox(FrameBuscarPerro,width=50, height=1)
    listboxBusPerro.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarPerro = Button(FrameBuscarPerro, text="Buscar",command=lambda:busquedaPerro(FrameBuscarPerro,entryBuscarPerro.get()))
    botonBuscarPerro.grid(row=2,column=1,sticky=W+E)
    botonBuscarPerro.config(cursor="hand2")
    bus_perro.mainloop()



'''-------------------PROCEDIMIENTOS PARA ADOPCIONES------------------------'''
#------------------Ventana insercion-adopciones------------------------------
def actualizarTablaAdopciones():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaAdopciones.delete(*tablaAdopciones.get_children())
    query = '''SELECT * FROM adopcion'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (id_adopcion, fecha_adopcion, id_refugio, id_perro, id_adoptante) in row:
        tablaAdopciones.insert(parent="",
                                index="end",
                                text=id_adopcion,
                                values=(fecha_adopcion, id_refugio, id_perro, id_adoptante))
    coneccion.commit()
    coneccion.close()

def guardarAdopcion(fecha_adopcion, id_refugio, id_perro, id_adoptante):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO adopcion (fecha_adopcion, id_refugio, id_perro, id_adoptante) VALUES(%s, %s, %s, %s)'''
    cursor.execute(query, (fecha_adopcion, id_refugio, id_perro, id_adoptante))
    coneccion.commit()
    coneccion.close()
    actualizarTablaAdopciones()

def insertarAdopcion():
    ven_insertar = Tk()
    ven_insertar.title("Insertar adopción")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("350x225")

    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0,columnspan=2)


    lb_id_refugio = Label(ven_insertar, text="ID del refugio")
    lb_id_refugio.grid(row=1, column=0, padx=5, pady=5)
    entrada_id_refugio = Entry(ven_insertar)
    entrada_id_refugio.grid(row=1, column=1)

    lb_id_perro = Label(ven_insertar, text="ID del perro")
    lb_id_perro.grid(row=2, column=0, padx=5, pady=5)
    entrada_id_perro = Entry(ven_insertar)
    entrada_id_perro.grid(row=2, column=1)

    lb_id_adoptante = Label(ven_insertar, text="ID del adoptante")
    lb_id_adoptante.grid(row=3, column=0, padx=5, pady=5)
    entrada_id_adoptante = Entry(ven_insertar)
    entrada_id_adoptante.grid(row=3, column=1)

    lb_fecha_adopcion = Label(ven_insertar, text="Fecha de adopción")
    lb_fecha_adopcion.grid(row=4, column=0, padx=10, pady=10)
    entrada_fecha_adopcion = Entry(ven_insertar)
    entrada_fecha_adopcion.grid(row=4, column=1)

    boton_insertar = Button(ven_insertar,text="Agregar",
                            command=lambda:guardarAdopcion(entrada_fecha_adopcion.get(),
                                                            entrada_id_refugio.get(),
                                                            entrada_id_perro.get(),
                                                            entrada_id_adoptante.get()))
    boton_insertar.grid(row=5, column=1, sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()
#------------------Ventana actualizacion-adopciones--------------------------
def actualizarAdopcion(id,nuevaFechaAdopcion,nuevoIdRefugio,nuevoIdPerro,nuevoIdAdoptante,ventanaActAdopcion):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE adopcion SET fecha_adopcion=%s, id_refugio=%s, id_perro=%s, id_adoptante=%s  WHERE id_adopcion=%s'''
    cursor.execute(query, (nuevaFechaAdopcion,nuevoIdRefugio,nuevoIdPerro,nuevoIdAdoptante,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActAdopcion.destroy()
    actualizarTablaAdopciones()

def ventanaActualizarAdopcion():
    try:
        tablaAdopciones.item(tablaAdopciones.selection())['values'][0]
    except IndexError:
        return
    id= tablaAdopciones.item(tablaAdopciones.selection())['text']
    FechaAdopcionVieja= tablaAdopciones.item(tablaAdopciones.selection())['values'][0]
    idRefugioViejo= tablaAdopciones.item(tablaAdopciones.selection())['values'][1]
    idPerroViejo= tablaAdopciones.item(tablaAdopciones.selection())['values'][2]
    idAdoptanteViejo= tablaAdopciones.item(tablaAdopciones.selection())['values'][3]

    actualizar_adopcion = Tk()
    actualizar_adopcion.title("Actualizar Adopción")
    actualizar_adopcion.resizable(0,0)

    canvasActualizarAdopcion= Canvas(actualizar_adopcion, height = "240", width = "325")
    canvasActualizarAdopcion.pack()
    FrameActualizarAdopcion = Frame(actualizar_adopcion)
    FrameActualizarAdopcion.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDAdopcion= Label(FrameActualizarAdopcion, text="ID Adopción")
    labelIDAdopcion.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDAdopcion= Entry(FrameActualizarAdopcion,textvariable= StringVar(actualizar_adopcion, value=id),state='readonly')
    entryIDAdopcion.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelFechaAdopcionVieja= Label(FrameActualizarAdopcion, text='Fecha Adopción')
    labelFechaAdopcionVieja.grid(row=2, column = 0,padx= 0, pady=6)
    entryFechaAdopcionVieja= Entry(FrameActualizarAdopcion,textvariable= StringVar(actualizar_adopcion, value=FechaAdopcionVieja))
    entryFechaAdopcionVieja.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIdRefugioViejo= Label(FrameActualizarAdopcion, text='ID Refugio')
    labelIdRefugioViejo.grid(row=3, column = 0,padx= 0, pady=6)
    entryIdRefugioViejo= Entry(FrameActualizarAdopcion,textvariable= StringVar(actualizar_adopcion, value=idRefugioViejo))
    entryIdRefugioViejo.grid(row=3, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIdPerroViejo= Label(FrameActualizarAdopcion, text='ID Perro')
    labelIdPerroViejo.grid(row=4, column = 0,padx= 0, pady=6)
    entryIdPerroViejo= Entry(FrameActualizarAdopcion,textvariable= StringVar(actualizar_adopcion, value=idPerroViejo))
    entryIdPerroViejo.grid(row=4, column = 1,padx= 0, pady=6, sticky=W+E)

    labelIdAdoptanteViejo= Label(FrameActualizarAdopcion, text='ID Adoptante')
    labelIdAdoptanteViejo.grid(row=5, column = 0,padx= 0, pady=6)
    entryIdAdoptanteViejo= Entry(FrameActualizarAdopcion,textvariable= StringVar(actualizar_adopcion, value=idAdoptanteViejo))
    entryIdAdoptanteViejo.grid(row=5, column = 1,padx= 0, pady=6, sticky=W+E)

    boton_actualizarAdopcion = Button(FrameActualizarAdopcion, text="Actualizar",
                                        command = lambda:actualizarAdopcion(id,
                                        entryFechaAdopcionVieja.get(),
                                        entryIdRefugioViejo.get(),
                                        entryIdPerroViejo.get(),
                                        entryIdAdoptanteViejo.get(),
                                        actualizar_adopcion))
    
    boton_actualizarAdopcion.grid(row=8,column=1,sticky=W+E)
    actualizar_adopcion.mainloop()

#------------------Ventana eliminacion-adopciones----------------------------
def EliminarAdopcion():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaAdopciones.item(tablaAdopciones.selection())['values'][0]
    except IndexError:
        return
    id= tablaAdopciones.item(tablaAdopciones.selection())['text']
    query= '''DELETE FROM adopcion WHERE id_adopcion=%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaAdopciones()

#------------------Ventana busqueda-adopciones-------------------------------
def busquedaAdopciones(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM adopcion WHERE id_adopcion=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusAdopcion= Listbox(frame,width=40, height=1)
    listboxBusAdopcion.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusAdopcion.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarAdopcion():
    bus_adopcion= Tk()
    bus_adopcion.title("Buscar Adopción")
    bus_adopcion.resizable(0,0)

    canvasBuscarAdopcion= Canvas(bus_adopcion, height = "160", width = "475")
    canvasBuscarAdopcion.pack()

    FrameBuscarAdopcion= Frame(bus_adopcion)
    FrameBuscarAdopcion.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarAdopcion = Label(FrameBuscarAdopcion, text="Ingrese los datos de búsqueda")
    labelBuscarAdopcion.grid(row=0, column = 0, columnspan=2,padx= 0, pady=6)

    labelIdBusAdopcion= Label(FrameBuscarAdopcion, text = "ID Adopción")
    labelIdBusAdopcion.grid(row=1, column = 0,padx= 0, pady=6,sticky=E)
    entryBuscarAdopcion= Entry(FrameBuscarAdopcion)
    entryBuscarAdopcion.grid(row = 1, column = 1,padx= 0, pady=6,sticky=W+E)

    listboxBusAdopcion= Listbox(FrameBuscarAdopcion,width=50, height=1)
    listboxBusAdopcion.grid(row=3,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarAdopcion = Button(FrameBuscarAdopcion, text="Buscar",command=lambda:busquedaAdopciones(FrameBuscarAdopcion,entryBuscarAdopcion.get()))
    botonBuscarAdopcion.grid(row=2,column=1,sticky=W+E)
    botonBuscarAdopcion.config(cursor="hand2")
    bus_adopcion.mainloop()




'''-------------------PROCEDIMIENTOS PARA ADOPTANTES------------------------'''
#------------------Actualizacion de la tabla adoptantes-------------------------------
def actualizarTablaAdoptantes():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    tablaAdoptantes.delete(*tablaAdoptantes.get_children())
    query = '''SELECT * FROM adoptante'''
    cursor.execute(query)
    row = cursor.fetchall()
    for (telefono, nombre, domicilio, id_adoptante) in row:
        tablaAdoptantes.insert(parent="",index="end", text=id_adoptante,values=(nombre, domicilio, telefono))
    coneccion.commit()
    coneccion.close()

#------------------Ventana insercion-adoptante------------------------------
def guardarAdoptante(telefono, nombre, domicilio):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''INSERT INTO adoptante VALUES(%s, %s, %s)'''
    cursor.execute(query, (telefono, nombre, domicilio))
    coneccion.commit()
    coneccion.close()
    actualizarTablaAdoptantes()

def insertarAdoptante():
    ven_insertar = Tk()
    ven_insertar.title("Insertar adoptante")
    ven_insertar.resizable(0,0)
    ven_insertar.geometry("315x180")

    lb_insertar = Label(ven_insertar, text="Ingrese los datos")
    lb_insertar.grid(row=0,column=0)
    lb_nombre = Label(ven_insertar, text="Nombre")

    lb_nombre.grid(row=1, column=0, padx=5, pady=5)
    entrada_nombre = Entry(ven_insertar)
    entrada_nombre.grid(row=1, column=1)

    lb_telefono = Label(ven_insertar, text="Teléfono")
    lb_telefono.grid(row=2, column=0, padx=5, pady=5)
    entrada_telefono = Entry(ven_insertar)
    entrada_telefono.grid(row=2, column=1)

    lb_domicilio = Label(ven_insertar, text="Domicilio")
    lb_domicilio.grid(row=3, column=0, padx=5, pady=5)
    entrada_domicilio = Entry(ven_insertar)
    entrada_domicilio.grid(row=3, column=1)

    boton_insertar = Button(ven_insertar, text="Agregar",
                            command=lambda:guardarAdoptante(entrada_telefono.get(),
                                                            entrada_nombre.get(),
                                                            entrada_domicilio.get()))
    boton_insertar.grid(row=4, column=1, sticky=W+E)
    boton_insertar.config(cursor="hand2")
    ven_insertar.mainloop()

#------------------Ventana actualizacion-adoptante--------------------------
def actualizarAdoptante(id,nuevoNombre,nuevoDomicilio,nuevoTelefono,ventanaActAdoptante):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query = '''UPDATE adoptante SET telefono =%s, nombre=%s, domicilio=%s WHERE id_adoptante =%s'''
    cursor.execute(query, (nuevoTelefono,nuevoNombre,nuevoDomicilio,id,))
    coneccion.commit()
    coneccion.close()
    ventanaActAdoptante.destroy()
    actualizarTablaAdoptantes()

def ventanaActualizarAdoptante():
    try:
        tablaAdoptantes.item(tablaAdoptantes.selection())['values'][0]
    except IndexError:
        return
    id= tablaAdoptantes.item(tablaAdoptantes.selection())['text']
    nombreViejo= tablaAdoptantes.item(tablaAdoptantes.selection())['values'][0]
    domicilioViejo= tablaAdoptantes.item(tablaAdoptantes.selection())['values'][1]
    telefonoViejo= tablaAdoptantes.item(tablaAdoptantes.selection())['values'][2]

    actualizar_adoptante = Tk()
    actualizar_adoptante.title("Actualizar Adoptante")
    actualizar_adoptante.resizable(0,0)

    canvasActualizarAdoptante= Canvas(actualizar_adoptante, height = "200", width = "280")
    canvasActualizarAdoptante.pack()

    FrameActualizarAdoptante = Frame(actualizar_adoptante)
    FrameActualizarAdoptante.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelIDAdoptante= Label(FrameActualizarAdoptante, text="ID Adoptante")
    labelIDAdoptante.grid(row=1, column = 0,padx= 0, pady=6)
    entryIDAdoptante= Entry(FrameActualizarAdoptante,textvariable= StringVar(actualizar_adoptante, value=id),state='readonly')
    entryIDAdoptante.grid(row=1, column = 1,padx= 0, pady=6, sticky=W+E)

    labelNombreViejo= Label(FrameActualizarAdoptante, text='Nombre')
    labelNombreViejo.grid(row=2, column = 0,padx= 0, pady=6)
    entryNombreViejo= Entry(FrameActualizarAdoptante,textvariable= StringVar(actualizar_adoptante, value=nombreViejo))
    entryNombreViejo.grid(row=2, column = 1,padx= 0, pady=6, sticky=W+E)

    labelDomicilioViejo= Label(FrameActualizarAdoptante, text='Domicilio')
    labelDomicilioViejo.grid(row=3, column = 0,padx= 0, pady=6)
    entryDomicilioViejo= Entry(FrameActualizarAdoptante,textvariable= StringVar(actualizar_adoptante, value=domicilioViejo))
    entryDomicilioViejo.grid(row=3, column = 1,padx= 0, pady=6, sticky=W+E)

    labelTelefonoViejo= Label(FrameActualizarAdoptante, text='Teléfono')
    labelTelefonoViejo.grid(row=4, column = 0,padx= 0, pady=6)
    entryTelefonoViejo= Entry(FrameActualizarAdoptante,textvariable= StringVar(actualizar_adoptante, value=telefonoViejo))
    entryTelefonoViejo.grid(row=4, column = 1,padx= 0, pady=6, sticky=W+E)

    boton_actualizarAdoptante = Button(FrameActualizarAdoptante, text="Actualizar",
                                        command = lambda:actualizarAdoptante(id,
                                        entryNombreViejo.get(),
                                        entryDomicilioViejo.get(),
                                        entryTelefonoViejo.get(),
                                        actualizar_adoptante))
    
    boton_actualizarAdoptante.grid(row=8,column=1,sticky=W+E)
    boton_actualizarAdoptante.config(cursor="hand2")
    actualizar_adoptante.mainloop()

#------------------Ventana eliminacion-adoptante----------------------------
def EliminarAdoptante():
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    try:
        tablaAdoptantes.item(tablaAdoptantes.selection())['values'][0]
    except IndexError:
        return
    id= tablaAdoptantes.item(tablaAdoptantes.selection())['text']
    query= '''DELETE FROM adoptante WHERE id_adoptante  =%s'''
    cursor.execute(query, (id,))
    coneccion.commit()
    coneccion.close()
    actualizarTablaAdoptantes()

#------------------Ventana busqueda-adoptante-------------------------------
def busquedaAdoptante(frame,id):
    coneccion = conectarABaseDeDatos()
    cursor = coneccion.cursor()
    query= '''SELECT * FROM adoptante WHERE id_adoptante=%s'''
    cursor.execute(query, (id,))
    encontrado= cursor.fetchone()
    listboxBusAdoptante= Listbox(frame,width=50, height=1)
    listboxBusAdoptante.grid(row=4,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)
    listboxBusAdoptante.insert(END,encontrado)
    coneccion.commit()
    coneccion.close()

def ventanaBuscarAdoptante():
    bus_adoptante= Tk()
    bus_adoptante.title("Buscar Adoptante")
    bus_adoptante.resizable(0,0)

    canvasBuscarAdoptante= Canvas(bus_adoptante, height = "160", width = "475")
    canvasBuscarAdoptante.pack()

    FrameBuscarAdoptante= Frame(bus_adoptante)
    FrameBuscarAdoptante.place(relx = 0.025, rely =0.025, relwidth = 1, relheight = 1)

    labelBuscarAdoptante = Label(FrameBuscarAdoptante, text="Ingrese los datos de búsqueda")
    labelBuscarAdoptante.grid(row=0, column = 0,padx= 0, pady=6, columnspan=2)

    labelIdBusAdoptante= Label(FrameBuscarAdoptante, text = "ID Adoptante")
    labelIdBusAdoptante.grid(row=1, column = 0,padx= 0, pady=6,sticky=E)
    entryBuscarAdoptante= Entry(FrameBuscarAdoptante)
    entryBuscarAdoptante.grid(row = 1, column = 1,padx= 0, pady=6, sticky=W+E)

    listboxBusAdoptante= Listbox(FrameBuscarAdoptante,width=50, height=1)
    listboxBusAdoptante.grid(row=4,column=0,columnspan=2,sticky=W+E,padx= 2, pady=8)

    botonBuscarAdoptante = Button(FrameBuscarAdoptante, text="Buscar",command=lambda:busquedaAdoptante(FrameBuscarAdoptante,entryBuscarAdoptante.get()))
    botonBuscarAdoptante.grid(row=3,column=1, sticky=W+E)
    botonBuscarAdoptante.config(cursor="hand2")
    bus_adoptante.mainloop()


#------------------INICIO DE PROGRAMA -------------------------------------
raiz=Tk()

#-----------------VENTANA--------------------------------------------------
raiz.title("RED DE REFUGIOS") #damos titulo a la ventana
raiz.resizable(1,1)#Decimos si se puede redimensionar
raiz.config(width="740",height="260")#Dimensiones originales de la ventana
raiz.config(bd=4) #Ancho del borde de la ventana(raiz) 
raiz.iconbitmap("icono.ico")

#----------------MENUS SUPERIORES-----------------------------------------
barraMenu= Menu(raiz)#declaramos barra superiores de la aplicacion
raiz.config(menu=barraMenu)#configuramos barra

#-------------------BARRAS-------------------------------------------------
#               OPCIONES DE ARCHIVO
barraArchivo= Menu(barraMenu, tearoff=0)#Pestaña para "Archivo"
barraArchivo.add_command(label= "Guardar")#Opcion de la barra "Archivo"
barraArchivo.add_command(label= "Salir")#Opcion de la barra "Archivo"

#              OPCIONES DE AYUDA
barraAyuda= Menu(barraMenu, tearoff=0)  #Barra para "Ayuda"
barraAyuda.add_command(label= "Acerca de...")#Opcion de la barra "Ayuda"

#--------------AGREGAMOS BARRAS--------------------------------------------
barraMenu.add_cascade(label= "Archivo", menu=barraArchivo)#Para imprimir "Archivo" en la barra
barraMenu.add_cascade(label= "Ayuda", menu=barraAyuda)#Para imprimir "Ayuda" en la barra

#---------------PESTAÑAS------------------------------------------------------
pestanias=ttk.Notebook(raiz) #creamos la variable pestañas y guardamos en raiz
pestanias.pack(fill="both",expand="True")#Empaquetamos  
pestanias.config(width="850",height="260",cursor="hand2")              

frameRefugios = ttk.Notebook(raiz)
frameRefugios.pack()
pestanias.add(frameRefugios, text="Refugios")#Agregamos al notebook "Refugios"

framePatrocinios = ttk.Notebook(raiz)
framePatrocinios.pack()
pestanias.add(framePatrocinios, text="Patrocinios")#Agregamos al notebook "Patrocinios"

framePatrocinadores = ttk.Notebook(raiz)
framePatrocinadores.pack()
pestanias.add(framePatrocinadores, text="Patrocinadores")#Agregamos al notebook "Patrocinadores"

frameVoluntarios= Frame()#Hacemos un frame para voluntarios
frameVoluntarios.pack()#Empaquetamos
pestanias.add(frameVoluntarios, text="Voluntarios")#Agregamos al notebook "Voluntarios"

framePerros=ttk.Notebook(raiz)
framePerros.pack()
pestanias.add(framePerros, text="Perros")#Agregamos al notebook "Perros"

frameAdopciones=ttk.Notebook(raiz)
frameAdopciones.pack()
pestanias.add(frameAdopciones, text="Adopciones")#Agregamos al notebook "Adopciones"

frameAdoptantes=ttk.Notebook(raiz)#Hacemos un frame para adoptantes
frameAdoptantes.pack()#Empaquetamos
pestanias.add(frameAdoptantes, text= "Adoptantes")#Agregamos al notebook "Adoptantes"

#---------------REFUGIOS-----------------------------------------------------------------
botonInsertarRefugio=Button(frameRefugios, text="Insertar", command=lambda:insertarRefugio())
botonInsertarRefugio.grid(row=0,column=0, padx=7,pady=10)
botonInsertarRefugio.config(cursor="hand2")
botonEliminarRefugio=Button(frameRefugios, text="Eliminar",command=lambda:EliminarRefugio())
botonEliminarRefugio.grid(row=1,column=0, padx=7,pady=10)
botonEliminarRefugio.config(cursor="hand2")
botonActualizarRefugio=Button(frameRefugios, text="Actualizar",command=lambda:ventanaActualizarRefuigio())
botonActualizarRefugio.grid(row=2,column=0, padx=7,pady=10)
botonActualizarRefugio.config(cursor="hand2")
botonBuscarRefugio=Button(frameRefugios, text="Buscar",command=lambda:ventanaBuscarRefugio())
botonBuscarRefugio.grid(row=3,column=0, padx=7,pady=10)
botonBuscarRefugio.config(cursor="hand2")
botonRecargarRefugio=Button(frameRefugios, text="Recargar", command=lambda:actualizarTablaRefugio())
botonRecargarRefugio.grid(row=0,column=3, padx=7, pady=10)
botonRecargarRefugio.config(cursor="hand2")
tablaRefugios= ttk.Treeview(frameRefugios) #definimos el treeview
tablaRefugios['columns']= ("Direccion","numero_perros") #definos las columnas 1 "fantasma" + la segunda 
tablaRefugios.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaRefugios.column("#0",width=90)#definimos las columnas #0 = ID Refugios
tablaRefugios.column("Direccion",width=230)#definimso la columna "Direccion"
tablaRefugios.column("numero_perros",width=120)#definimso la columna "Direccion"

tablaRefugios.heading("#0",text="ID Refugio",anchor=W)#agregamos texto
tablaRefugios.heading("Direccion",text="Dirección",anchor=CENTER)#agregamos texto
tablaRefugios.heading("numero_perros",text="Cantidad de perros",anchor=CENTER)

actualizarTablaRefugio()

#---------------PATROCINIOS--------------------------------------------------------------
botonInsertarPatrocinio=Button(framePatrocinios, text="Insertar", command=lambda:insertarPatrocinios())
botonInsertarPatrocinio.grid(row=0,column=0, padx=7,pady=10)
botonInsertarPatrocinio.config(cursor="hand2")
botonEliminarPatrocinio=Button(framePatrocinios, text="Eliminar",command=lambda:EliminarPatrocinio())
botonEliminarPatrocinio.grid(row=1,column=0, padx=7,pady=10)
botonEliminarPatrocinio.config(cursor="hand2")
botonActualizarPatrocinio=Button(framePatrocinios, text="Actualizar",command=lambda:ventanaActualizarPatrocinio())
botonActualizarPatrocinio.grid(row=2,column=0, padx=7,pady=10)
botonActualizarPatrocinio.config(cursor="hand2")
botonBuscarPatrocinio=Button(framePatrocinios, text="Buscar",command=lambda:ventanaBuscarPatrocinio())
botonBuscarPatrocinio.grid(row=3,column=0, padx=7,pady=10)
botonBuscarPatrocinio.config(cursor="hand2")

tablaPatrocinios= ttk.Treeview(framePatrocinios) #definimos el treeview
tablaPatrocinios['columns']= ("ID_Refugio", "ID_Patrocinador") #definos las columnas 1 "fantasma" + la segunda 
tablaPatrocinios.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaPatrocinios.column("#0",width=100)#definimos las columnas #0 = ID patrocinio
tablaPatrocinios.column("ID_Refugio",width=100)#definimso la columna "ID_Refugio"
tablaPatrocinios.column("ID_Patrocinador",width=100)#definimso la columna "ID_Patrocinio"

tablaPatrocinios.heading("#0",text="ID Patrocinio",anchor=CENTER)#agregamos texto
tablaPatrocinios.heading("ID_Refugio",text="ID Refugio",anchor=CENTER)#agregamos texto
tablaPatrocinios.heading("ID_Patrocinador",text="ID Patrocinador",anchor=CENTER)#agregamos texto

actualizarTablaPatrocinios()

#---------------PATROCINADORES-----------------------------------------------------------
botonInsertarPatrocinador=Button(framePatrocinadores, text="Insertar", command=lambda:insertarPatrocinador())
botonInsertarPatrocinador.grid(row=0,column=0, padx=7,pady=10)
botonInsertarPatrocinador.config(cursor="hand2")
botonEliminarPatrocinador=Button(framePatrocinadores, text="Eliminar",command=lambda:EliminarPatrocinador())
botonEliminarPatrocinador.grid(row=1,column=0, padx=7,pady=10)
botonEliminarPatrocinador.config(cursor="hand2")
botonActualizarPatrocinador=Button(framePatrocinadores, text="Actualizar",command=lambda:ventanaActualizarPatrocinador())
botonActualizarPatrocinador.grid(row=2,column=0, padx=7,pady=10)
botonActualizarPatrocinador.config(cursor="hand2")
botonBuscarPatrocinador=Button(framePatrocinadores, text="Buscar",command=lambda:ventanaBuscarPatrocinador())
botonBuscarPatrocinador.grid(row=3,column=0, padx=7,pady=10)
botonBuscarPatrocinador.config(cursor="hand2")

tablaPatrocinadores= ttk.Treeview(framePatrocinadores)
tablaPatrocinadores['columns']= ("Nombre","Telefono")
tablaPatrocinadores.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaPatrocinadores.column("#0",width=90)
tablaPatrocinadores.column("Nombre", anchor=W, width= 180)
tablaPatrocinadores.column("Telefono", anchor=CENTER, width= 110)

tablaPatrocinadores.heading("#0",text="ID Patrocinador",anchor=W)
tablaPatrocinadores.heading("Nombre",text="Nombre",anchor=CENTER)
tablaPatrocinadores.heading("Telefono",text="Teléfono",anchor=CENTER)

actualizarTablaPatrocinadores()

#---------------VOLUNTARIOS--------------------------------------------------------------
botonInsertarVoluntario=Button(frameVoluntarios, text="Insertar", command=lambda:insertarVoluntario())
botonInsertarVoluntario.grid(row=0,column=0, padx=7,pady=10)
botonInsertarVoluntario.config(cursor="hand2")
botonEliminarVoluntario=Button(frameVoluntarios, text="Eliminar", command=lambda:EliminarVoluntario())
botonEliminarVoluntario.grid(row=1,column=0, padx=7,pady=10)
botonEliminarVoluntario.config(cursor="hand2")
botonActualizarVoluntario=Button(frameVoluntarios, text="Actualizar",command=lambda:ventanaActualizarVoluntario())
botonActualizarVoluntario.grid(row=2,column=0, padx=7,pady=10)
botonActualizarVoluntario.config(cursor="hand2")
botonBuscarVoluntario=Button(frameVoluntarios, text="Buscar", command=lambda:ventanaBuscarVoluntario())
botonBuscarVoluntario.grid(row=3,column=0, padx=7,pady=10)
botonBuscarVoluntario.config(cursor="hand2")

tablaVoluntarios= ttk.Treeview(frameVoluntarios)
tablaVoluntarios['columns']= ("Nombre","Apellido","Fecha_registro","Fecha_nacimiento","Telefono","ID_ref")
tablaVoluntarios.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaVoluntarios.column("#0",width=80)
tablaVoluntarios.column("Nombre", width= 130)
tablaVoluntarios.column("Apellido", width= 130)
tablaVoluntarios.column("Fecha_registro", width= 95)
tablaVoluntarios.column("Fecha_nacimiento", width= 105)
tablaVoluntarios.column("Telefono", width= 100)
tablaVoluntarios.column("ID_ref", width= 100)

tablaVoluntarios.heading("#0", text="ID Voluntario",anchor=CENTER)
tablaVoluntarios.heading("Nombre", text="Nombre",anchor=CENTER)
tablaVoluntarios.heading("Apellido", text="Apellido",anchor=CENTER)
tablaVoluntarios.heading("Fecha_registro", text="Fecha Registro",anchor=CENTER)
tablaVoluntarios.heading("Fecha_nacimiento", text="Fecha Nacimiento",anchor=CENTER)
tablaVoluntarios.heading("Telefono", text="Teléfono",anchor=CENTER)
tablaVoluntarios.heading("ID_ref", text="Refugio",anchor=CENTER)

actualizarTablaVoluntario()
#---------------PERROS------------------------------------------------------------------
botonInsertarPerro=Button(framePerros, text="Insertar", command=lambda:insertarPerro())
botonInsertarPerro.grid(row=0,column=0, padx=7,pady=10)
botonInsertarPerro.config(cursor="hand2")
botonEliminarPerro=Button(framePerros, text="Eliminar", command=lambda:EliminarPerro())
botonEliminarPerro.grid(row=1,column=0, padx=7,pady=10)
botonEliminarPerro.config(cursor="hand2")
botonActualizarPerro=Button(framePerros, text="Actualizar", command=lambda:ventanaActualizarPerro())
botonActualizarPerro.grid(row=2,column=0, padx=7,pady=10)
botonActualizarPerro.config(cursor="hand2")
botonBuscarPerro=Button(framePerros, text="Buscar", command=lambda:ventanaBuscarPerro())
botonBuscarPerro.grid(row=3,column=0, padx=7,pady=10)
botonBuscarPerro.config(cursor="hand2")
botonRecargarPerros=Button(framePerros, text="Recargar", command=lambda:actualizarTablaPerro())
botonRecargarPerros.grid(row=0,column=3, padx=7, pady=10)
botonRecargarPerros.config(cursor="hand2")
tablaPerros= ttk.Treeview(framePerros)
tablaPerros['columns']= ("Adoptado","Nombre","Fecha_ingreso","Raza","Edad","ID_refu")
tablaPerros.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaPerros.column("#0",width=80)
tablaPerros.column("Adoptado", width= 100)
tablaPerros.column("Nombre", width= 130)
tablaPerros.column("Fecha_ingreso", width= 105)
tablaPerros.column("Raza", width= 110)
tablaPerros.column("Edad", width= 50)
tablaPerros.column("ID_refu", width= 80)

tablaPerros.heading("#0", text="ID Perro",anchor=CENTER)
tablaPerros.heading("Adoptado", text="Adoptado",anchor=CENTER)
tablaPerros.heading("Nombre", text="Nombre",anchor=CENTER)
tablaPerros.heading("Fecha_ingreso", text="Fecha Ingreso",anchor=CENTER)
tablaPerros.heading("Raza", text="Raza",anchor=CENTER)
tablaPerros.heading("Edad", text="Edad",anchor=CENTER)
tablaPerros.heading("ID_refu", text="Refugio",anchor=CENTER)

actualizarTablaPerro()
#---------------ADOPCIONES--------------------------------------------------------------
botonInsertarAdopcion=Button(frameAdopciones, text="Insertar", command=lambda:insertarAdopcion())
botonInsertarAdopcion.grid(row=0,column=0, padx=7,pady=10)
botonInsertarAdopcion.config(cursor="hand2")
botonEliminarAdopcion=Button(frameAdopciones, text="Eliminar", command=lambda:EliminarAdopcion())
botonEliminarAdopcion.grid(row=1,column=0, padx=7,pady=10)
botonEliminarAdopcion.config(cursor="hand2")
botonActualizarAdopcion=Button(frameAdopciones, text="Actualizar", command=lambda:ventanaActualizarAdopcion())
botonActualizarAdopcion.grid(row=2,column=0, padx=7,pady=10)
botonActualizarAdopcion.config(cursor="hand2")
botonBuscarAdopcion=Button(frameAdopciones, text="Buscar", command=lambda:ventanaBuscarAdopcion())
botonBuscarAdopcion.grid(row=3,column=0, padx=7,pady=10)
botonBuscarAdopcion.config(cursor="hand2")

tablaAdopciones= ttk.Treeview(frameAdopciones)
tablaAdopciones['columns']= ("Fecha_adopcion","ID_refugio","ID_perro","ID_adoptante")
tablaAdopciones.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaAdopciones.column("#0",width=80)
tablaAdopciones.column("Fecha_adopcion", width= 110)
tablaAdopciones.column("ID_refugio", width= 80)
tablaAdopciones.column("ID_perro", width= 80)
tablaAdopciones.column("ID_adoptante", width= 80)

tablaAdopciones.heading("#0", text="ID Adopción",anchor=CENTER)
tablaAdopciones.heading("Fecha_adopcion", text="Fecha Adopción",anchor=CENTER)
tablaAdopciones.heading("ID_refugio", text="ID Refugio",anchor=CENTER)
tablaAdopciones.heading("ID_perro", text="ID Perro",anchor=CENTER)
tablaAdopciones.heading("ID_adoptante", text="ID Adoptante",anchor=CENTER)

actualizarTablaAdopciones()

#---------------ADOPTANTES--------------------------------------------------------------
botonInsertarAdoptantes=Button(frameAdoptantes, text="Insertar", command=lambda:insertarAdoptante())
botonInsertarAdoptantes.grid(row=0,column=0, padx=7,pady=10)
botonInsertarAdoptantes.config(cursor="hand2")
botonEliminarAdoptantes=Button(frameAdoptantes, text="Eliminar", command=lambda:EliminarAdoptante())
botonEliminarAdoptantes.grid(row=1,column=0, padx=7,pady=10)
botonEliminarAdoptantes.config(cursor="hand2")
botonActualizarAdoptantes=Button(frameAdoptantes, text="Actualizar", command=lambda:ventanaActualizarAdoptante())
botonActualizarAdoptantes.grid(row=2,column=0, padx=7,pady=10)
botonActualizarAdoptantes.config(cursor="hand2")
botonBuscarAdoptantes=Button(frameAdoptantes, text="Buscar", command=lambda:ventanaBuscarAdoptante())
botonBuscarAdoptantes.grid(row=3,column=0, padx=7,pady=10)
botonBuscarAdoptantes.config(cursor="hand2")

tablaAdoptantes= ttk.Treeview(frameAdoptantes)
tablaAdoptantes['columns']= ("Nombre","Domiclio","Telefono")
tablaAdoptantes.grid(row= 0, column=1,rowspan=4, padx=7,pady=10)

tablaAdoptantes.column("#0",width=80)
tablaAdoptantes.column("Nombre", width= 200)
tablaAdoptantes.column("Domiclio", width= 180)
tablaAdoptantes.column("Telefono", width= 100)

tablaAdoptantes.heading("#0", text="ID Adoptante",anchor=CENTER)
tablaAdoptantes.heading("Nombre", text="Nombre",anchor=CENTER)
tablaAdoptantes.heading("Domiclio", text="Domiclio",anchor=CENTER)
tablaAdoptantes.heading("Telefono", text="Teléfono",anchor=CENTER)

actualizarTablaAdoptantes()
#---------------FIN DE PROGRAMA----------------------------------------
raiz.mainloop()