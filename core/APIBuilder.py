#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: APIBuilder.py
# @time: 2025/8/14 16:17
# DO EVERYTHING WHET YOU WANT

"""API构建器"""
import os.path
import random

from config.setting import URL_SOURCES, USER_AGENTS
from utils.Log_Manager import log_manager, logger

_PARAMS = {
    "search": {
        "ac": "search",
        "wd": "keyword"
    },
    "detail": {
        "ac": "detail",
        "ids": "vod_ids"
    },
    "index": {
        "ac": "list",
        "t": None
    },
    "default": {
        "pg": 1,
        "pagesize": 50
    }
}


# 构建API信息
class APIBuilder:
    """构建API信息，根据类型，返回url，headers，params"""

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'url_source.yaml')
        self._PARAMS = _PARAMS
        self.URL_SOURCES = URL_SOURCES
        self._params = None
        self._headers = None
        self._sources_url = None
        self._is_search = 0
        self._name = None

    # 读取配置信息,获取基础url 和 是否支持搜索
    @log_manager.log_method
    def _read_config(self, source_keyname):
        """读取配置信息"""
        config = self.URL_SOURCES[0]
        logger.info(f'视频源：{config}')
        # 匹配资源站
        if config.get('key') == source_keyname:
            self._sources_url = config.get('base_url')
            self._is_search = config.get('is_search')
            self._name = config.get('name')

    # 构建参数
    @log_manager.log_method
    def _build_params(self, api_type):
        """构建API信息"""
        default_params = self._PARAMS.get('default').copy()  # 默认参数
        if api_type is None:  # 如果类型为空，则使用默认参数
            self._params = default_params
        else:
            taget_params = self._PARAMS.get(api_type).copy()  # 目标参数
            self._params = {**default_params, **taget_params}  # 解包并合并

    def _build_headers(self):
        """构建headers信息"""
        self._headers = {
            # 获取随机一个user-agent
            'user-agent': random.choice(USER_AGENTS)
        }

    # 开始构建
    def begin_builder(self, source_keyname='ffzy', api_type='index'):
        """
        :param source_keyname: 资源key,如：ffzy
        :param api_type: api类型，如：search，detail,index
        """
        self._read_config(source_keyname)
        if self._is_search == 0 and api_type == 'search':  # 不支持搜索
            print(f"该资源站不支持搜索功能")
            self._build_params(None)
            self._build_headers()
        else:
            self._build_params(api_type)
            self._build_headers()
    @log_manager.log_method
    def get_api_info(self):
        """返回API信息"""
        return self._sources_url, self._headers, self._params, self._name


if __name__ == '__main__':
    api = APIBuilder()
    api.begin_builder('ffzy', 'search')
    url, headers, params, name = api.get_api_info()
    print(url)
    print(headers)
    print(params)
    print(name)
