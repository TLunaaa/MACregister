from scapy.all import AsyncSniffer,sniff
from scapy.layers.dot11 import Dot11
from datetime import datetime
import registro
import os
import time

mac_list = []
time_stamp_list = []

"""Se encarga de limpiar la pantalla y dibujar el logo del programa."""
def print_logo():
    os.system('clear')
    print "                                                                          "
    print " MMMMMM           MMMMMM           AAAAAA           CCCCCCCCCCCCCCCCCCCCC "              
    print " M      M       M      M          A      A          C                   C "
    print " M        M   M        M         A   AA   A         C    CCCCCCCCCCCCCCCC "
    print " M          M          M        A   A  A   A        C    C                "
    print " M                     M       A   A    A   A       C    C                "
    print " M     M         M     M      A   AAAAAAAA   A      C    C                "
    print " M     M  M   M  M     M     A                A     C    C                "
    print " M     M    M    M     M    A    AAAAAAAAAA    A    C    C                "
    print " M     M         M     M   A    A          A    A   C    CCCCCCCCCCCCCCCC "
    print " M     M         M     M  A    A            A    A  C                   C "
    print " MMMMMMM         MMMMMMM AAAAAA              AAAAAA CCCCCCCCCCCCCCCCCCCCC "
    print "                                                      R E G I S T E R     "

""" Muestra una pantalla de espera correspondiente al tiempo que se esta sniffeando.
pre: wait_time es numerico != null
"""
def waiter(wait_time):
    #CONST
    X = 0.5
    WAIT_TEXT = []
    WAIT_TEXT.append(" Buscando MACs       ")
    WAIT_TEXT.append(" Buscando MACs #     ")
    WAIT_TEXT.append(" Buscando MACs ##    ")
    WAIT_TEXT.append(" Buscando MACs ###   ")
    WAIT_TEXT.append(" Buscando MACs ####  ")
    WAIT_TEXT.append(" Buscando MACs ##### ")
    WAIT_TEXT.append(" Buscando MACs ######")
    #VARIABLES
    i = 0
    total_time = wait_time

    while total_time >= X:
        print_logo()
        print(WAIT_TEXT[i])
        time.sleep(X)
        total_time -=X
        i+=1
        if i==7:
            i = 0
            
""" Sniffea paquetes de manera asincronica durante el tiempo st, el cual es 10 por defecto
    y los almacena en la lista mac_list y el timestamp en time_stamp_list.
pre: st es numerico
post: Se tiene la listas mac_list y time_stamp_list cargadas con los dispositivos activos y su ultima aparicion respectivamente.
"""
def mac_sniffer(st = 10):
    IFACE = "mon0"
    SNIFF_TIME = st
    t = AsyncSniffer(iface=IFACE,prn=store_packets)
    t.start()
    waiter(SNIFF_TIME)
    t.stop()

""" Por cada paquete sniffeado analiza si se debe almacenar en la lista o no
    >>packet.type == 0 -> Management frame
        >>subtype == 8 -> Beacon
    >>packet.type == 2 -> Data frame

    >>packet.addr == ff:ff:ff:ff:ff:ff -> Broadcast
    >>packet.addr1 -> La direccion MAC fuente
    >>packet.addr2 -> La direccion MAC destino
"""
def store_packets(packet):
    if packet.haslayer(Dot11) :
        if packet.type == 0 and packet.subtype != 8:
            if packet.addr1 != "ff:ff:ff:ff:ff:ff":
                if packet.addr1 not in mac_list:         
                    mac_list.append(packet.addr1)
                    time_stamp_list.append(datetime.now())
                else:
                    time_stamp_list[mac_list.index(packet.addr1)] = datetime.now()
            if packet.addr2 != "ff:ff:ff:ff:ff:ff":
                if packet.addr2 not in mac_list:         
                    mac_list.append(packet.addr2)
                    time_stamp_list.append(datetime.now())
                else:
                    time_stamp_list[mac_list.index(packet.addr2)] = datetime.now()
        if packet.type == 2 :
            if packet.addr1 != "ff:ff:ff:ff:ff:ff":
                if packet.addr1 not in mac_list:         
                    mac_list.append(packet.addr1)
                    time_stamp_list.append(datetime.now())
                else:
                    time_stamp_list[mac_list.index(packet.addr1)] = datetime.now()
            if packet.addr2 != "ff:ff:ff:ff:ff:ff":
                if packet.addr2 not in mac_list:         
                    mac_list.append(packet.addr2)
                    time_stamp_list.append(datetime.now())
                else:
                    time_stamp_list[mac_list.index(packet.addr2)] = datetime.now()

def main():
    print_logo()
    f = open("archivoMac.txt","a")
    f.close()
    accion = raw_input(" Presione:\n a: Agregar un cliente\n e: Eliminar un cliente\n m: Mostrar las MACs activas\n f: Finalizar\n")
    while(accion!="f"):
        if(accion=="a"):
            print_logo()
            mac = raw_input(" Ingrese la MAC a registrar\n")
            nombre =  raw_input(" Ingrese el nombre del cliente\n")
            registro.agregar(mac.lower(), nombre)
            print(" Se agrego correctamente\n")
        elif(accion=="e"):
            print_logo()
            modo = raw_input("Como desea eliminar?\nn: Por nombre\nm: Por MAC\n")
            if(modo == "n"):
                nombre = raw_input("Ingrese el nombre del cliente a eliminar\n")
                nombre+="\n"
                registro.eliminarNombre(nombre)
                print("Se elimino correctamente\n")
            elif(modo == "m"):
                mac = raw_input("Ingrese la MAC del cliente a eliminar\n")
                registro.eliminarMac(mac)
                print("Se elimino correctamente\n")
            else:
                print("No se reconoce el metodo a eliminar, intente de nuevo")
        elif(accion=="m"):
            #macs= obtener las mac del aire
            #dur = raw_input("Inserte la duracion en segundos de la busqueda: \n")
            act = raw_input("Mostrar solo clientes conocidos Y/N: \n")
            mac_sniffer()
            print_logo()
            print(" [  Ultima vez Activo ] -        MAC        -    Nombre ")
            print " --------------------------------------------------------"
            print("")
            if act.upper() == "Y":
                registro.mostrarActivos(mac_list,time_stamp_list,True)
            else:
                registro.mostrarActivos(mac_list,time_stamp_list,False)
            raw_input("Presione Enter para continuar...")
        else:
            print(" No se reconoce la accion\n")
        print_logo()
        accion = raw_input(" Presione:\n a: Agregar un cliente\n e: Eliminar un cliente\n m: Mostrar las MACs activas\n f: Finalizar\n")
    if accion == "f":
        os.system("clear")


main()
