#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-06-24 11:30:00
# @Author  : victor
 
import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
from fetch_path import FetchPath
from ftbats_logger import FtbatsLogger
import os
import yaml
from ftbats_logger import FtbatsLogger


fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')



class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in
 
    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    #def runner_on_ok(self, host, result):
    #    pass
    #def v2_runner_on_ok(self, result, **kwargs):
    def v2_runner_on_ok(self, result):
        """Print a json representation of the result
 
        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        task = result._task
        rc = result._result['rc'] if 'rc' in result._result.keys() else None
        rfile = result._result['results_file'] if 'results_file' in result._result.keys() else None
        stdout_list = result._result['stdout_lines'] if 'stdout_lines' in result._result.keys() else None
        #print result.needs_debugger()
        #print result.task_name()
        #print result.is_unreachable()
        #print result.is_skipped()
        #print result.is_changed()  
        #print result.is_failed()
        #print result.clean_copy()
        #print result._task
        #print result._task_fields
        #print({host.name: result.is_failed}, indent=4)
        print(json.dumps({"{}|{}".format(host.name,task.name): result._result}, indent=4))
        #stdout_info = "\n".join(stdout_list) if isinstance(stdout_list,list) else stdout_list
        #print("{}|{}|{}|{}|{}".format(host.name,task.name,rc,rfile,stdout_info))
        #self.runner_on_ok(host, result._result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        task = result._task
        print(json.dumps({"{}|{}".format(host.name,task.name): result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        host = result._host
        task = result._task
        print(json.dumps({"{}|{}".format(host.name,task.name): result._result}, indent=4))
    
    def v2_runner_on_skipped(self, result, ignore_errors=False):
        #host = result._host
        #task = result._task
        #print(json.dumps({"{}|{}".format(host.name,task.name): result._result['stdout_lines']}, indent=4))
        pass

    def v2_runner_on_async_poll(self, result):
        host = result._host.get_name()
        task = result._task.get_name()
        jid = result._result.get('ansible_job_id')
        # FIXME, get real clock
        clock = 0
        #self.runner_on_async_poll(host, result._result, jid, clock)
        #print(json.dums({"{}|{}|{}".format(host.name, task.name, jid):result._result}))
        print(json.dums({"{}|{}|{}".format(host, task, jid):result._result}))

    def v2_runner_on_async_ok(self, result):
        host = result._host.get_name()
        task = result._task.get_name()
        jid = result._result.get('ansible_job_id')
        #self.runner_on_async_ok(host, result._result, jid)
        print(json.dums({"{}|{}|{}".format(host, task, jid):result._result}))

    def v2_runner_on_async_failed(self, result):
        host = result._host.get_name()
        task = result._task.get_name()
        jid = result._result.get('ansible_job_id')
        #self.runner_on_async_ok(host, result._result, jid)
        #print(json.dums({"{}|{}|{}".format(host.name, task.name, jid):result._result}))
        print(json.dums({"{}|{}|{}".format(host, task, jid):result._result}))



class MyAnsible2(object):
    """docstring for MyAnsible2"""
    def __init__(self, 
        connection="local",
        remote_user=None,
        remote_password=None,
        private_key_file=None,
        sudo=None,
        sudo_user=None,
        ask_sudo_pass=None,
        module_path=None,
        became=None,
        became_method=None,
        became_user=None,
        check=False,
        diff=False,
        listhosts=None,
        listtasks=None,
        listtags=None,
        verbosity=None,
        syntax=None,
        start_at_task=None,
        inventory=None,
        extra_vars=None,
        forks=None):
        #ftb_logger.info(extra_vars)
        '''
        初始化函数，定义的默认的选项值，
        在初始化的时候可以传参，以便覆盖默认选项值
        '''
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            private_key_file=private_key_file,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            became=became,
            became_method=became_method,
            became_user=became_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
            extra_vars=extra_vars,
            forks=forks,
        )

        '''
        三元表达式，假如没有传递 inventory，就使用 "localhost,"
        指定 inventory 文件
        也可以是一个包含主机的元组，这个仅仅适用于测试
        比如： 1.1.1.1,   #如果只有一个 IP ，最后必须有英文的逗号
        或者： 1.1.1.1, 2.2.2.2
        '''

        self.inventory = inventory if inventory else "localhost,"

        #实例化数据解析器
        self.loader = DataLoader()

        #实例化资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)

        #设置密码
        self.passwords = remote_password

        #实例化回调插件对象
        self.result_callback = ResultCallback()
        #self.result_callback = None

        #变量管理器
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inv_obj)

        #ftb_logger.info("inventory: {}".format(self.inventory))
        #print dir(self.inv_obj)
    def test(self):
        print self.variable_manager.get_vars() 
        print self.variable_manager.extra_vars


    def run(self, hosts="localhost", gather_facts="no", module="ping", args="", task_time=0):
        '''
        参数说明：
        task_time -- 执行异步任务时等待的秒数，这个需要大于0，等于0的时候不支持异步（默认值），这个值应该等于执行任务实际消耗时间为好
        '''
        #print ("xxx{} {}".format(self.inventory,hosts))
        #ftb_logger.info("{}:{}:{}".format(hosts,module,args))
        #self.inv_obj = InventoryManager(loader=self.loader, sources="{},".format(hosts))
        play_source = dict(
            name = "Ad-hoc",
            hosts = hosts,
            gather_facts = gather_facts,
            #remote_user = 'root',
            tasks = [
            # 这里每个 task 就是这个列表中的一个元素，格式是嵌套的字典
            {"action":{"module": module, "args": args}, "async": task_time, "poll": 0}
            ])
        
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.result_callback)

            result = tqm.run(play)
        finally:
            if tqm is None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



    def my_playbook(self, playbooks):
        '''
        Keyword argument:
        playbooks --- 需要一个列表类型
        '''

        from ansible.executor.playbook_executor import PlaybookExecutor

        #self.variable_manager.extra_vars = extra_vars
        
        playbook = PlaybookExecutor(
            playbooks=playbooks,
            inventory=self.inv_obj,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords)

        playbook._tqm._stdout_callback = self.result_callback

        result = playbook.run()


        
