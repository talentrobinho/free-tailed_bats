#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-13 18:00:00
# @Author  : victor

import os
import sys
from ftbats_logger import FtbatsLogger
from my_ansible2 import MyAnsible2
from multiprocessing import Process
import subprocess

fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')




class IpToList(object):
    """docstring for IpMap"""
    def __init__(self):
        self.ip_list = []

    def file_to_list(self, ip_file):
        
        with open(ip_file) as f:
            for ip in f.readlines():
                ip_info = ip.strip('\n').split()
                if len(ip_info) == 0:
                    ftb_logger.info("The ip file[{}] is null.".format(ip_file))
                    break
                self.ip_list.append({
                    'src_ip':ip_info[1], 
                    'dst_ip':ip_info[0]})

        return self.ip_list



class AnalyzerArgs(object):
    """docstring for SynchronousData"""
    def __init__(self, args_info):
        self.args_info = args_info
        self.args_list = {}

    #src_ip=None, dst_ip=None, playbooks=None, extra_vars=None
    def analyzer_args(self):
        print '33333333333333'
        for e in os.environ.keys():
            print e+": "+os.environ.get(e)
        ip_to_list = IpToList()
        self.args_list['ip_map_list'] = [ x for x in ip_to_list.file_to_list(self.args_info['ipmapfile']) if x != '' ]
        self.args_list['playbook'] = "{}/{}_{}".format(os.environ.get('ANSIBLE_PLAYBOOK_DIR'), self.args_info['service_name'], "playbook.yaml")      
        #self.args_list['playbook'] = "{}_{}".format(self.args_info['service_name'], "playbook.yaml")      
        self.args_list['extra_vars'] = {'items':["{}.sh".format(y) for y in self.args_info['items']]}
        self.args_list['action'] = self.args_info['action']
        #if self.args_info['report']:
        #   self.args_list['report'] = [ "{}_{}".format(self.args_info['service_name'], y) for y in self.args_info['items'].split(',') if y != '' ]
        return self.args_list
