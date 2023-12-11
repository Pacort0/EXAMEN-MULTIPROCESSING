from multiprocessing import *
from multiprocessing.connection import PipeConnection

#Explicación de la elección de Pipe: Dada la estructura del ejercicio, encuentro más intuitivo el uso de las tuberías
#Lo que se manda por un extremo se recibe por otro, filtrado y tratado según pide el ejercicio, hasta que 
#el resultado es satisfactorio y se escribe en el fichero correspondiente

#Esta función recibe el nombre del departamento por el que filtrar y el lado izquierdo de la primera tuberia
def filtraDept(departamentoFiltro, tubleft:PipeConnection):
    with open("Examen/Ejercicio02/salarios.txt") as fichero: #Abrimos el fichero de los salarios
        for _ in fichero.readlines(): #Leemos el fichero linea a linea
            linea = _.split(";") #Dividimos la línea por ';'
            departamento = linea[3] #Cogemos el elemento de la línea correspondiente al departamento

            #Eliminamos el salto de línea junto al departamento, y si el departamento resultante es igual que el enviado por parámetros
            #Para poder abarcar todos los departamentos en el filtro, tenemos que añadir a mano los que tengan espacios en el nombre. 
            #Es feo, pero no recuerdo cómo crear una clase enumerada en python ahora mismo
            if departamento.strip() == departamentoFiltro or departamento == "Recursos Humanos": 
                lineaSinDept = linea[0:3] #Hacemos 'slicing' de la línea para llevarnos los elementos que deseemos.
                tubleft.send(lineaSinDept) #Enviamos la línea sin el departamento
        tubleft.send(None) #Una vez nos quedemos sin empleados en la lista, enviamos 'None'
    
#Esta función recibe el salario minimo por el que filtrar, el lado derecho de la primera tuberia y el izquierdo de la segunda
def salarioMinimo(salarioMin, tubright:PipeConnection, tubleft:PipeConnection ):
    empleado = tubright.recv() #Recogemos lo enviado por la primera tuberia
    while empleado is not None: #si lo recogido no es 'None'
        salario = empleado[2] #el salario se encuentra en la tercera posición de lo recogido
        if int(salario) >= salarioMin: #Si el salario es mayor o igual al del empleado recibido
            tubleft.send(empleado) #Enviamos la información del empleado a la última línea
        empleado = tubright.recv() #Recogemos al siguiente empleado
    tubleft.send(None) #Cuando no queden más elementos que recoger, enviamos 'None'

#Esta función recibe el extremo derecho de la tubería de la segunda tubería
def escribeEmpleados(tubright:PipeConnection):
    empleado = tubright.recv() #Recogemos la información enviada
    while empleado is not None: #Mientras esta información no sea 'None'
        with open("Examen/Ejercicio02/empleados.txt", "a") as fichero: #Abrimos el fichero donde vamos a escribir los empleados
            fichero.write(f"{empleado[1]} {empleado[0]}, {empleado[2]}\n") #Escribimos los datos del empleado según el formato indicado
        empleado = tubright.recv() #Recogemos al siguiente empleado

#main
if __name__ == "__main__":
    departamento = input("Introduzca un departamento: ") #Pedimos un departamento al usuario
    salarioMin = int(input("Introduzca el salario mínimo: ")) #Pedimos el salario mínimo al usuario

    #Creamos las tuberias
    tubleft1, tubright1 = Pipe() #Creamos las tuberias
    tubleft2, tubright2 = Pipe()

    #Creamos los procesos y les asignamos una función y los parámetros correspondientes
    proceso1 = Process(target=filtraDept, args=(departamento, tubleft1))
    proceso2 = Process(target=salarioMinimo, args=(salarioMin, tubright1, tubleft2))
    proceso3 = Process(target=escribeEmpleados, args=(tubright2,))

    #Comenzamos los procesos
    proceso1.start()
    proceso2.start()
    proceso3.start()

    #Ejecutamos los procesos
    proceso1.join()
    proceso2.join()
    proceso3.join()

    #Informamos del fin de los procesos
    print("Procesos finalizados")