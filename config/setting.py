#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: setting.py
# @time: 2025/8/11 21:17
# @version:
import os.path

from config import user_agent
from config.config_loader import ConfigLoader

config_dir = os.path.dirname(os.path.abspath(__file__))
USER_AGENTS = user_agent.USER_AGENTS
SYS_CONFIG = dict(ConfigLoader(os.path.join(config_dir, './sys_config.yaml')).read_yaml_file())
URL_SOURCES = list(ConfigLoader(os.path.join(config_dir, './url_source.yaml')).read_yaml_file())

print(f'配置初始化完成')
