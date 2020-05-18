#!/usr/bin/env python3

from scapy.layers.l2 import ARP, Ether, srp
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target-network', dest='target', help='Target Network xx.xx.xx.xx/xx')
    network = parser.parse_args()
    return network


def scan(network):
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1)[0]
    arp_dictionary_list = []
    for element in answered_list:
        arp_dictionary_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return arp_dictionary_list


def print_arp_result(results_list):
    print('IP\t\t\tMAC ADDRESS\n-----------------------------------------')
    for client in results_list:
        print(client['ip'] + '\t\t' + client['mac'])


arguments = get_arguments()
scan_result = scan(arguments.target)
print_arp_result(scan_result)
