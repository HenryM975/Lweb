import scapy.all as scp

def sniff(interfase):
    scp.sniff(ifase=interfase, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    print(packet)

sniff("eth0")#or eth0 if you need