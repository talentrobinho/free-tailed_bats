#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-15 20:00:00
# @Author  : victor


class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		


class ElementServer(object):
	"""docstring for ElementServer"""
	def __init__(self, server_name,
					   server_work_path,
					   server_start_user,
					   server_log_collection,
					   server_data_flow):

		self.server_name = server_name
		self.server_work_path = server_work_path
		self.server_start_user = server_start_user
		self.server_log_collection = server_log_collection
		self.server_data_flow = server_data_flow


class ElementRunEnv(object):
	"""docstring for ElementRunEnv"""
	def __init__(self, run_env_monitor_path,
					   run_env_hadoop_path,
					   run_env_system_version,
					   run_env_cron_task):

		self.run_env_monitor_path = run_env_monitor_path
		self.run_env_hadoop_path = run_env_hadoop_path
		self.run_env_system_version = run_env_system_version
		self.run_env_cron_task = run_env_cron_task


class ElementResourcesEnv(object):
	"""docstring for ElementResourcesEnv"""
	def __init__(self, resources_env_cpu,
					   resources_env_mem,
					   resources_env_disk,
					   resources_env_net):

		self.resources_env_cpu = resources_env_cpu
		self.resources_env_mem = resources_env_mem
		self.resources_env_disk = resources_env_disk
		self.resources_env_net = resources_env_net


class ElementBussinessItem(object):
	"""docstring for ElementBussinessItem"""
	def __init__(self, business_item_script_name,
		               business_item_script_language,
		               business_item_script_path):

		self.business_item_script_name = business_item_script_name
		self.business_item_script_language = business_item_script_language
		self.business_item_script_path = business_item_script_path


class ElementServerChain(object):
	"""docstring for ElementServerChain"""
	def __init__(self, server_chain_upstream_service,
		               server_chain_downstream_service):

		self.server_chain_upstream_service = server_chain_upstream_service
		self.server_chain_downstream_service = server_chain_downstream_service


class ElementPersonnelInformation(object):
	"""docstring for ElementPersonnelInformation"""
	def __init__(self, personnel_information_name,
					   personnel_information_group,
					   personnel_information_phone,
					   personnel_information_email):

		self.personnel_information_name = personnel_information_name
		self.personnel_information_group = personnel_information_group
		self.personnel_information_phone = personnel_information_phone
		self.personnel_information_email = personnel_information_email


class ElementMachinePackage(object):
	"""docstring for ElementMachinePackage"""
	def __init__(self, machine_package_name,
		               machine_package_cpu,
		               machine_package_mem,
		               machine_package_disk,
		               machine_package_net):

		self.machine_package_name = machine_package_name
		self.machine_package_cpu = machine_package_cpu
		self.machine_package_mem = machine_package_mem
		self.machine_package_disk = machine_package_disk
		self.machine_package_net = machine_package_net


class ElementLogCollect(object):
	"""docstring for ElementLogCollect"""
	def __init__(self, log_collection_topic,
		               log_collection_name,
		               log_collection_local_path,
		               log_collection_hadoop_path,
		               log_collection_save):
	
		self.log_collection_topic = log_collection_topic
		self.log_collection_name = log_collection_name
		self.log_collection_local_path = log_collection_local_path
		self.log_collection_hadoop_path = log_collection_hadoop_path
		self.log_collection_save = log_collection_save


class BaseService(object):

	def __init__(self, service_info,
					   service_run_env,
					   service_resouce_env,
					   service_machine_package,
					   service_business_items_list,
					   service_server_chain,
					   service_personnel_info,
					   service_log_collection):

		if isinstance(service_business_items_list, list):
			for item in service_business_items_list:
				if isinstance(item, ElementBussinessItem):
		else:


		self.service_info = service_info
		self.service_run_env = service_run_env
		self.service_resouce_env = service_resouce_env
		self.service_machine_package = service_machine_package
		self.service_business_items_list = service_business_items_list
		self.service_server_chain = service_server_chain
		self.service_personnel_info = service_personnel_info
		self.service_log_collection = service_log_collection
		
		
		

		
		
