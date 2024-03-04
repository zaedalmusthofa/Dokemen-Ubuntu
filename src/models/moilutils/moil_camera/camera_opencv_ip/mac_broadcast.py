import socket

import scapy.all as scapy


def broadcast_ip_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    dict_mac_ip = {}
    for element in answered_list:
        dict_mac_ip[element[1].hwsrc] = element[1].psrc

    # dict_mac_ip = {
    #       'fc:34:97:83:68:f8': '192.168.113.1',
    #       '40:8d:5c:19:45:13': '192.168.113.19',
    #       '7c:83:34:b9:33:10': '192.168.113.26',
    #       '94:a6:7e:72:ea:61': '192.168.113.29',
    #       ... }
    return dict_mac_ip


def get_subnet_ip():
    list_subnet_ip = []
    host_name = socket.gethostname()

    ip_addresses = socket.gethostbyname_ex(host_name)

    for ip_address in ip_addresses[2]:
        if ip_address != '127.0.0.1':
            list_subnet_ip.append(ip_address)
    return list_subnet_ip


dict_ip_mac_result = {}
for ip in get_subnet_ip():
    if ip == '0.0.0.0' or ip == '127.0.0.1':
        continue

    scan_one_round = broadcast_ip_mac(ip + '/24')
    dict_ip_mac_result.update(scan_one_round)

print(dict_ip_mac_result)
