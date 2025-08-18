#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: setting.py
# @time: 2025/8/11 21:17
# @version:
import os.path
import time

from config import user_agent
from config.config_loader import ConfigLoader

config_dir = os.path.dirname(os.path.abspath(__file__))
USER_AGENTS = user_agent.USER_AGENTS
SYS_CONFIG = dict(ConfigLoader(os.path.join(config_dir, './sys_config.yaml')).read_yaml_file())
URL_SOURCES = list(ConfigLoader(os.path.join(config_dir, './url_source.yaml')).read_yaml_file())
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------日志配置---------
DEBUG_ = SYS_CONFIG.get('debug')
LOG_LEVEL = SYS_CONFIG.get('log_level')
LOG_FILE = os.path.join(project_root,SYS_CONFIG['log_file'])

# ---------网络配置---------
MAX_THREADS = int(SYS_CONFIG.get('max_threads'))
MAX_RETRIES = int(SYS_CONFIG.get('max_retries'))
TIMEOUT = int(SYS_CONFIG.get('timeout'))

# ---------文件路径配置---------
def check_directory():
    # 检查配置值
    if SYS_CONFIG.get('output_dir',None) is not None:
        output_dir = os.path.join(project_root,SYS_CONFIG['output_dir'])
    else:
        output_dir = os.path.join(project_root, 'output')
    if SYS_CONFIG.get('cache_dir',None) is not None:
        cache_dir = os.path.join(project_root,SYS_CONFIG['cache_dir'])
    else:
        cache_dir = os.path.join(project_root, 'cache')

    os.makedirs(output_dir, exist_ok=True) # 创建输出目录
    time.sleep(1)
    os.makedirs(cache_dir, exist_ok=True) # 创建缓存目录

    return output_dir, cache_dir

OUTPUT_DIR, CACHE_DIR = check_directory()

print(f'配置初始化完成')
