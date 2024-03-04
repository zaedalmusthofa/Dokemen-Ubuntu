import json
import os
import subprocess
import sys
import platform


def scan(admin_pwd):
    ip_mac_table = get_subnet_mac_table(admin_pwd)
    return get_dict_id_url_from_mac_table(ip_mac_table)


def get_subnet_mac_table(admin_pwd: str) -> {}:
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.dirname(abs_path)
    scan_subnet_python_file = 'mac_broadcast.py'
    scan_subnet_python_path = abs_dir + '/' + scan_subnet_python_file

    system = platform.system()
    if os.path.isfile(scan_subnet_python_path):
        cmd = sys.executable + ' ' + scan_subnet_python_path
        if system == "Linux":
            try:
                ip_mac_result = subprocess.check_output('echo ' + admin_pwd + '| sudo -S ' + cmd, shell=True)
                ip_mac_result = ip_mac_result.decode()

                return convert_str_to_dict(ip_mac_result)

            except Exception as e:
                error_prompt = '    System returned non-zero exit status 1. Maybe because:\n' \
                               '        1. Python "scapy" module is not install.\n' \
                               '        2. Maybe "admin password" is incorrect.'
                print('[SystemError] ' + abs_path + '\n' + error_prompt)
                return {'SystemError': error_prompt}

        elif system == "Windows":
            try:
                ip_mac_result = subprocess.check_output(cmd, shell=True, text=True)
                return convert_str_to_dict(ip_mac_result)

            except Exception as e:
                error_prompt = '\n    System returned non-zero exit status 1. Maybe because:\n' \
                               '        1. Python "scapy" module is not install.\n' \
                               '        2. Windows "npcap" is not installed.\n' \
                               '           Installation file:"' + abs_dir + '\scapy_installation_windows\\npcap-1.76.exe' + '"'
                print('[SystemError] ' + abs_path + '\n' + error_prompt)
                return {'SystemError': error_prompt}


    else:
        raise FileNotFoundError('No such file "{}" under {}/'.format(scan_subnet_python_file, abs_dir))


def get_dict_id_url_from_mac_table(dict_ip_mac):

    if dict_ip_mac == {}:
        return {}

    dict_cam_mac = read_mac_json()

    dict_total_id_url = {}
    for mac in dict_ip_mac:
        if mac in dict_cam_mac:
            protocol = dict_cam_mac[mac]["protocol"]
            id = dict_cam_mac[mac]["id"]
            suffix = dict_cam_mac[mac]["suffix"]

            ipcam_url = protocol + dict_ip_mac[mac] + suffix
            # Ex: 'rtsp://192.168.113.37:8000/stream.mjpg'

            dict_id_url = {id: ipcam_url}
            # Ex: {'raspberry_pi4_1': 'rtsp://192.168.113.37:8000/stream.mjpg'}

            dict_total_id_url.update(dict_id_url)
            # Ex: {'raspberry_pi4_1': 'rtsp://192.168.113.37:8000/stream.mjpg',
            #      'axis_m3068p_1': ...}

    if list(dict_ip_mac.keys())[0] == 'SystemError':
        return list(dict_ip_mac.values())[0]

    return dict_total_id_url


def read_mac_json():
    abs_path = os.path.abspath(__file__)
    abs_dir = os.path.dirname(abs_path)
    mac_json_file = 'mac.json'
    mac_json_path = abs_dir + '/' + mac_json_file

    f = open(mac_json_path)
    dict_cam_mac = json.load(f)
    # Ex: {'dc:a6:32:e9:0b:8f': {'id': 'raspberry_pi4_1', 'suffix': ':8000/stream.mjpg'}}
    f.close()
    return dict_cam_mac


def convert_str_to_dict(str_mac_ip_table: str):

    if str_mac_ip_table == '{}\n':
        return {}

    str_dict = str_mac_ip_table[1:-1]

    list_mac_ip = str_dict.split(', ')

    dict_mac_ip = {}
    for mac_ip in list_mac_ip:
        mac = mac_ip.split(': ')[0][1:-1]
        ip = mac_ip.split(': ')[1][1:-1]

        dict_mac_ip.update({mac: ip})

    return dict_mac_ip
