#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Base_control.py
# @time: 2025/8/12 17:09
# DO EVERYTHING WHET YOU WANT.

# 基础控制器

from core.Detail_fetcher import DetailFetcher
from core.Search_fetcher import SearcherFetcher
from download.VideoDownload import VideoDownload


def get_detail(vod_id):
    return DetailFetcher(vod_id).get_play_lists()


def search_video(video_name):
    search_result = SearcherFetcher(video_name).get_search_result_list()
    search_list = search_result.search_list
    return search_list


def format_output_console(result_list):
    """格式化搜索结果为字符串"""
    result_str = "=" * 50 + "\n"
    result_str += "搜索结果:\n"
    result_str += "=" * 50 + "\n"
    for item, value in enumerate(result_list):
        result_str += f"  [{item}] | {value.name} |  {value.vod_id}\n"
        result_str += "-" * 30 + "\n"
    result_str += f"共找到 {len(result_list)} 个结果\n"
    return result_str


def download_video(url, v_name):
    VideoDownload(url, v_name).main()


if __name__ == '__main__':
    _result = None
    while True:
        print("欢迎使用视频下载工具")
        print("1. 搜索视频")
        print("2. 退出")
        choice = input("请选择: ")
        if choice == "1":
            name = input("请输入视频名称: ")
            _result = search_video(name)
        elif choice == "2":
            exit()
        else:
            print("无效的选择，请重新输入")

        format_result = format_output_console(_result)
        print(format_result)
        choose_one = int(input("请选择一个序号: "))
        if choose_one > len(_result):
            print("无效的选择，请重新输入")
            continue
        video_id = _result[choose_one].vod_id

        # 查询详情
        detail = get_detail(video_id)
        print("=" * 50 + "\n")
        print(f'剧名：{detail.name} | 状态：{detail.status} | 总集数：{detail.total} | 备注：{detail.remarks}')
        for i, value in enumerate(detail.url_list):
            for index, j in enumerate(value):
                print(f'序号：{i}-{index} | 集名：{j.episode_name} | 链接：{j.episode_url}')

        choose_episode_num = int(input("请选择一个集数: "))

        choose_episode_name = detail.url_list[1][choose_episode_num].episode_name
        choose_episode_url = detail.url_list[1][choose_episode_num].episode_url
        final_episode_name = detail.name + '-' + choose_episode_name
        videodownloader = VideoDownload(url=choose_episode_url, name=final_episode_name).main()
        break

