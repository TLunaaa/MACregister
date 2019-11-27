from scapy.all import AsyncSniffer,sniff
from scapy.layers.dot11 import Dot11
import os
import time

mac_list = []

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
    print " M     M         M     M  A    A            A    A  C  R E G I S T E R  C "
    print " MMMMMMM         MMMMMMM AAAAAA              AAAAAA CCCCCCCCCCCCCCCCCCCCC "
    print "                                                                          "

def waiter(wait_time):
    #CONST
    X = 0.5
    WAIT_TEXT = []
    WAIT_TEXT.append(" Sniffing packets      ")
    WAIT_TEXT.append(" Sniffing packets #    ")
    WAIT_TEXT.append(" Sniffing packets ##   ")
    WAIT_TEXT.append(" Sniffing packets ###  ")
    WAIT_TEXT.append(" Sniffing packets #### ")
    WAIT_TEXT.append(" Sniffing packets #####")
    WAIT_TEXT.append(" Sniffing packets ######")
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
            
# Sniff packets during a certain time
def mac_sniffer(st = 60):
    IFACE = "mon0"
    SNIFF_TIME = st
    t = AsyncSniffer(iface=IFACE,prn=store_packets)
    t.start()
    waiter(SNIFF_TIME)
    t.stop()

#Stores no duplicates packets in array 
# >>> packet : every packet sniffed
def store_packets(packet):
    if packet.haslayer(Dot11) :
        if packet.type == 0 and packet.subtype == 4: #subtype = Probe Request
            if packet.addr2 not in mac_list:         #addr2 = Sender MAC address
                mac_list.append(packet.addr2)
        if packet.type == 0 and packet.subtype == 5: #subtype = Probe Response
            if packet.addr1 not in mac_list:         #addr1 = Reciever MAC address
                mac_list.append(packet.addr1)

def show_sniffed():
    print_logo()
    print " ##Devices MAC addresses##"
    for x in range(len(mac_list)):
        print (" MAC %d %s" %(x,mac_list[x]))

def main():
    print_logo()
    mac_sniffer(10)
    show_sniffed()


main()
