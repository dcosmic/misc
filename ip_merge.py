#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Merge IPNetworks
'''

import sys
import os
import csv
import ipaddress


def get_nets(src_file_path):
    ip_net = []
    with open(src_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for eachline in reader:
            entry = eachline[0]
            if '-' in entry:
                ip_pair = entry.strip().split('-')
                ip_begin = ipaddress.ip_address(ip_pair[0].strip())
                ip_end = ipaddress.ip_address(ip_pair[1].strip())
                temp_net = [
                    ipaddr for ipaddr in ipaddress.summarize_address_range(
                        ip_begin, ip_end)]
            elif '/' in entry:
                temp_net = [ipaddress.ip_network(entry.strip(), strict=False)]
            else:
                temp_net = [ipaddress.ip_address(entry.strip())]
            ip_net = ip_net + temp_net
        print(ip_net)
        return(ip_net)


def merge_ip_nets(ip_net):
    ip_counter = 0
    net_break_counter = 0
    nets = [
        ipaddr for ipaddr in ipaddress.collapse_addresses(ip_net)]
    merged_nets = []
    for n in nets:
        ip_counter += n.num_addresses
        start_ip = n[0]
        end_ip = n[-1]
        if net_break_counter == 0:
            net_start = start_ip
            net_end = end_ip
        # check if the temp ip net can be continue
        if net_break_counter > 0:
            if start_ip == net_end + 1:
                net_end = end_ip
            else:
                # net breaks
                net_break_counter = 0
                merged_nets.append(
                    [net_start.compressed + '-' + net_end.compressed])
                print(merged_nets)
                # reset net_start & net_end
                net_start = start_ip
                net_end = end_ip
        net_break_counter += 1
    merged_nets.append([net_start.compressed + '-' + net_end.compressed])
    print(merged_nets)
    return(ip_counter, merged_nets)


def write_summ_nets(net_list, dst_file_path, config):
    with open(dst_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # transform OUTPUT
        if 'T' in config:
            write_list = []
            for i in net_list:
                item = i[0]
                if 'c' in config:
                    ip_pair = item.split('-')
                    if ip_pair[0] == ip_pair[1]:
                        write_list.append(ip_pair[0])
                    else:
                        write_list.append(item)
                else:
                    write_list.append(item)
            writer.writerow(write_list)
        else:
            for i in net_list:
                item = i[0]
                if 'c' in config:
                    ip_pair = item.split('-')
                    if ip_pair[0] == ip_pair[1]:
                        item_to_write = [ip_pair[0]]
                    else:
                        item_to_write = [item]
                else:
                    item_to_write = [item]
                writer.writerow(item_to_write)
        print('OUTPUT CONFIG:', config)


def show_help():
    print('usage: ipmerge.py D:\\xxx [-config]')
    print('-h    show help')
    print('-c    compact mode: single ip without "-"')
    print('-T    transform OUTPUT: 1*n')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        show_help()
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        show_help()
    else:
        working_dir = sys.argv[1]
        if len(sys.argv) == 2:
            config = ''
        else:
            config = sys.argv[2]

        src_file_path = working_dir + '\\to_merge.csv'
        dst_file_path = working_dir + '\\merged.csv'
        if os.path.exists(working_dir):
            ip_net = get_nets(src_file_path)
            (ip_count, net_list) = merge_ip_nets(ip_net)
            write_summ_nets(net_list, dst_file_path, config)
            print('Total: ', ip_count, 'hosts!')
