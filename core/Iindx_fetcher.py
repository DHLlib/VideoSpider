#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Iindx_fetcher.py
# @time: 2025/8/12 14:29
# DO EVERYTHING WHET YOU WANT
import requests

from config.setting import YML_CONFIG, USER_AGENT

_yml_config = YML_CONFIG.get('ffzy')


# 获取首页信息
class IndexFetcher:
    def __init__(self):
        self._headers = {
            'user-agent': USER_AGENT
        }
        self._base_url = _yml_config.get('base_url')
        self._index_keyword = _yml_config.get('list')
        self._page = _yml_config.get('page')
        self._page_size = _yml_config.get('page_size')
        self._index_result_list = []

        # 执行方法
        self._get_index_list()

    def _build_search_url(self, page=1, page_size=50):
        return (f"{self._base_url}"
                f"{self._index_keyword}&"
                f"{self._page}{page}&"
                f"{self._page_size}{page_size}")

    def _get_index_list(self, in_page=1, in_page_size=50):
        index_url = self._build_search_url(page=in_page, page_size=in_page_size)
        result = requests.get(index_url, headers=self._headers)
        if result.status_code == 200:
            index_json = result.json()
            self._handle_search_result(index_json)
        else:
            print(f"获取首页信息失败")

    # 处理查询结果
    def _handle_search_result(self, search_result):
        for i in search_result['list']:
            self._index_result_list.append(i)  # 列表追加

    # 获取查询结果
    def get_index_result_list(self):
        return self._index_result_list


if __name__ == '__main__':
    index_fetcher = IndexFetcher()
    list_1 = index_fetcher.get_index_result_list()
    print(len(list_1))
