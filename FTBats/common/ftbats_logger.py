#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-18 15:00:00
# @Author  : victor

import os
import yaml
import logging
import logging.config
from fetch_path import FetchPath



class FtbatsLogger(object):
	"""docstring for FtbatsLogger"""
	def __init__(self, dir='conf'):
		self.config_path = FetchPath.fetch_path(dir)
		self.file_abspath = None


	def load_log_conf(self, logger_name):
		self.file_abspath = "{}/{}".format(self.config_path, 'log.yaml')
		with open(self.file_abspath) as f:
			self.config_info = yaml.load(f)
		logging.config.dictConfig(self.config_info)
		ftb_logger = logging.getLogger(logger_name)	
		return ftb_logger



def main():
	pass

if __name__ == '__main__':
	main()