#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-10 11:00:00
# @Author  : victor

import os
import sys
from common.ftbats_logger import FtbatsLogger
from common.execute_playbook import ExecutePlaybook

fl = FtbatsLogger()
ftb_logger = fl.load_log_conf('ftbats_log')

class ServiceIndicators(ExecutePlaybook):

    def __init__(self, args):
        """docstring for ClassName"""
        super(ServiceIndicators, self).__init__(args)





