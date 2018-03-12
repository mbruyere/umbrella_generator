#!/usr/bin/env python3

# Copyright (C) 2018 Marc Bruyere.
# Copyright (C) 2018 The University of Tokyo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import csv
from docopt import docopt
from pathlib import Path
import ipaddress
from subprocess import call
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as qs
from settings import *
yaml = YAML()

def load_csv(csvfilename):
    '''Laod the CSV file  and return an OrderedDic'''
    list_load = []

    with open(csvfilename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            list_load.append(line)
        return list_load

def check_input_consistency():
    '''  todo add more verification like no the same port#  '''
    try:
        ipaddress.IPv6Address(list_load[i]['addr_ipv6'])
        ipaddress.ip_address(list_load[i]['addr_ipv4'])
        return True
    except ValueError as e:
        print(e)
        return False


def HexInt(i):
    ''' function to insert right hexa dpids '''
    stri = "0x" + hex(i)[2:].upper().zfill(1)
    return yaml.load(stri)


def Braket(i):
    ''' function to remove the brackets for the Groupe faiover buckets'''
    return yaml.load(i)


def one_switch(list_load):
    ''' Function generating the faucet config for a single OF switch'''
    data = {'vlans': {vlan_name: {'vid': 100, 'description': qs(vlan_name)}}, 'dps': {'sw1': {'dp_id': HexInt(dp_id_sw1), 'hardware': qs(sw1_type), 'interfaces': {1: {'name': qs(
        'link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1}}}}, 'acls': {1: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}]}}

    for i in range(len(list_load)):
        data['dps']['sw1']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
            list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 1}
        data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                               'output': {'port': int(list_load[i]['port'])}}}})
        data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
            list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
        data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
            list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
    data['acls'][1].pop(0)
    data['acls'][1].append({'rule': {'actions': {'allow': 0}}})
    return(data)

def one_legacy(data):
    print('one_legacy not yet')
    pass

def two_legacy(list_load):
    data = {'vlans': {'PIXIE': {'vid': 100, 'description': qs(vlan_name)}}, 'dps': {'sw1': {'dp_id': HexInt(dp_id_sw1), 'hardware': qs(sw1_type), 'interfaces': {1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}, 2: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}}}, 'sw2': {'dp_id': HexInt(0x2), 'hardware': qs(
    sw2_type), 'interfaces': {1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}, 2: {'name': 'link', 'description': 'link', 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}}}}, 'acls': {1: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}], 2: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}]}}
    for i in range(len(list_load)):
        if list_load[i]['switch'] == 'sw1' and list_load[i]['status'] == 'Production':
            data['dps']['sw1']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
                list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}
            data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

            data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': i, 'ports': Braket('[' + sw1_primary_port + ',' + sw1_backup_port + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 100 + i, 'ports': Braket('[' + sw1_primary_port + ',' + sw1_backup_port + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 200 + i, 'ports': Braket('[' + sw1_primary_port + ',' + sw1_backup_port + ']')}}}}})

        elif list_load[i]['switch'] == 'sw2' and list_load[i]['status'] == 'Production':
            data['dps']['sw2']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
                list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}
            data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 600 + i, 'ports': Braket('[' + sw2_primary_port + ',' + sw2_backup_port + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 700 + i, 'ports': Braket('[' + sw2_primary_port + ',' + sw2_backup_port + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 800 + i, 'ports': Braket('[' + sw2_primary_port + ',' + sw2_backup_port + ']')}}}}})

            data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

    data['acls'][1].pop(0)
    data['acls'][2].pop(0)
    data['acls'][1].append({'rule': {'actions': {'allow': 0}}})
    data['acls'][2].append({'rule': {'actions': {'allow': 0}}})
    return(data)

def triangle(list_load):
    data = {'vlans': {'tousix': {'vid': 100, 'description': qs(vlan_name)}}, 'dps': {'Edge1': {'dp_id': HexInt(dp_id_Edge1), 'hardware': qs(sw1_type), 'interfaces': {1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}, int(sw1_portnum_to_sw2): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}, int(sw1_portnum_to_sw3): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 1, 'opstatus_reconf': False}}
                                                                                           }, 'Edge2': {'dp_id': HexInt(0x2), 'hardware': qs(sw2_type), 'interfaces': {1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}, int(sw2_portnum_to_sw1): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}, int(sw2_portnum_to_sw3): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 2, 'opstatus_reconf': False}}}, 'Edge3': {'dp_id': HexInt(0x3), 'hardware': qs(sw3_type), 'interfaces': {1: {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 3, 'opstatus_reconf': False}, int(sw3_portnum_to_sw1): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 3, 'opstatus_reconf': False}, int(sw3_portnum_to_sw2): {'name': qs('link'), 'description': qs('link'), 'native_vlan': 100, 'acl_in': 3, 'opstatus_reconf': False}}                                                                                                                                                                                                                                                                                                                                                                                                              }}, 'acls': {1: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}], 2: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}], 3: [{'rule': {'dl_dst': '00:00:00:00:00:01', 'actions': {'output': {'port': 1}}}}]}}
    for i in range(len(list_load)):
        if list_load[i]['switch'] == 'Edge1' and list_load[i]['status'] == 'Production':
            data['dps']['Edge1']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
                list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 1}
            data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

            data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 1+ i, 'ports': Braket('[' + sw2_portnum_to_sw1 + ',' + sw2_portnum_to_sw3 + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 100 + i, 'ports': Braket('[' + sw2_portnum_to_sw1+ ',' + sw2_portnum_to_sw3 + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 200 + i, 'ports': Braket('[' + sw2_portnum_to_sw1+ ',' + sw2_portnum_to_sw3 + ']')}}}}})

            data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 300 + i, 'ports': Braket('[' + sw3_portnum_to_sw1+ ',' + sw3_portnum_to_sw2 + ']')}}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 400 + i, 'ports': Braket('[' + sw3_portnum_to_sw1+ ',' + sw3_portnum_to_sw2 + ']')}}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 500 + i, 'ports': Braket('[' + sw3_portnum_to_sw1+ ',' + sw3_portnum_to_sw2 + ']')}}}}})
        elif list_load[i]['switch'] == 'Edge2' and list_load[i]['status'] == 'Production':
            data['dps']['Edge2']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
                list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 2}
            data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 600 + i, 'ports': Braket('[' + sw1_portnum_to_sw2+ ',' + sw1_portnum_to_sw3 + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 700 + i, 'ports': Braket('[' + sw1_portnum_to_sw2+ ',' + sw1_portnum_to_sw3 + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 800 + i, 'ports': Braket('[' + sw1_portnum_to_sw2+ ',' + sw1_portnum_to_sw3 + ']')}}}}})

            data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})

            data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 900 + i, 'ports': Braket('[' + sw3_portnum_to_sw2+ ',' + sw3_portnum_to_sw1 + ']')}}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1000 + i, 'ports': Braket('[' + sw3_portnum_to_sw2+ ',' + sw3_portnum_to_sw1 + ']')}}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1100 + i, 'ports': Braket('[' + sw3_portnum_to_sw2+ ',' + sw3_portnum_to_sw1 + ']')}}}}})
        elif list_load[i]['switch'] == 'Edge3' and list_load[i]['status'] == 'Production':
            data['dps']['Edge3']['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']), 'description': qs(
                list_load[i]['hostname']), 'native_vlan': 100, 'acl_in': 3}
            data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 1200 + i, 'ports': Braket('[' + sw1_portnum_to_sw3+ ',' + sw1_portnum_to_sw2 + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1300 + i, 'ports': Braket('[' + sw1_portnum_to_sw3+ ',' + sw1_portnum_to_sw2 + ']')}}}}})
            data['acls'][1].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1400 + i, 'ports': Braket('[' + sw1_portnum_to_sw3+ ',' + sw1_portnum_to_sw2 + ']')}}}}})

            data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'failover': {'group_id': 1500 + i, 'ports': Braket('[' + sw2_portnum_to_sw3+ ',' + sw2_portnum_to_sw1 + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'failover': {'group_id': 1600 + i, 'ports': Braket('[' + sw2_portnum_to_sw3+ ',' + sw2_portnum_to_sw1 + ']')}}}}})
            data['acls'][2].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'failover': {'group_id': 1700 + i, 'ports': Braket('[' + sw2_portnum_to_sw3+ ',' + sw2_portnum_to_sw1 + ']')}}}}})

            data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                                   'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                list_load[i]['addr_ipv6']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
            data['acls'][3].append({'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                list_load[i]['addr_ipv4']), 'actions': {'output': {'port': int(list_load[i]['port'])}}}})
    data['acls'][1].pop(0)
    data['acls'][2].pop(0)
    data['acls'][3].pop(0)
    data['acls'][1].append({'rule': {'actions': {'allow': 0}}})
    data['acls'][2].append({'rule': {'actions': {'allow': 0}}})
    data['acls'][3].append({'rule': {'actions': {'allow': 0}}})
    return(data)


def gen_faucet_yaml(data, yaml_file_name = 'faucet.yaml'):
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.indent = 40
    yaml.preserve_quotes = True
    yaml.boolean_representation = ['False', 'True']
    yaml.default_flow_style = False
    out = Path(yaml_file_name)
    list_yaml = {}
    yaml.dump(data, out)

def check_config(faucet_config_to_check):
    '''  todo : work on a better vesion '''
    try:
        call(["check_faucet_config", faucet_config_to_check])
        print('The Faucet config check passed')
    except:
        print('Something went wrong and the Faucet check failed')



doc = """Umbrella FAUCET config generator

Usage:
  umbrella.py topo <topo_name> <csv_file_name> <faucet_config_file_name>
  umbrella.py --check_output_config | -c <faucet_config_to_check>
  umbrella.py -h | --help | --version
"""

if __name__ == '__main__':
    arguments = docopt(doc, version='0.1.1rc')
    if arguments['topo'] == True:
        out_data = []
        input_data =load_csv(arguments['<csv_file_name>'])
        if arguments['<topo_name>'] == 'one_switch':
            out_data = one_switch(input_data)
        elif arguments['<topo_name>'] == 'one_legacy':
            out_data = one_legacy(input_data)
        elif arguments['<topo_name>'] == 'two_legacy':
            out_data = two_legacy(input_data)
        elif arguments['<topo_name>'] == 'triangle':
            out_data = triangle(input_data)

        if len(out_data) != 0 :
            gen_faucet_yaml(out_data, arguments['<faucet_config_file_name>'])
            print('FAUCET Config generated')
    if (arguments['--check_output_config'] == True or arguments['-c'] == True):
        check_config(arguments['<faucet_config_to_check>'])


        
