#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-15 12:00:00
# @Author  : victor

from ftbats_logger import FtbatsLogger
from fetch_path import FetchPath
import os
'''
# 设置环境变量
os.environ['WORKON_HOME']="value"
# 获取环境变量方法1
os.environ.get('WORKON_HOME')
#获取环境变量方法2(推荐使用这个方法)
os.getenv('path')
# 删除环境变量
del os.environ['WORKON_HOME']
'''

#ANSIBLE_PLAYBOOK_DIR
#ANSIBLE_ROLES_DIR

class SettingEnv(object):
    """docstring for InitEnv"""
    @classmethod
    def setting_env(cls):
        roles_path = FetchPath.fetch_path('roles')
        playbook_path = FetchPath.fetch_path('playbook')
        os.environ['ANSIBLE_ROLES_DIR'] = roles_path
        os.environ['ANSIBLE_PLAYBOOK_DIR'] = playbook_path
        