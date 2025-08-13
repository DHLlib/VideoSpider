#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Base_control.py
# @time: 2025/8/12 17:09
# DO EVERYTHING WHET YOU WANT

# 基础控制器

from core.Detail_fetcher import DetailFetcher
from core.Search_fetcher import SearcherFetcher

def get_detail(vod_id):
    return DetailFetcher(vod_id).get_play_lists(), DetailFetcher(vod_id).get_name()


def search_video(video_name):
    search_result = SearcherFetcher(video_name).get_search_result_list()
    search_list = []
    for i, result in enumerate(search_result):
        vod_id = result.get('vod_id')
        vod_name = result.get('vod_name')
        search_list.append([vod_name, vod_id])
    return search_list


def format_output_console(result_list):
    """格式化搜索结果为字符串"""
    result_str = "=" * 50 + "\n"
    result_str += "搜索结果:\n"
    result_str += "=" * 50 + "\n"
    for item, value in enumerate(result_list):
        result_str += f"  [{item}] | {value[0]} |  {value[1]}\n"
        result_str += "-" * 30 + "\n"
    result_str += f"共找到 {len(result_list)} 个结果\n"
    return result_str


if __name__ == '__main__':
    name = input("请输入视频名称: ")
    _result = search_video(name)
    format_result = format_output_console(_result)
    print(format_result)
    choose_one = int(input("请选择一个序号: "))

    video_id = _result[choose_one][1]

    # 查询详情
    detail,result_name = get_detail(video_id)
    print("=" * 50 + "\n")
    print(f'电影名称：{result_name}')
    print(f'详情页：{detail}')
