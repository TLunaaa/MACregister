import os

"""Agrega la mac con su nombre al archivo
pre: mac y nombre son strings != null
post: actualiza el archivo con la nueva mac y su nombre"""

def agregar(mac, nombre):
    f = open("archivoMac.txt","r")
    lineas = f.readlines()
    f.close()
    i=0     #variable para recorrer las lineas del archivo de macs
    bandArch = True     #signfica que la mac no esta en el archivo
    while((bandArch) and  (i<len(lineas))):     #verifico que no exista la mac
        lineasSplit = lineas[i].split("-")
        if(mac==lineasSplit[0]):
            bandArch = False    #la mac ya esta registrada en el archivo
        i+=1
    if (bandArch):      #la mac no esta registrada
        f = open("archivoMac.txt","a")   
        macString = mac+"-"+nombre
        f.write(macString+"\n")
    else:
        print("La mac ya se encontraba registrada")
    f.close()

"""Elimina la mac y su nombre del archivo de texto.
pre: mac es un string != null
post: actualiza el archivo sin la linea perteneciente a la mac. Si la mac no existe, imprime un cartel"""

def eliminarMac(mac):  
    f = open("archivoMac.txt","r")
    lineas = f.readlines()
    f.close()
    aux = open("archivoAuxiliar.txt","w")
    try:
        nombre = obtenerNombre(mac)
        macString = mac+"-"+nombre      #concateno strings para que sean igual que las lineas del archivo
        for linea in lineas:
            if(linea!=macString):
                aux.write(linea)
    except Exception:
        print("La mac no estaba registrada")
    finally:
        aux.close()
        os.remove("archivoMac.txt")
        os.rename("archivoAuxiliar.txt","archivoMac.txt")

"""Elimina el nombre y su mac del archivo de texto.
pre: nombre es un string != null
post: actualiza el archivo sin la linea perteneciente al nombre. Si el nombre no existe, imprime un cartel"""

def eliminarNombre(nombre):
    f = open("archivoMac.txt","r")
    lineas = f.readlines()
    f.close()
    aux = open("archivoAuxiliar.txt","w")
    try:
        mac = obtenerMac(nombre)
        nombreString = mac+"-"+nombre    #concateno strings para que sean igual que las lineas del archivo
        for linea in lineas:
            if(linea!=nombreString):
                aux.write(linea)
    except Exception:
        print("El nombre no estaba registrado")
    finally:
        aux.close()
        os.remove("archivoMac.txt")
        os.rename("archivoAuxiliar.txt","archivoMac.txt")
        

"""Obtiene el nombre de la mac enviada por parametro
pre: mac es un string != null
post: devuelve el nombre asociado a ese mac o desconocido si no esta asociado"""

def obtenerNombre(mac):
    f = open("archivoMac.txt","r")
    lineas = f.readlines()
    f.close
    bandArch = True
    i=0
    while((bandArch) and  (i<len(lineas))):     #verifico que exista la mac
        lineasSplit = lineas[i].split("-")
        if(mac==lineasSplit[0]):
            nombre = lineasSplit[1]
            bandArch = False    #se encontro la mac
        i+=1
    if(not bandArch):       #la mac existe
        return nombre
    else:
        raise Exception("No se encontro la mac")

"""Obtiene la mac del nombre enviado por parametro
pre: nombre es un string != null
post: devuelve la mac asociada a ese nombre
throw exception: lanza excepcion del tipo Exception si el nombre enviado por parametro no existe"""

def obtenerMac(nombre):
    f = open("archivoMac.txt","r")
    lineas = f.readlines()
    f.close
    bandArch = True
    i=0
    while((bandArch) and  (i<len(lineas))):     #verifico que exista la mac
        lineasSplit = lineas[i].split("-")
        if(nombre==lineasSplit[1]):
            mac = lineasSplit[0]
            bandArch = False    #se encontro la mac
        i+=1
    if(not bandArch):       #la mac existe
        return mac
    else:
        raise Exception("No se encontro el nombre")

"""Muestra las macs que se encuentran activas con su respectivo nombre
pre: macs es un arreglo de las macs que se encuentran activas != null
post: imprime por pantalla las macs activas con su nombre"""

def mostrarActivos(macs):
    for i in range(0, len(macs)):
        try:
            nombre = obtenerNombre(macs[i])
            print(str(i) +": "+macs[i]+"-"+nombre)
        except Exception:
            print(str(i) +": "+macs[i]+"-Desconocido\n")

    