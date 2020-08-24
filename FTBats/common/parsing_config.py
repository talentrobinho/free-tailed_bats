#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-18 15:00:00
# @Author  : victor

import os
import sys
import yaml
from fetch_path import FetchPath
from ftbats_logger import FtbatsLogger
#import logging
#import logging.config

fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')


class ParsingConfig(object):
	"""docstring for parsing_conf"""
	def __init__(self, dir='conf'):
		self.config_path = FetchPath.fetch_path(dir)
		self.file_list = None
		self.yml_list = None
		self.config_info_list = []


	
	def _filter_yml_file(self):
		self.file_list = os.listdir(self.config_path)
		#print self.file_list
		for yml_file in self.file_list:
			if not yml_file.endswith('.yaml') or yml_file in ['log.yaml']:
				self.file_list.remove(yml_file)
		#print self.file_list
		if len(self.file_list) == 0:
			ftb_logger.warning('Not found service yaml file.')
			sys.exit(1)
		return self.file_list


	def _read_conf(self):
		self.yml_list = self._filter_yml_file()
		for file in self.yml_list:
			file_abspath = "{}/{}".format(self.config_path, file)
			with open(file_abspath) as f:
				self.config_info_list.append(yaml.load(f))

		return self.config_info_list

	def parsing_conf(self):
		ftb_logger.debug('parsing config!!')
		return self._read_conf()



def main():
	pc = ParsingConfig()
	print pc.parsing_conf()


if __name__ == '__main__':
	main()