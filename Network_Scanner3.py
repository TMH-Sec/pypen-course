#!/usr/bin/env python3

from scapy.layers.l2 import ARP, Ether, srp
from subprocess import check_output
from re import search
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help='interface connected to target network e.g. eth0')
    network = parser.parse_args()
    return network


def get_network_id(interface):
    ip_a_s = check_output('ip address show | grep inet | grep {}'.format(interface), shell=True)
    ip_a_s = str(ip_a_s)
    network_id_search = search(r'\d+.\d+.\d+.\d+/\d+', ip_a_s)
    if network_id_search:
        return network_id_search.group()
    else:
        print('[+] Could not find Network ID')


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
network_id = get_network_id(arguments.interface)
scan_result = scan(network_id)
print_arp_result(scan_result)
