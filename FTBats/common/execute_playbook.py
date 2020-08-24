#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-21 12:00:00
# @Author  : victor

import os
import sys
from ftbats_logger import FtbatsLogger
from my_ansible2 import MyAnsible2
from multiprocessing import Process
from common.setting import SettingEnv
import subprocess

fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')


class ExecutePlaybook(object):
	"""docstring for SynchronousData"""
	def __init__(self, action_info):
		self.action_info = action_info


	def _execute_playbook(self, src_ip=None, dst_ip=None, playbook=None, extra_vars=None):
		SettingEnv.setting_env()
		ma = MyAnsible2(
			connection='smart', 
			inventory='{},'.format(dst_ip),
			#extra_vars=[{"src_ip":"{}".format(src_ip)}]
			extra_vars=[extra_vars])
		ma.my_playbook(playbooks=[playbook])


	def start(self):
		print self.action_info
		ip_map_list = self.action_info.pop('ip_map_list')
		for ip_map in ip_map_list:
			self.action_info.update(ip_map)
			ftb_logger.info(self.action_info)
			#p = Process(target=self._execute_playbook, kwargs=("{}".format(ip_map['src_ip']), "{},".format(ip_map['dst_ip']),["conf/{}".format(service_playbook)]))
			p = Process(
				target=self._execute_playbook, 
				kwargs=self.action_info)
			p.start()
			#p.join()
			#ma.get_result()
		return 0




def main():
	sd = ExecutePlaybook('test')
	sd.execute_playbook()



if __name__ == '__main__':
	main()