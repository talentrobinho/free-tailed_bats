#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-19 17:00:00
# @Author  : victor

import os
import sys
import argparse
import requests
from common.ftbats_logger import FtbatsLogger
from common.parsing_config import ParsingConfig
from common.execute_playbook import ExecutePlaybook
from migrate.migrate_service import MigrateService
from expansion.expansion_service import ExpansionService
from report.service_indicators import ServiceIndicators
from common.analyzer_args import AnalyzerArgs
from common.setting import SettingEnv



fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')


class CliArg(object):
	"""docstring for CliArg"""
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument(
			'--service', 
			type=str,  
			required=True, 
			default=None,
			help='传入的服务标识。 如：RetrieverServer')
		self.parser.add_argument(
			'--path', 
			type=str,  
			required=True, 
			default=None,
			help='传入的服务凯撒路径，多个服务请用逗号分隔。 如：Mobile_Search/main/RS,Mobile_Search/searchkey/RS')
		self.parser.add_argument(
			'--ipmapfile', 
			type=str,  
			required=True, 
			default=None,
			help='''传入ip映射文件。 如：/tmp/rs.ip 文件格式如：
			  src_ip	dst_ip''')
		self.parser.add_argument(
			'--forks',
			type=str,
			help='传入并行执行任务的数量，默认是5个任务并行执行')
		self.parser.add_argument(
			'--items',
			type=str,
			default=None,
			help='传入业务指标名称，多个指标请用都好分隔')
		self.parser.add_argument(
			'--action',
			#action="store_true",
			choices=['migrate', 'expansion', 'report'],
			default=False,
			help='传入操作类型，migrate:迁移；expansion:扩容；report:生成校验报告')

		#互斥的参数
		#group1 = self.parser.add_mutually_exclusive_group()
		#group1.add_argument("-v", "--verbose", action="store_true")
		#group1.add_argument("-q", "--quiet", action="store_true")
		self.cli_args = None
		self.service_config = {}

	def wget_ceasar(self):
		url="http://db.caesar.adtech.sogou/server/GetIpByPath.php?path=/&type=text"
		r = requests.get(url)
		if r.status_code == 200:
			service_list = [x.split("\t")[0] for x in r.text.split("\n") if x != '']
			#print service_list
			#print '='*100
			service_set = set(["/".join(s.split("/")[2:-2]) for s in service_list])
		return service_set



	def check_file(self, ipfile):
		file_status = 0
		if not os.path.exists(ipfile):
			ftb_logger.error("The file of {} is not exists.".format(ipfile))
			file_status = 1
		elif not os.path.getsize(ipfile):
			ftb_logger.error("The {}'s size is 0.".format(ipfile))
			file_status = 1
		return file_status


	def check_service(self, sr):
		sr_status = 0
		pc = ParsingConfig()
		config_list = pc.parsing_conf()
		for service in config_list:
			if not sr in service.keys()[0]:
				sr_status = 1
			else:
				self.service_config = service
				sr_status = 0
				break
		return sr_status

	def full_args(self, cli_args, service_args):
		service_args['service_name'] = cli_args.service
		service_args['path'] = cli_args.path
		service_args['ipmapfile'] = cli_args.ipmapfile
		service_args['action'] = self.cli_args.action
		if self.cli_args.action == 'report':
			service_args['items'] = [ "{}_{}".format(cli_args.path.replace("/", "_"), x) for x in cli_args.items.split(',') if x != '' ]
		else:
			service_args['items'] = None
		return service_args

	def check_arg(self):
		self.cli_args = self.parser.parse_args()
		ftb_logger.info("Check parameters.")
		#if self.check_service(self.cli_args.service):
		#	ftb_logger.error("Not found config of {}".format(sr))
		#	sys.exit(1)
		#elif self.check_file(self.cli_args.ipmapfile):
		#	sys.exit(1)

		
		if self.cli_args.action == 'report':
			if self.cli_args.items is None:
				ftb_logger.error("args report of action is used with args items")
				#self.wget_ceasar()
				sys.exit(1)
			elif self.cli_args.items.strip('').startswith(',') or len(self.cli_args.items.strip()) == 0:
				ftb_logger.error("args items is error")
				#self.wget_ceasar()
				sys.exit(1)
		elif not self.cli_args.items is None:
			ftb_logger.error("args items is used with args report")
			#self.wget_ceasar()
			sys.exit(1)
		if not u"{}".format(self.cli_args.path) in self.wget_ceasar():
			ftb_logger.error("args service is not exist in caesar")
			sys.exit(1)

		return self.full_args(self.cli_args, self.service_config)
		


class Flying(object):
	"""docstring for Flying"""
	def __init__(self, arg):
		self.arg = arg
		self.action = None
		#print "B_PB: "+"NULL" if os.environ.get('ANSIBLE_PLAYBOOK_DIR') is None else os.environ.get('ANSIBLE_PLAYBOOK_DIR')
		#print "B_RD: "+"NULL" if os.environ.get('ANSIBLE_ROLES_DIR') is None else os.environ.get('ANSIBLE_ROLES_DIR')
		SettingEnv.setting_env()
		#print 'ssssssss'
		#print "A_PB: "+os.environ.get('ANSIBLE_PLAYBOOK_DIR')
		#print "A_RD: "+os.environ.get('ANSIBLE_ROLES_DIR')
		for e in os.environ.keys():
			print e+": "+os.environ.get(e)
		
	def start(self):
		#print self.arg
		#sys.exit(1)
		#ftb_logger.info("Start syncing data.")
		#syncing_data = ExecutePlaybook(self.arg)
		#syncing_data.start()
		ftb_logger.info("All parameters are correct.")
		self.action = self.arg.pop('action')
		if self.action == 'report' :
			ftb_logger.info('report')
			si = ServiceIndicators(self.arg)
			si.start()
		elif self.action == 'migrate' :
			#mr = MigrateService(self.arg)
			#mr.start()
			ftb_logger.info('MigrateService')
		elif self.action == 'expansion' :
			#es = ExpansionService(self.arg)
			#es.start()
			ftb_logger.info('ExpansionService')
		ftb_logger.info("Data synchronization is complete.")

		
def main():
	ca = CliArg()
	aa = AnalyzerArgs(ca.check_arg())
	fly = Flying(aa.analyzer_args())
	fly.start()


if __name__ == '__main__':
	main()