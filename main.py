#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: main.py
# @time: 2025/8/14 21:36
# @version:
from control.Base_control import format_output_console, get_detail, search_video
from download.VideoDownload import VideoDownload


def main():
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
                VideoDownload(url=choose_episode_url, name=detail.name,
                              episode_name=choose_episode_name).main()  # 下载
        else:
            choose_episode_name = detail.url_list[video_source][int(choose_episode_num)].episode_name
            choose_episode_url = detail.url_list[video_source][int(choose_episode_num)].episode_url
            final_episode_name = detail.name + '-' + choose_episode_name
            print(f'正在下载视频源：{choose_episode_num} | {final_episode_name} | {choose_episode_url}')
            VideoDownload(url=choose_episode_url, name=detail.name, episode_name=final_episode_name).main()  # 下载
        break


if __name__ == '__main__':
    main()
