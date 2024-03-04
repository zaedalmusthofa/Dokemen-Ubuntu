import os
import subprocess
import sys


def get_subnet_mac_table(admin_pwd: str) -> {}:
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.dirname(abs_path)
    scan_subnet_python_file = 'mac_broadcast.py'
    scan_subnet_python_path = abs_dir + '/' + scan_subnet_python_file

    if os.path.isfile(scan_subnet_python_path):
        cmd = sys.executable + ' ' + scan_subnet_python_path

        try:
            ip_mac_result = subprocess.check_output('echo ' + admin_pwd + '| sudo -S ' + cmd, shell=True)
            ip_mac_result = ip_mac_result.decode()

            return convert_str_to_dict(ip_mac_result)

        except Exception as e:
            print('[SystemError] ' + abs_path + '\n'
                                                '    System returned non-zero exit status 1. Maybe because:\n'
                                                '        1. Python "scapy" module is not install.\n'
                                                '        2. Maybe "admin password" is incorrect.')
            return {'SystemError': 'System returned non-zero exit status 1. [ Maybe sudo password is incorrect. ]'}

    else:
        raise FileNotFoundError('No such file "{}" under {}/'.format(scan_subnet_python_file, abs_dir))


def convert_str_to_dict(str_mac_ip_table: str):
    str_dict = str_mac_ip_table[1:-1]

    list_mac_ip = str_dict.split(', ')

    dict_mac_ip = {}
    for mac_ip in list_mac_ip:
        mac = mac_ip.split(': ')[0][1:-1]
        ip = mac_ip.split(': ')[1][1:-1]

        dict_mac_ip.update({mac: ip})

    return dict_mac_ip


ip_mac_table = get_subnet_mac_table('mcut1234')

import pprint

# Prints the nicely formatted dictionary
pprint.pprint(ip_mac_table)
