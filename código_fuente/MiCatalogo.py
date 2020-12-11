import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

def init_window():
    """
    interfaz grafica del inicio de sesion y registro del progrma, página principal
    :return:None
    """

    window = tk.Tk()
    window.title('ACCESO ')
    window.geometry('950x400')
    window['bg'] = 'silver'

    label_titulo = tk.Label(window, text='Bienvenido a "MiCatalogo"', font=('Matura MT Script Capitals', 45), bg = 'silver')
    label_titulo.grid(column=0, row=0, columnspan = 4)

    entrada1 = tk.Entry(window, width=45)
    entrada2 = tk.Entry(window, width=45)

    entrada1.grid(column = 2, row = 4, columnspan=2)
    entrada2.grid(column = 2, row = 5, columnspan = 2)

    label_entrada1 = tk.Label(window, text = 'Usuario:', font=('Lucida Console', 20), bg = 'silver')
    label_entrada1.grid(column = 0, row = 4, columnspan = 2)

    label_entrada2 = tk.Label(window, text = 'Contraseña:', font=('Lucida Console', 20), bg = 'silver')
    label_entrada2.grid(column = 0, row= 5, columnspan = 2)

    entrada2.config(show="*")

    label_operador = tk.Label(window, text='Escoja una opcion para ingresar', font=('Lucida Console', 20), bg = 'silver')
    label_operador.grid(column=0, row=2, columnspan = 2)

    combo_operadores = ttk.Combobox(window,font = ('Lucida Consple', 15))
    combo_operadores['values'] = ['Registro', 'Inicio sesion']
    combo_operadores.current(1)
    combo_operadores.grid(column=2, row=2, columnspan = 4)

    label_operador = tk.Label(window, text='Escoja el rol con el que desea ingresar', font=('Lucida Console', 20), bg = 'silver')
    label_operador.grid(column=0, row=7, columnspan=2)

    combo_roles = ttk.Combobox(window,font=('Lucida Consple', 15))
    combo_roles['values'] = ['Administrador', 'Usuario']
    combo_roles.current()
    combo_roles.grid(column=2, row=7, columnspan=4)

    label_resultado = tk.Label(window, text='', font=('Calibri ', 25), bg = 'silver')
    label_resultado.grid(column = 1, row = 6, columnspan = 2)

    boton = tk.Button(window,
                      command=lambda: click_login(
                          label_resultado,
                          entrada1.get(),
                          entrada2.get(),
                          combo_operadores.get(),
                          combo_roles.get()),
                      text='Ingresar',
                      bg='green',
                      font = ('Calibri', 25),
                      fg='black')
    boton.grid(column=1, row=10)

    boton = tk.Button(window,
                      command=lambda: salir(),
                      text='Salir',
                      bg='green',
                      font=('Calibri', 25),
                      fg='black')
    boton.grid(column=2, row=10)

    def salir():            #Comando que usa el boton salir para acabar la página
        window.destroy()

    window.mainloop()


def click_login(label, usuario, passw, operador, rol):
    """
    click_login: envia el resultado a imprimir en la interfaz de acuerdo a los return de login, o permite el paso a la siguiente página del programa
    :param label: mensaje que enviara en caso de error
    :param usuario: Usuario ingresado
    :param passw: Contrasenia ingresada
    :param operador: El tipo de acceso que se quiera hacer
    :return: Un label con lo que se quiere escribir en la interfaz
    """
    tupla_res = login(usuario, passw, operador, rol)        #llamdo a funcion login

    if tupla_res == 'Error Passw':
        label.configure(text = 'Error en el inicio de sesión,\n verifique su contraseña\n e intentelo de nuevo', font=('Calibri', 15))
    elif tupla_res == 'Error User':
        label.configure(text = 'Error en el inicio de sesión,\n verifique su contraseña\n e intentelo de nuevo', font=('Calibri', 15))
    elif tupla_res == 'URegis' :
        label.configure(text='Usuario ya registrada,\n intentelo de nuevo',font=('Calibri', 15))
    elif tupla_res == 'PRegis':
        label.configure(text='Contraseña ya registrado,\n intentelo de nuevo', font=('Calibri', 15))
    elif tupla_res == 'Rol':
        label.configure(text='Usted solo puede acceder con el rol de usuario', font=('Calibri',15))
    else:
        menu_window(tupla_res)


def login(usuario, passw, operador, rol):
    """
    login : comprueba la veracidad o posibilidad de creacion de un usuario o contrasenia.
    :param usuario: nombre inngresado
    :param passw: contrasenia ingresada
    :param operador: si se desea iniciar sesion registrar una nueva cuenta
    :param rol: rol con el que se quiere ingresar
    :return: dos string, las cuales representan el error o el usuario y contraseña.
    """
    registeredUser=()   #Lista de todos los usuarios regisrados
    registeredPW=()     #Lista contrasenias registradas
    diccionario_registro ={}

    try:
        Usuarios= open('../archivos/Usuarios.txt', 'r')
    except:
        Usuarios = open('../archivos/Usuarios.txt', 'a+')

    try:
        Passwords = open('../archivos/Passwords.txt', 'r')
    except:
        Passwords= open('../archivos/Passwords.txt','a+')

    for lines in Usuarios:
        lines = lines.rstrip()
        registeredUser += (lines,)

    for lines2 in Passwords:
        lines2=lines2.rstrip()
        registeredPW += (lines2,)

    Usuarios.close()
    Passwords.close()
    c = 0
    for users in registeredUser:
        diccionario_registro[users] = registeredPW[c]
        c += 1


    if operador == 'Inicio sesion':
        f = 'Error Passw'
        g = 'Error User'
        if usuario in diccionario_registro.keys():
            if diccionario_registro[usuario] == passw:
                return usuario, passw, rol
            else:
                return f
        else:
            return g
    else:
        t = 'URegis'         #Errores
        s = 'PRegis'
        w = 'Rol'
        if rol == 'Administrador':
            return w
        else:
            if usuario in diccionario_registro.keys():
                return t
            else:
                if passw in diccionario_registro.values():
                    return s
                else:
                    diccionario_registro[usuario] = passw

    usuarios = open('../archivos/usuarios.txt','w')
    for u in list(diccionario_registro.keys()):
        usuarios.write(str(u)+'\n')
    usuarios.close()

    passwords = open('../archivos/passwords.txt', 'w')
    for p in list(diccionario_registro.values()):
        passwords.write(str(p)+'\n')
    passwords.close()

    return usuario, passw, rol


def menu_window(a):
    """
    menu_window: Interfaz gráfica, página secundaria, menú
    :param a: usuario, contraseña y rol con el que ingreso
    :return: none
    """
    m_window = tk.Tk()
    m_window.title('MENÚ')
    m_window.geometry('600x500')
    m_window['bg'] = 'SteelBlue2'

    label_titulo = tk.Label(m_window, text='Menú "MiCatalogo"', font=('Matura MT Script Capitals', 45), bg = 'firebrick3', fg = 'azure' )
    label_titulo.grid(column=2, row=3, columnspan=1)

    informacion_web()

    if a[2] == 'Administrador':
        boton1 = tk.Button(m_window,
                        command=lambda: agregar_libro(),
                        text='Agregar Nuevos Libros',
                        bg='firebrick3',
                        anchor ='center',
                        font=('Calibri', 25),
                        fg='azure')
        boton1.grid(column=2, row=4, columnspan=2, pady= 15)

    boton2 = tk.Button(m_window,
                       command = lambda: mostrar_libros(),
                       text='Ver el catalogo',
                       bg='firebrick3',
                       font=('Calibri',25),
                       fg='azure')
    boton2.grid(column=2, row=6, columnspan= 2, pady=15)

    boton3 = tk.Button(m_window,
                       command=lambda:prestamos(a[0]),
                       text='Préstamos',
                       bg='firebrick3',
                       font=('Calibri',25),
                       fg='azure')
    boton3.grid(column=2, row = 8, columnspan=2, pady=15)

    boton4 = tk.Button(m_window,
                       command=lambda: mis_prestamos(a[0]),
                       text='Mis préstamos',
                       bg='firebrick3',
                       font=('Calibri', 25),
                       fg='azure')
    boton4.grid(column=2, row=10, columnspan=2, pady = 15)

    boton = tk.Button(m_window,
                      command=lambda: salir(),
                      text='Volver al inico de sesion',
                      bg='firebrick3',
                      anchor = 'center',
                      font=('Calibri', 25),
                      fg='azure')
    boton.grid(column=2, row=12, pady = 15)

    def salir():                #Comando que usa el boton salir para acabar la página
        m_window.destroy()

    m_window.mainloop()


def agregar_libro():
    """
    agregar_libros:Interfaz gráfica secundaria, donde muestra opciones para ingresar datos de los libros
    :return: None
    imprime los principales datos que fueron guardados
    """
    # Todos los datos escenciales que se piden para agregar al catalogo
    agregar_window = tk.Tk()
    agregar_window.title('NUEVO ')
    agregar_window.geometry('700x700')
    agregar_window['bg'] = 'gold3'

    def salir():                #Comando que usa el boton salir para acabar la página
        agregar_window.destroy()

    label_titulo = tk.Label(agregar_window, text='AGREGAR LIRBO', font=('Ink free', 45), bg = 'gold3', pady = 5 )
    label_titulo.grid(column=0, row=0, columnspan=4)

    nombre = tk.Entry(agregar_window, width=45)
    autor = tk.Entry(agregar_window, width=45)
    fecha = tk.Spinbox(agregar_window, from_=1900, to=2020, width=45)
    fecha.grid(column=2, row=4)
    genero = tk.Entry(agregar_window, width=45)
    paginas = tk.Entry(agregar_window, width=45)

    nombre.grid(column=2, row=2, columnspan=2, pady = 5)
    autor.grid(column=2, row=3, columnspan=2)
    genero.grid(column=2, row=5, columnspan=2)
    paginas.grid(column=2, row=6, columnspan=2)

    label_nombre = tk.Label(agregar_window, text='Título del libro', font=('Lucida Console', 20), bg = 'gold3', pady = 5)
    label_nombre.grid(column=0, row=2, columnspan=2)

    label_autor = tk.Label(agregar_window, text='Autor', font=('Lucida Console', 20), bg = 'gold3')
    label_autor.grid(column=0, row=3, columnspan=2)

    label_fecha = tk.Label(agregar_window, text='Año de publicacion', font=('Lucida Console', 20), bg = 'gold3')
    label_fecha.grid(column=0, row=4, columnspan=2)

    label_genero = tk.Label(agregar_window, text='Género', font=('Lucida Console', 20), bg = 'gold3')
    label_genero.grid(column=0, row=5, columnspan=2)

    label_paginas = tk.Label(agregar_window, text='Paginas', font=('Lucida Console', 20), bg = 'gold3')
    label_paginas.grid(column=0, row=6, columnspan=2, pady = 5)

    label_guardado = tk.Label(agregar_window, text='', font=('Lucida Console ', 20), bg = 'gold3')
    label_guardado.grid(column=1, row=8, columnspan=2, pady = 5)

    boton_agregar = tk.Button(agregar_window,
                       command=lambda: guardar(
                           label_guardado,
                           nombre.get(),
                           autor.get(),
                           fecha.get(),
                           genero.get(),
                           paginas.get()),
                       text='AGREGAR',
                       bg='gray34',
                       font=('Calibri', 25),
                       fg='black')
    boton_agregar.grid(column=2, row=10, columnspan=2, pady = 5)
    nombre.delete(0, 4)
    autor.delete(0, 'end')

    boton_volver = tk.Button(agregar_window,
                      command=lambda: salir(),
                      text='Volver al menú',
                      bg='gray34',
                      font=('Calibri', 25),
                      fg='black')
    boton_volver.grid(column=1, row=10, pady = 5)

    agregar_window.mainloop()


def guardar(label,nombre,autor,fecha,genero,paginas):
    """
    guardar: guarda los datos del nuevo libro en los archivos del programa
    :param label: mensaje que mostrara con los datos del libro guardado
    :param nombre: título del libro
    :param autor: nombre del autor del libro
    :param fecha: fecha de publicacion del libro
    :param genero: género del libro
    :param paginas: número de páginas que tiene el libro
    :return: none
    """
    archivo = open("../archivos/ejemplo.txt", "a")
    if autor == '' :
        autor = 'Desconocido'
    if paginas == '':
        fecha = 'Desconocida'
    if genero == '' :
        genero = 'Desconocida'
    label.configure(text=f'Se ha guardado el libro {nombre} del autor {autor}\n{nombre}\n{autor}\n{fecha}\n{genero}\n{paginas}\n')

    archivo.write(nombre + ",0," + autor + "," + fecha + "," + paginas + "," + genero + "\n")  # Guardado de los datos en el archivo ejemplo.txt
    archivo.close()


def mostrar_libros():
    """
    mostrar_libros, muestra todo el catalogo de libros con sus respectivos datos
    :param libros: lista con cada libro
    :return: None
    Imprime la lista de catalogo
    """
    libros =[]
    mostrar_window = tk.Tk()
    mostrar_window.title('LIBROS')
    mostrar_window.geometry('850x800')
    mostrar_window['bg'] = 'gold3'

    def salir():                    #Comando que usa el boton salir para acabar la página
        mostrar_window.destroy()

    label_titulo = tk.Label(mostrar_window, text='CATALOGO', font=('Showcard Gothic', 35), bg = 'gold3' )
    label_titulo.grid(column=1, row=0, columnspan = 3)

    archivo = open("../archivos/ejemplo.txt", "r")
    lines = archivo.readlines()
    for line in lines:  # conversion de los datos del archivo en listas por cada libro
        datos = line.split(',')
        libros.append(datos)
    archivo.close()

    scrollbar = Scrollbar(mostrar_window, orient='vertical', bg='green', troughcolor='green')
    scrollbar.grid(column=0, row=2, rowspan=100, ipady=100, sticky=(N, S))

    len_mayor = ''

    mylist = Listbox(mostrar_window, yscrollcommand=scrollbar.set)
    for l in libros:
        for i in range(len(l)):
            if l[i] == '0':
                mylist.insert(END, '     DISPONIBLE')
            elif l[i] == '1':
                mylist.insert(END, '     PRESTAMO ACTIVO')
            elif i == 5:
                mylist.insert(END, f'     Páginas           {l[i]}')
            elif i == 4:
                mylist.insert(END, f'     Publicacion:      {l[i]}')
            elif i == 3:
                mylist.insert(END, f'     Género:         {l[i]}')
            elif i == 2:
                mylist.insert(END, f'     Autor:            {l[i]}')
            else:
                mylist.insert(END, f'     {l[i]}')
                if len(l[i]) > len(len_mayor):
                    len_mayor = l[i]
        mylist.insert(END, '-----' * 20)
    mylist.grid(column=1, row=2, rowspan=100, ipady=250, ipadx=len(len_mayor)*2.5, padx=10)
    scrollbar.config(orient='vertical', command=mylist.yview)

    boton_volver = tk.Button(mostrar_window,
                             command=lambda: salir(),
                             text='Volver al menú',
                             bg='gray34',
                             font=('Calibri', 25),
                             fg='black')
    boton_volver.grid(column = 3, row = 3, pady = 100, padx = 40)

    mostrar_window.mainloop()


def prestamos(x):
    """
    prestamos: Interfaz gráfica, muestra la lista de libros del catalogo y da opciones de prestamos
    :param x: usuario con el cual se ingreso
    :return: none
    """

    libros = []
    prestamo_window = tk.Tk()
    prestamo_window.title('PRESTAMOS')
    prestamo_window.geometry('950x650')
    prestamo_window['bg'] = 'gold3'

    def salir():
        prestamo_window.destroy()

    label_titulo = tk.Label(prestamo_window, text='PRESTAMOS', font=('Showcard Gothic', 45), bg = ('gold3'))
    label_titulo.grid(column = 1, row = 0, columnspan = 5)

    label_sub = tk.Label(prestamo_window, text='Lista libros:',font=('Ink free', 25), bg = 'gold3')
    label_sub.grid(column=1, row= 1)

    archivo = open("../archivos/ejemplo.txt", "r")
    lines = archivo.readlines()
    for line in lines:
        datos = line.split(',')
        libros.append(datos)
    archivo.close()

    scrollbar = Scrollbar(prestamo_window, orient='vertical', bg='green', troughcolor='green')
    scrollbar.grid(column = 0, row = 2, rowspan =120, ipady = 230,sticky=(N,S))

    len_mayor = 0
    identificador = 0
    mylist = Listbox(prestamo_window, yscrollcommand=scrollbar.set)
    for h in range(len(libros)):
        identificador += 1
        libros[h].append(identificador)
        if len(libros[h])>len(libros[len_mayor]):
            len_mayor = h
        mylist.insert(END, f'{identificador}.{libros[h][0]}')
        mylist.insert(END, f'   {libros[h][2]}')
        mylist.insert(END,'-----' * 16)
    mylist.grid(column = 1, row = 2, rowspan = 100, ipady = 170, ipadx = len(libros[len_mayor])*17, padx = 10)
    scrollbar.config(orient='vertical', command=mylist.yview)

    label_num_libro = tk.Label(prestamo_window, text='Seleccione el número del libro que desea pedir prestado',font=('Ink free', 15), bg = 'gold3')
    label_num_libro.grid(column=3, row=10, columnspan=2)

    num_libro = tk.Spinbox(prestamo_window, from_=1, to=identificador, width=10)
    num_libro.grid(column=3, row=11, columnspan = 2)

    label_fecha = tk.Label(prestamo_window, text='Fecha de vigencia del prestamo', font=('Ink free', 15), bg = 'gold3')
    label_fecha.grid(column=3, row=12, columnspan=2, pady = 6)

    dia_fecha = tk.Spinbox(prestamo_window, from_=1, to=30, width=10)
    dia_fecha.grid(column=3, row=13)

    label_dia_fecha = tk.Label(prestamo_window, text='Día', font=('Ink free', 12), bg = 'gold3')
    label_dia_fecha.grid(column=3, row=14, pady = 6)

    mes_fecha = tk.Spinbox(prestamo_window, from_=1, to=12, width=10)
    mes_fecha.grid(column=4, row=13)

    label_mes_fecha = tk.Label(prestamo_window, text='Mes', font=('Ink free', 12),bg = 'gold3')
    label_mes_fecha.grid(column=4, row=14, pady = 6)

    label_comprobar = tk.Label(prestamo_window, text='', font=('Calibri ', 25), bg = 'gold3')
    label_comprobar.grid(column=3, row=16, columnspan=2)

    boton_continuar = tk.Button(prestamo_window,
                             command=lambda: comprobar(
                                 mes_fecha.get(),
                                 dia_fecha.get(),
                                 label_comprobar,
                                 num_libro.get(),
                                 libros,
                                 x),
                             text='Continuar',
                             bg='gray34',
                             font=('Calibri', 25),
                             fg='black')
    boton_continuar.grid(column=3, row=18,columnspan =2, pady = 6)

    boton_volver = tk.Button(prestamo_window,
                             command=lambda: salir(),
                             text='Volver al menú',
                             bg='gray34',
                             font=('Calibri', 25),
                             fg='black')
    boton_volver.grid(column=3, row=20,columnspan =2,  pady = 6)

    prestamo_window.mainloop()


def comprobar(mes_fecha, dia_fecha, label, num_libro, libros, user):
    """
    comprobar: lee el catalogo y da los libros en prestamo de acuerdo a su disponibilidad
    guarda el registro del prestamo en un archivo.txt.
    :param mes_fecha: mes de vigencia del prestamo
    :param dia_fecha: dia de vigencia del prestamo
    :param label: mensaje de error o confirmacion del prestamo
    :param num_libro: identificador del libro que se quiere pedir prestado
    :param libros: lista de libros del catalogo
    :param user: usuario con el cual ingreso
    :return: none
    """
    bandera = False
    now = datetime.now()
    for i in range(len(libros)):  # Comprobacion disponibilidad libro a partir de
        if str(libros[i][-1]) == num_libro:  # el 1 y 0.
            if libros[i][1] == '0':
                libros[i][1]='1'
                libro = libros[i][0]
                bandera = True
                break
            else:
                break
        else:
            continue

    if bandera:
        dia = [str(now.day), str(now.month), str(now.year)]
        dia = '-'.join(dia)
        hora = [str(now.hour), str(now.minute)]
        hora = ':'.join(hora)
        dia_completo = [dia, hora]
        dia_completo = ' / '.join(dia_completo)
        label.configure(text=f'Se ha realizado prestamo del libro\n{libro}\na nombre de\n{user}\nhasta el dia\n{dia_fecha}/{mes_fecha}',font=('Ink free', 15))
        prestamos = open('../archivos/prestamos.txt', 'a')
        prestamos.write(libro + ',' + user + ',' + dia_fecha + '/' + mes_fecha + ',' + dia_completo+'\n')  # Guardado de datos en el archivo prestamos.txt
        prestamos.close()

    else:
        label.configure(text='El libro ya fue prestado', font=('Ink free', 15))


    archivo = open("../archivos/ejemplo.txt", "w")
    for l in libros:
        l1 = ''
        for i in l:  # Guardado de los datos actualizados en el archivo
            if i == l[-1]:
                l1 = l1
            elif i == l[-2]:
                l1 += i
            else:
                l1 += i + ','
        archivo.write(str(l1))
    archivo.close()


def mis_prestamos(user):
    """
    mis_pretamos: Interfaz gráfica secundaria donde aparecen todos los libros que el usuario pidio prestado
    :param user: usuario con el que se ingreso
    :return: None
    """
    libros=[]
    mis_window = tk.Tk()
    mis_window.title('PRESTAMOS')
    mis_window.geometry('750x500')
    mis_window['bg'] = 'gold3'


    def salir():
        mis_window.destroy()

    label_titulo = tk.Label(mis_window, text='Mis préstamos', font=('Showcard Gothic', 45), bg=('gold3'))
    label_titulo.grid(column = 1, row = 0, columnspan = 4)

    archivo = open("../archivos/prestamos.txt", 'r')
    lines = archivo.readlines()
    for line in lines:
        datos = line.split(',')
        libros.append(datos)
    archivo.close()

    scrollbar = Scrollbar(mis_window, orient = 'vertical',bg ='green', 	troughcolor = 'green')
    scrollbar.grid(column = 0, row = 2, rowspan =100, ipady = 100,sticky=(N,S))

    len_mayor = 0

    mylist = Listbox(mis_window, yscrollcommand=scrollbar.set)
    for h in range(len(libros)):
        if libros[h][1] == user:
            if len(libros[h]) > len(libros[len_mayor]):
                len_mayor = h
            mylist.insert(END,f'  TÍTULO:                         {libros[h][0]}')
            mylist.insert(END, f'')
            mylist.insert(END,f'  FECHA PETICION:        {libros[h][3]}')
            mylist.insert(END, f'')
            mylist.insert(END,f'  FECHA EXPEDICION:    {libros[h][2]}')
            mylist.insert(END, '-----'* 10)
    mylist.grid(column = 1, row = 2, rowspan = 100, ipady = 100, ipadx = len(libros[len_mayor])*20, padx = 10)
    scrollbar.config(orient='vertical', command=mylist.yview)

    boton_volver = tk.Button(mis_window,
                             command=lambda: salir(),
                             text='Volver al menú',
                             bg='gray34',
                             font=('Calibri', 25),
                             fg='black')
    boton_volver.grid(column = 3, row = 3, pady = 100, padx = 40)

    mis_window.mainloop()


def info_pag(texto):
    """
    termina de extraer la informacion valiosa para el proyecto
    :param texto: informacion del html de la pagina web
    :return: lista de informacion valiosa de la página
    """
    lineas = [linea for linea in texto.split('\n') if linea != '']
    bandera = False

    listo = []
    for i in lineas:
        if i == 'Blue paradise':
            listo.append(i.strip())
            bandera = True
        elif i == ' Añadir a la cesta' or i == 'Cantidad:' or 'Libro impreso' in i or i == 'Autor:'or 'Ebook (epub):' in i or i == 'Agotado':
            continue
        elif i == '← Anterior':
            bandera = False
        elif bandera:
            listo.append(i.strip())

    libros = []
    libro = {}
    for elemento in listo:
        if ':' not in elemento:
            if len(elemento) <= 0:
                if len(libro) == 6:
                    libro_ordenado = []
                    for d in libro.keys():
                        if d == 'Descripcion':
                            continue
                        libro_ordenado.append(libro[d])
                    libros.append(libro_ordenado)
                    libro = {}
                else:
                    continue
            elif len(libro) == 0:
                libro['nombre'] = elemento.strip()
            elif len(libro) == 1:
                libro['autor'] = elemento.strip()
            elif len(libro) == 5:
                libro['Descripcion'] = elemento
            else:
                continue
        elif len(libro) == 5:
            libro['Descripcion'] = elemento
        else:
            elemento = elemento.split(':')
            libro [elemento[0].strip()] = elemento[1].strip()

    return libros


def comprobar_info(libros_pagina):
    """
    comprobar: comprueba que libros de la web ya estan en el archivo de texto
    :param libros_pagina: lista de libros extraidos de la web
    :return: lista con los libros que no estan en el archivo de texto
    """
    libros_archivo = []
    archivo = open("../archivos/ejemplo.txt", "r")
    lines = archivo.readlines()
    for line in lines:
        datos = line.split(',')
        libros_archivo.append(datos)
    archivo.close()

    libros_falta= []
    for indice in range(len(libros_pagina)):
        bandera = False
        for libro_archivo in libros_archivo:
            if libros_pagina[indice][0] == libro_archivo[0] or libro_archivo[0] in libros_pagina[indice][0]:
                bandera = True
        if bandera == False:
            libros_falta.append(libros_pagina[indice])

    return libros_falta


def informacion_web():
    """
    informacion_web: toma la informacion de la pagina web y se quitan etiquetas
    ademas agregar la informacion al archivo de texto
    :return: none
    """
    url = "https://editorialamarante.es/libros"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text()
    libros_pagina = info_pag(texto)
    libros = comprobar_info(libros_pagina)
    archivo = open("../archivos/ejemplo.txt", "a")
    for libro in libros:
        libro.insert(1, '0')
        libro = ','.join(libro)
        archivo.write(libro + '\n')
    archivo.close()


def main():
    init_window()

main()