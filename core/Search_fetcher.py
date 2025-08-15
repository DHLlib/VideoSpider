#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Search_fetcher.py
# @time: 2025/8/12 14:04
# DO EVERYTHING WHET YOU WANT

from core.Base_fetcher import BaseFetcher
from models.DTOs import SearchEpisodeDTO, VideoSearchDTO


# 搜索视频提取器
class SearcherFetcher(BaseFetcher):
    def __init__(self, video_name, page=1, page_size=20):
        fetcher_type = 'search'
        super().__init__(type_=fetcher_type, resource_name='ffzy')
        self._local_params = self._params.copy()
        self.video_name = video_name
        self._search_result_list = []
        self._get_search_all_result()

    # 魔术方法
    # 当打印SearcherFetcher对象时，会直接显示video_name的值
    def __str__(self):
        return self.video_name

    # 搜索视频
    def _get_search_all_result(self):
        self._local_params['wd'] = self.video_name
        page_ = 1
        while True:
            self._local_params['pg'] = page_
            print(f"正在搜索第{page_}页...")
            search_all_result = super()._request(params=self._local_params)
            print(search_all_result)
            self._handle_search_result(search_all_result)
            page_count = search_all_result.get('pagecount')
            if page_count <= page_:
                break
            else:
                page_ += 1

    # 处理查询结果
    def _handle_search_result(self, search_result):
        for search_index in search_result['list']:
            search_data = SearchEpisodeDTO(
                name=search_index.get('vod_name'),
                vod_id=search_index.get('vod_id')
            )
            self._search_result_list.append(search_data)  # 列表追加
        print(f'数据合并完成')

    # 获取查询结果
    def get_search_result_list(self):
        return VideoSearchDTO(search_list=self._search_result_list)


if __name__ == '__main__':
    s = SearcherFetcher('JOJO')
    result_list = s.get_search_result_list()
    for i in result_list.search_list:
        print(i.name)
        print(i.vod_id)
