#!/usr/bin/env python3

import optparse
import random
import re
import subprocess


def get_mac_args():
    parser = optparse.OptionParser()
    parser.add_option('-n', '--nic', dest='nic', help='specify a network interface (nic)')
    parser.add_option('-m', '--new-mac', dest='new_mac', help='specify a new MAC address')
    parser.add_option('-r', '--random-mac', action='store_true', dest='randomness', default=False,
                      help='generate random SLAP address')
    (values, modifiers) = parser.parse_args()
    if not values.nic:
        parser.error('[-] Please specify a network interface (nic), use --help for more info.')
    if not values.randomness:
        if not values.new_mac:
            parser.error('[-] Please specify a new MAC address, use --help for more info.')
    return values


def change_mac(nic, mac, randomness):
    if randomness:
        oui = '02:00:00:'
        unq = str(hex(random.randint(0, 255)))[2:] + ":" + \
              str(hex(random.randint(0, 255)))[2:] + ":" + str(hex(random.randint(0, 255)))[2:]
        mac = oui + unq
    subprocess.call('ip link set dev ' + nic + ' down', shell=True)
    subprocess.call('ip link set dev ' + nic + ' address ' + mac, shell=True)
    subprocess.call('ip link set dev ' + nic + ' up', shell=True)


def get_current_mac(nic):
    ip_link_result = subprocess.check_output('ip link show ' + nic + ' | grep link', shell=True)
    ip_link_result = str(ip_link_result)
    mac_search = re.search(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', ip_link_result)
    if mac_search:
        return mac_search.group(0)
    else:
        print('[-] Could not read MAC address')


arguments = get_mac_args()
pre_mac = get_current_mac(arguments.nic)
print('Current MAC = ' + pre_mac)
change_mac(arguments.nic, arguments.new_mac, arguments.randomness)
new_mac = get_current_mac(arguments.nic)
if pre_mac == arguments.new_mac:
    print('Stuck in a rut? That is already the MAC!')
if arguments.new_mac == new_mac and pre_mac != new_mac:
    print('[+] MAC address was successfully changed to ' + new_mac)
if arguments.randomness:
    if pre_mac != new_mac:
        print('My that was random! MAC address is now ' + new_mac)
    if pre_mac == new_mac:
        print('REEEEEE! Something went wrong!')
else:
    print('[-] MAC address did not change.')
