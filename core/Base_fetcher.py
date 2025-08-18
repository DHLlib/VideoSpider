#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Base_fetcher.py
# @time: 2025/8/14 14:30
# DO EVERYTHING WHET YOU WANT

import requests

from core.APIBuilder import APIBuilder
from utils.Log_Manager import log_manager, logger

"""基础获取器"""


class BaseFetcher:
    def __init__(self, type_='index', resource_name='ffzy'):
        """初始化配置"""
        api_builder = APIBuilder()  # 创建APIBuilder对象
        api_builder.begin_builder(resource_name, type_)  # 获取api信息

        self._sources_url, self._headers, self._params, self._name = api_builder.get_api_info()

    def __str__(self):
        return f"当前站点：{self._name}"

    # 请求
    @log_manager.log_method
    def _request(self,params=None):
        """请求数据"""
        try:
            request_params = params if params is not None else self._params
            response = requests.get(url=self._sources_url, params=request_params, headers=self._headers)
            result = response.json()
            if response.status_code == 200:
                return result
            return None
        except Exception as e:
            logger.error(f"请求错误：{e}")
            return None

    # 解析返回
    def _response_handler(self, result):
        """解析返回数据"""
        pass

if __name__ == '__main__':
    base = BaseFetcher()
    print(base)
