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
    for item, episode_value in enumerate(result_list):
        result_str += f"  [{item}] | {episode_value.name} |  {episode_value.vod_id}\n"
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
            print(f'视频源：{i}')
            for index, j in enumerate(value):
                print(f'序号：{index} | 集名：{j.episode_name} | 链接：{j.episode_url}')

        video_source = int(input("请选择一个视频源: "))
        choose_episode_num = input("请选择一个基数编号（按*标识全部下载）: ")
        if video_source > len(detail.url_list) - 1:
            print(f'不存在视频源，请重新选择')
            video_source = int(input("请选择一个视频源: "))
        if choose_episode_num == '*':
            for v in detail.url_list[video_source]:
                choose_episode_name = detail.episode_name + '-' + v.episode_name
                choose_episode_url = v.episode_url
                print(f'正在下载视频源：{choose_episode_num} | {choose_episode_name} | {choose_episode_url}')
                videodownloader = VideoDownload(url=choose_episode_url, episode_name=choose_episode_name).main()
        else:
            choose_episode_name = detail.url_list[video_source][int(choose_episode_num)].episode_name
            choose_episode_url = detail.url_list[video_source][int(choose_episode_num)].episode_url
            final_episode_name = detail.name + '-' + choose_episode_name
            print(f'正在下载视频源：{choose_episode_num} | {final_episode_name} | {choose_episode_url}')
            videodownloader = VideoDownload(
                url=choose_episode_url,
                name=detail.name,
                episode_name=final_episode_name
            ).main()
        break
