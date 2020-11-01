from os import remove

def catalogo(opcion):
    """
    catalogo da la posibilidad de entrar en contacto con un catalogo de libros virtual
    dada una opcion:
            1.Imprime y guarda la informacion del libro agregado.
            2.Muestra el archivo, el cual contiene toda los datos de los libros
            3.imprime la informacion del prestamo dependiendo de su disponibilidad
    :param opcion: tipo de contacto con el catalogo
            1. Agregar un nuevo libro al catalogo
            2. Mostrar todos los libros del catalogo
            3. Entrar al sistema de prestamos de los libros
    :return: None
    """
    libros = []
    opciones = ['1','2','3']
    while opcion in opciones:
        if opcion == "1":
            agregar_libro()

        elif opcion == "2":
            mostrar_libros(libros)

        elif opcion == "3":
            prestamos(libros)
        opcion = menu()
    if opcion == '4':
        print('Gracias por usar el programa')
    else:
        print("Debes  elegir una opcion")
def agregar_libro():
    """
    agregar_libros, agrega nuevos libros al catalogo, estso deben tener sus datos
    :return: None
    imprime los principales datos que fueron guardados
    """
    # Todos los datos escenciales que se piden para agregar al catalogo
    print("Nuevo Registro")
    with open("../archivos/ejemplo.txt", "a") as archivo:

        nombre = input("Titulo: ")
        while nombre == '':
            nombre = input('Título')
        autor = input("Autor: ")
        fecha = input("Año de publicación: ")
        descripcion = input("Descripción: ")
        while descripcion == '':
            descripcion = input('Descripcion: ')
        editorial = input("Editorial: ")

        if autor == '':
            autor = 'Desconocido'
        if fecha == '':
            fecha = 'Desconocida'
        if editorial == '':
            editorial = 'Desconocida'

        print("Se ha guardado: ", nombre, ", del autor:", autor)
        print(f'{nombre}\n{autor}\n{fecha}\n{descripcion}\n{editorial}\n')

        archivo.write(nombre + ",0," + autor + "," + fecha + "," + editorial + "," + descripcion + "\n")  # Guardado de los datos en el archivo ejemplo.txt
        archivo.close()

def mostrar_libros(libros):
    """
    mostrar_libros, muestra todo el catalogo de libros con sus respectivos datos
    :param libros: lista con cada libro
    :return: None
    Imprime la lista de catalogo
    """
    print("Mostrar Libros")
    archivo = open("../archivos/ejemplo.txt", "r")
    lines = archivo.readlines()
    for line in lines:  # conversion de los datos del archivo en listas por cada libro
        datos = line.split(',')
        libros.append(datos)
    for l in libros:
        for i in l:
            if i == l[-1]:
                print(i, end='')
            else:
                if i == '0':
                    print('DISPONIBLE')
                elif i == '1':
                    print('PRESTAMO ACTIVO')
                else:
                    print(i)
        print('_____________________________________________________\n')
        archivo.close()

def prestamos(libros):
    """
    prestamos lee el catalogo y da los libros en prestamo de acuerdo a su disponibilidad
    guarda el registro del prestamo en un archivo.txt.
    :param libros: lista de todos los libros del catalogo con sus datos
    :return: None
    """
    print('LISTA DE LIBROS')
    archivo = open("../archivos/ejemplo.txt", "r+")
    lines = archivo.readlines()
    for line in lines:
        datos = line.split(',')
        libros.append(datos)
    for h in range(len(libros)):
        print(libros[h][0])
        print('_________________________________')
    titulo = input('Ingrese el nombre del libro que quiere pedir prestado:\n')
    bandera = False
    for i in range(len(libros)):  # Comprobacion disponibilidad libro a partir de
        if libros[i][0] == titulo:  # el 1 y 0.
            libros[i][1] = '1'
            bandera = True
            break
        else:
            continue
    archivo.close()
    archivo = open("../archivos/ejemplo.txt", "w")
    for l in libros:
        l1 = ''
        for i in l:  # Guardado de los datos actualizados en el archivo
            if i == l[-1]:
                l1 += i
            else:
                l1 += i + ','
        archivo.write(str(l1))
    archivo.close()
    if bandera:
        nombre = input('Usuario:\n')  # Datos de prestamo
        fecha = input('Fecha vigencia: \n')
        print(f'Se ha realizado el prestamo de el texto {titulo} a nombre de {nombre}\n')
        archivo = open('../archivos/prestamos.txt', 'w')
        archivo.write(titulo + ',' + nombre + ',' + fecha + '\n')  # Guardado de datos en el archivo prestamos.txt
    else:
        print(f'El libro {titulo} no esta disponible\n')

def menu():
    """
    menu imprime el menu del catalogo de acuerdo a sus opciones
    :return: opcion que el usuario elija 1, 2, 3 o 4
    """
    print("Bienvenido,\n Ingrese 1 para\t Ingresar un nuevo libro\n Ingrese 2 para\t Mostrar el catalogo\n Ingrese 3 para\t Prestamo\n Ingrese 4 para\t Terminar el programa")
    opcion = input()
    return opcion

def main():
    opcion = menu()
    catalogo(opcion)

main()