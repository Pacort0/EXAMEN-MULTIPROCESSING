from multiprocessing import *
import random

#Esta función recibe por parámetros el nombre del fichero a abrir/crear. Es así porque le vamos a ir pasando un nombre distinto desde el main con cada iteración
def horasAleatorias(nombreFichero):
    with open(nombreFichero, "w") as fichero:
        for hora in range(24): #Para cada hora escribimos una temperatura
            temperatura = round(random.uniform(0,20), 2) #Número aleatorio entre 0 y 20 que indica la temperatura
            fichero.write(f"{temperatura}\n") #Escribimos la temperatura de la hora

#Esta función recibe el nombre del fichero que debe abrir y el día al que corresponde el fichero. Todo se pasa desde el main con cada iteración
def tempMaxima(nombreFichero, dia): 
    maxima = 0.0 #Variable donde vamos a guardar la temperatura máxima del día, inicializada a 0, al ser esta la temperatura mínima a registrar
    with open(nombreFichero, "r") as fichero: #Abrimos el archivo de donde leeremos las temperaturas del día
        for temperatura in fichero.readlines(): #Iteramos línea a línea del fichero
            if(float(temperatura) > maxima): #Si la temperatura leída es mayor a la registrada actualmente en ese día
                maxima = float(temperatura) #Cambiamos la temperatura máxima a la recién leída
    with open("Examen/Ejercicio01/maximas.txt", "a") as ficheroMaxima: #Abrimos/Creamos el fichero de máximas
        ficheroMaxima.write(f"{dia} : {maxima}\n") #Escribimos la máxima con el formato indicado

#Esta función recibe el nombre del fichero a abrir y el día al que corresponde el fichero. Funciona igual que la función anterior, pero trabaja con las temperaturas más bajas
def tempMinima(nombreFichero, dia): 
    minima = 20.0 #Variable donde vamos a guardar la temperatura minima registrada, inicializada a 20, al ser esta la máxima temperatura a registrar
    with open(nombreFichero, "r") as fichero:
        for temperatura in fichero.readlines():
            if(float(temperatura) < minima):
                minima = float(temperatura)
    with open("Examen/Ejercicio01/minimas.txt", "a") as ficheroMinima:
        ficheroMinima.write(f"{dia} : {minima}\n")

#Esta función embellece el título de los archivos y de los días
#Recibe por parámetros el día (iteración) y le pone un 0 delante en función de si está entre 0 y 10, si no, lo devuelve tal cual
def diaBonito(dia):
    diaBonitoString = ""
    if(dia < 10):
        diaBonitoString = f"0{dia}"
    else:
        diaBonitoString = str(dia)

    return diaBonitoString
 
#main
if __name__ == "__main__":
    procesosNotas = [] #En este array vamos a guardar todos los procesos de generación de temperaturas comenzados para después ejecutarlos todos simultáneamente
    procesosMaxMin = [] #En este array vamos a guardar todos los procesos de filtrado de temperaturas máx y mín comenzados para después ejecutarlos todos simultáneamente
 
    for i in range(31): #31 días
        proceso1 = Process(target=horasAleatorias, args=(f"Examen/Ejercicio01/dias/{diaBonito(i+1)}-12.txt",))
        proceso1.start() #Comienza el proceso
        procesosNotas.append(proceso1) #Agregamos el proceso a la lista
    
    #una vez están todos los procesos en la lista
    for proceso in procesosNotas: 
        proceso.join() #Ejecutamos los procesos uno a uno
    
    for i in range(31): #31 días en los que filtrar
        proceso2 = Process(target=tempMaxima, args=(f"Examen/Ejercicio01/dias/{diaBonito(i+1)}-12.txt", f"{diaBonito(i+1)}-12"))
        proceso3 = Process(target=tempMinima, args=(f"Examen/Ejercicio01/dias/{diaBonito(i+1)}-12.txt", f"{diaBonito(i+1)}-12"))
        proceso2.start()  #Comienza el proceso
        proceso3.start()  #Comienza el proceso
        procesosMaxMin.append(proceso2) #Agregamos el proceso a la lista
        procesosMaxMin.append(proceso3) #Agregamos el proceso a la lista
    
    for proceso in procesosMaxMin:
        proceso.join() #Ejecutamos los procesos uno a uno, primero el de máximas, luego el de mínimas
    
