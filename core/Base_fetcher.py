#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Base_fetcher.py
# @time: 2025/8/14 14:30
# DO EVERYTHING WHET YOU WANT

import requests

from core.APIBuilder import APIBuilder

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
    def _request(self, url, params=None):
        response = requests.get(url, params=params, headers=self._headers)
        return response.json()


if __name__ == '__main__':
    base = BaseFetcher()
    print(base)
