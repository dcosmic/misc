#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Merge IPNetworks
Rev.20161213
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
    summ_net = [ipaddr for ipaddr in ipaddress.collapse_addresses(ip_net)]
    print(summ_net)
    return(summ_net)


def write_summ_nets(summ_net, dst_file_path):
    ip_counter = 0
    net_break_counter = 0
    with open(dst_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for n in summ_net:
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
                    writer.writerow(
                        [net_start.compressed + '-' + net_end.compressed])
                    print(net_start.compressed + '-' + net_end.compressed)
                    # reset net_start & net_end
                    net_start = start_ip
                    net_end = end_ip
            net_break_counter += 1
        writer.writerow([net_start.compressed + '-' + net_end.compressed])
        print(net_start.compressed + '-' + net_end.compressed)
        return(ip_counter)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('No argument!  please input working dir!')

    else:
        working_dir = sys.argv[1]

        src_file_path = working_dir + '\\to_merge.csv'
        dst_file_path = working_dir + '\\merged.csv'
        if os.path.exists(working_dir):
            ip_net = get_nets(src_file_path)
            summ_net = merge_ip_nets(ip_net)
            ip_count = write_summ_nets(summ_net, dst_file_path)
            print('Total: ', ip_count, 'hosts!')
