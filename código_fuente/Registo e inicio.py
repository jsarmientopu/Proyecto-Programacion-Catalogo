import tkinter as tk
from tkinter import ttk

def init_window():
    """
    interfaz grafica del programa
    :return:None
    """

    window = tk.Tk()
    window.title('ACCESO ')
    window.geometry('400x250')

    entrada1 = tk.Entry(window, width=20)
    entrada2 = tk.Entry(window, width=20)

    entrada1.grid(column = 2, row = 2)
    entrada2.grid(column = 2, row = 3)

    label_entrada1 = tk.Label(window, text = 'Usuario:', font=('Calibri', 15))
    label_entrada1.grid(column = 1, row = 2)

    label_entrada2 = tk.Label(window, text = 'Contraseña:', font=('Calibri', 15))
    label_entrada2.grid(column = 1, row= 3)

    label_operador = tk.Label(window, text='Escoja una opcion', font=('Calibri', 15))
    label_operador.grid(column=1, row=0, columnspan = 2)

    combo_operadores = ttk.Combobox(window)
    combo_operadores['values'] = ['Registro', 'Inicio sesion']
    combo_operadores.current()
    combo_operadores.grid(column=1, row=1, columnspan = 2)

    label_resultado = tk.Label(window, text='', font=('Calibri ', 15))
    label_resultado.grid(column = 1, row = 6, columnspan = 2)

    boton = tk.Button(window,
                      command=lambda: click_login(
                          label_resultado,
                          entrada1.get(),
                          entrada2.get(),
                          combo_operadores.get()),
                      text='Aceptar',
                      bg='green',
                      font = ('Calibri', 15),
                      fg='black')
    boton.grid(column=1, row=5)

    boton = tk.Button(window,
                      command=lambda: salir(),
                      text='Cancelar',
                      bg='green',
                      font=('Calibri', 15),
                      fg='black')
    boton.grid(column=2, row=5)

    def salir():
        window.destroy()

    window.mainloop()


def login(usuario, passw, operador):
    """
    login comprueba la veracidad o posibilidad de creacion de un usuario o contrasenia.
    :param usuario: nombre inngresado
    :param passw: contrasenia ingresada
    :param operador: si se desea iniciar sesion registrar una nueva cuenta
    :return:dos string, las cuales representan el error o el usuario y contraseña.
    """
    registeredUser=[]   #Lista de todos los usuarios regisrados
    registeredPW=[]     #Lista contrasenias registradas
    Usuarios= open('../archivos/Usuarios.txt', 'r+')
    Passwords= open('../archivos/Passwords.txt','r+')
    for lines in Usuarios:
        lines = lines.rstrip()
        registeredUser.append(lines)
    for lines2 in Passwords:
        lines2=lines2.rstrip()
        registeredPW.append(lines2)
    Usuarios.close()
    Passwords.close()

    if operador == 'Inicio sesion':
        f = 'Error'                 #Errores
        s = 'intentelo de nuevo'
        if usuario in registeredUser:
            if passw in registeredPW:
                return usuario, passw
            else:
                return f, s
        else:
            return f, s
    else:
        f = 'Usuario ya registrado'         #Errores
        s = 'Contraseña ya registrada'
        while usuario != '':
            if usuario in registeredUser:
                return f, 0
            else:
                registeredUser.append(usuario)
                break

        while passw != '':
            if passw in registeredPW:
                return 0, s
            else:
                registeredPW.append(passw)
                break

        usuarios =open('../archivos/usuarios.txt','w')
        for u in registeredUser:
            usuarios.write(str(u)+'\n')
        usuarios.close()

        passwords = open('../archivos/passwords.txt', 'w')
        for p in registeredPW:
            passwords.write(str(p)+'\n')
        passwords.close()

        return usuario, passw

def click_login(label, usuario, passw, operador):
    """
    click_login envia el resultado a imprimir en la interfaz de acuerdo a los return de login
    :param label:
    :param usuario: Usuario ingresado
    :param passw: Contrasenia ingresada
    :param operador: El tipo de acceso que se quiera hacer
    :return: Un label con lo que se quiere escribir en la interfaz
    """
    user, con = login(usuario, passw, operador)         #llamdo a funcion login
    if con == 'intentelo de nuevo' or user == '' or con == '' :
        label.configure(text = 'Error en el inicio de sesión,\n verifique su usuario o contraseña\n e intentelo de nuevo', font=('Calibri', 15))
    elif con == 'Contraseña ya registrada':
        label.configure(text='Contraseña ya registrada,\n intentelo de nuevo',font=('Calibri', 15))
    elif user == 'Usuario ya registrado':
        label.configure(text='Usuario ya registrado,\n intentelo de nuevo', font=('Calibri', 15))
    else:
        con = '*'*(len(passw))
        label.configure(text = 'Bienvenido usuario\t' + str(user) + '\n Contraseña:\t' + str(con), font=('Calibri', 15))


def main():
    init_window()

main()