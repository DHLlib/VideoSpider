#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: setting.py
# @time: 2025/8/11 21:17
# @version:
import os

from config import user_agent
from config.config_loader import ConfigLoader

_file_path = os.path.join(os.path.dirname(os.getcwd()), 'config', 'video_source.yaml')
YML_CONFIG = dict(ConfigLoader(_file_path).read_yaml_file())  # 读取资源网地址
USER_AGENT = user_agent.USER_AGENTS[0]
USER_AGENTS = user_agent.USER_AGENTS
