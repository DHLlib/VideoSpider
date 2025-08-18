#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Index_fetcher.py
# @time: 2025/8/12 14:29
# DO EVERYTHING WHET YOU WANT
from core.Base_fetcher import BaseFetcher
from utils.Log_Manager import *

# 获取首页信息
class IndexFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(type_='index', resource_name='ffzy')
        self._index_result_list = []
        self._local_params = self._params.copy()
        self._get_index_list()

    # 下一页
    @log_manager.log_method
    def _choose_page(self, in_page=1, in_page_size=50):
        self._local_params['pg'] = in_page
        self._local_params['pagesize'] = in_page_size

    @log_manager.log_method
    def next_page(self):
        self._choose_page(self._local_params['pg'] + 1)
        return self._get_index_list(self._local_params)

    def _get_index_list(self, _params=None):
        if _params:
            result = super()._request(params=_params)
        else:
            result = super()._request()
        self._handle_search_result(result)

    @log_manager.log_method
    def _handle_search_result(self, search_result):
        # 清空列表结果
        self._index_result_list.clear()
        self._index_result_list = search_result['list']
        logger.info(f'获取首页信息成功，共有{self._index_result_list}条数据')


    # 获取查询结果
    @log_manager.log_method
    def get_index_result_list(self):
        return self._index_result_list


if __name__ == '__main__':
    index_fetcher = IndexFetcher()
    # list_1 = index_fetcher.get_index_result_list()
    a = index_fetcher.get_index_result_list()
    print(len(a))
    print(a)
    index_fetcher.next_page()
    b = index_fetcher.get_index_result_list()
    print(len(b))
    print(b)
