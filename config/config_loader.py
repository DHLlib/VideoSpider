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

import yaml


class ConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_exists = self.file_exists()

    # 检查文件是否存在
    def file_exists(self):
        if os.path.exists(self.file_path):
            return True
        return False

    def read_yaml_file(self):
        """
        读取YAML文件并返回字典
        :returns: dict: 解析后的字典数据
        """
        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    return data if data is not None else {}
            except FileNotFoundError:
                print(f"文件 {self.file_path} 不存在")
                return {}
            except yaml.YAMLError as e:
                print(f"YAML格式错误: {e}")
                return {}
            except Exception as e:
                print(f"读取文件时发生错误: {e}")
                return {}
        else:
            print(f'文件不存在')
