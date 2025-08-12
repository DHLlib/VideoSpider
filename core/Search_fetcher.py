#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Search_fetcher.py
# @time: 2025/8/12 14:04
# DO EVERYTHING WHET YOU WANT
import json

import requests

from config.setting import YML_CONFIG, USER_AGENT

_yml_config = YML_CONFIG.get('ffzy')


# 搜索视频提取器
class SearcherFetcher:
    def __init__(self, video_name, page=1, page_size=20):
        self.video_name = video_name
        self._base_url = _yml_config.get('base_url')
        self._headers = {
            'user-agent': USER_AGENT
        }
        self._search_path = _yml_config.get('search')
        self._page = _yml_config.get('page')
        self._page_size = _yml_config.get('page_size')
        self._search_url = None
        # self._search_result = None
        self._search_result_list = []
        self._search_video()

    # 魔术方法
    # 当打印SearcherFetcher对象时，会直接显示video_name的值
    def __str__(self):
        return self.video_name

    # 构建searchurl
    def _build_search_url(self, page=1, page_size=50):
        return (f"{self._base_url}"
                f"{self._search_path}"
                f"{self.video_name}&"
                f"{self._page}{page}&"
                f"{self._page_size}{page_size}")

    # 搜索视频
    def _search_video(self):
        page_ = 1
        while True:
            print(f"正在搜索第{page_}页...")
            self._search_url = self._build_search_url(page=page_)
            result = requests.get(url=self._search_url, headers=self._headers).text
            search_result = json.loads(result)
            self._handle_search_result(search_result)
            page_count = search_result.get('pagecount')
            if page_count == page_:
                break
            else:
                page_ += 1

    # 处理查询结果
    def _handle_search_result(self,search_result):
        for i in search_result['list']:
            self._search_result_list.append(i) # 列表追加

    # 获取查询结果
    def get_search_result_list(self):
        return self._search_result_list

    # 获取url
    def get_search_url(self):
        return self._search_url


if __name__ == '__main__':
    s = SearcherFetcher('海')
    result_list = s.get_search_result_list()
    url = s.get_search_url()
    print(result_list, '\n', url)
