#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: setting.py
# @time: 2025/8/11 21:17
# @version:
from config import user_agent
from config.config_loader import ConfigLoader

YML_CONFIG = dict(ConfigLoader('../config/video_source.yml').read_yaml_file())  # 读取资源网地址
USER_AGENT = user_agent.USER_AGENTS[0]
