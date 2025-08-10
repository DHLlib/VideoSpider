#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: config_loader.py
# @time: 2025/8/9 23:10
# @version:

"""
配置文件加载器
"""

import os


class ConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_exists = self.file_exists()

    # 检查文件是否存在
    def file_exists(self):
        if os.path.exists(self.file_path):
            return True
        return False
