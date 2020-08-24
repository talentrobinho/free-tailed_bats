#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-18 15:00:00
# @Author  : victor

import os
import yaml



class FetchPath(object):
	"""docstring for FetchPath"""
	@classmethod
	def _fetch_father_path(cls):
		current_path = os.path.dirname(os.path.abspath('__file__'))
		current_path_list = current_path.split("/")
		return "/".join(current_path_list[:current_path_list.index("FTBats")+1])



	@classmethod
	def fetch_path(cls, dir):
		return "{}/{}".format(cls._fetch_father_path(), dir)




def main():
	pass

if __name__ == '__main__':
	main()