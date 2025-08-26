#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: AggregatedSearchFetcher.py
# @time: 2025/8/25 21:33
# @version:


"""聚合搜索获取器"""
from core.Search_fetcher import SearcherFetcher


class AggregatedSearchFetcher:
    def __init__(self, video_name, resource_names):
        self.all_result = {}
        self.video_name = video_name
        self.resource_names = resource_names
        # super().__init__(video_name=self.video_name,resource_name=resource_names)

    def _search_single_source(self, resource_name):
        """从单个资源站搜索"""
        try:
            searcher = SearcherFetcher(self.video_name, resource_name)
            result = searcher.get_search_result_list()
            return result.search_list, resource_name
        except Exception as e:
            return [], resource_name

    def searcher_all_source(self):
        """从所有支持的资源站中搜索"""
        """使用多线程的方式"""
        pass
