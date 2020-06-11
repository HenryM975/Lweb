#on linux
import scapy.all as scp
import subprocess
import random
while True:
    inp = input("write something: ")
    if inp == "--scaner" or inp == "-s":
        def scan(ip):
        #    scp.arping(ip)
        #scan("192.168.0.1/24") #mac+ip in result /24 - for all in subnet
            arp_request = scp.ARP(pdst=ip)
            broadcast = scp.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            #answered_list, unanswered_list = scp.srp(arp_request_broadcast, timeout=1)
            answered_list = scp.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            #print("IP\t\t\t\tMAC Address\n---------------------------------------")
            clients_list = []
            for element in answered_list:
                client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
                clients_list.append(client_dict)
                #print(element[1].psrc + "\t\t" + element[1].hwsrc)#ip/mac
            #print(clients_list)
            return clients_list

        def print_result(results_list):
            print("IP\t\t\t\tMAC Address\n---------------------------------------")
            for client in results_list:
                print(client["ip"] + "\t\t" + client["mac"])




        scan_result = scan("192.168.0.1/24")
        print_result(scan_result)
    elif inp == "--changemac" or inp == "-cm":
        #######################
        def Randnum():
            rand = random.uniform(10, 99)
            rand = int(rand)
            rand = str(rand)
            return rand
        newmac = "".join(Randnum()) + ":" + "".join(Randnum()) + ":" + "".join(Randnum()) + ":" + "".join(Randnum()) + ":" + "".join(Randnum()) + ":" + "".join(Randnum())
        ########################
        #oldmac = subprocess.call("ifconfig", shell=True)
        subprocess.call("ifconfig wlan0 down", shell = True)
        subprocess.call("ifconfig wlan0 hw ether " + newmac, shell = True)#randomizing
        subprocess.call("ifconfig wlan0 up", shell=True)
        #newmac = subprocess.call("ifconfig", shell=True)#parsing
        #print("your old mac: " + oldmac)
        print("your new mac: " + newmac)#SIOCSIFHWADDR: Невозможно назначить запрошенный адрес #предохранитель с рециклом  в случае ошибки
    elif inp == "--help" or inp == "-h":
        print("commands: \n'--scaner' '-s' wifi scanning \n'--changemac' '-cm' change mac addres#\n'--help' '-h' info \n '--quit' '-q' output\n")
    elif inp == "--quit" or inp == "-q":
        break
    else:
        print("command error")