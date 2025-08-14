#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: Detail_fetcher.py
# @time: 2025/8/10 23:42
# @version:

import requests

from config.setting import YML_CONFIG, USER_AGENT
from models.DTOs import VideoEpisodeDTO, VideoDetailDTO

_yml_config = YML_CONFIG.get('ffzy')


# 获取视频详情

class DetailFetcher:
    def __init__(self, vod_id):
        self._vod_id = vod_id  # 视频id
        self._base_url = _yml_config.get('base_url')
        self._detail_path = _yml_config.get('detail')
        self._headers = {
            'user-agent': USER_AGENT
        }
        self._vod_name = None
        self._vod_status = None
        self._vod_remarks = None
        self._vod_total = None
        self._play_url_lists = None  # 播放列表
        # -----------先定义变量，再实现方法-----------------
        self._get_detail()  # 请求详情

    # 解析detail
    def _parse_detail_json(self, result):
        self._vod_name = result.get('vod_name').strip()
        self._vod_status = result.get('vod_status')
        self._vod_remarks = result.get('vod_remarks')
        self._vod_total = result.get('vod_total')  # 总集数
        vod_play_url_str = result.get('vod_play_url')  # 播放列表
        groups = vod_play_url_str.split("$$$")

        video_detail = VideoDetailDTO(
            name=self._vod_name,
            status=self._vod_status,
            remarks=self._vod_remarks,
            total=self._vod_total,
            url_list=[]
        )
        groups_list = []
        # 组转列表
        for index, group in enumerate(groups):
            # 按 # 分割剧集，并过滤空字符串
            episodes = [item for item in group.split("#") if item]
            group_data = []
            for item in episodes:
                parts = item.split("$")
                if len(parts) >= 2:  # 剧集名称和播放链接
                    # 创建VideoEpisodeDTO对象,保存剧集名称和播放链接
                    video_episodes = VideoEpisodeDTO(
                        episode_name=parts[0],
                        episode_url=parts[1]
                    )
                    group_data.append(video_episodes)
            # video_detail.url_list[from_[index]] = group_data
            groups_list.append(group_data)
        video_detail.url_list = groups_list
        self._play_url_lists = video_detail

    # 获取页面详情
    def _get_detail(self):
        detail_url = self._base_url + self._detail_path + str(self._vod_id)
        result = requests.get(url=detail_url, headers=self._headers)
        # 检查HTTP状态码
        if result.status_code != 200:
            raise requests.RequestException(f"HTTP请求失败，状态码: {result.status_code}")
        result_json = result.json()
        list_ = result_json.get('list')
        if list_:
            self._parse_detail_json(list_[0])
        else:
            raise ValueError(f"返回结果为空:{list_}")

    def get_name(self):
        return self._vod_name

    def get_status(self):
        return self._vod_status

    def get_id(self):
        return self._vod_id

    def get_play_lists(self):
        return self._play_url_lists


if __name__ == '__main__':
    # 30490
    detail_fetcher = DetailFetcher('83074')
    url_list = detail_fetcher.get_play_lists()
    print(f'剧名：{url_list.episode_name}')
    print(f'剧集状态：{url_list.status}')
    print(f'总数量：{url_list.total}')
    print(f'备注：{url_list.remarks}')
    episodes_list = url_list.url_list
    print("==============================================")
    for i in episodes_list:
        for j in i:
            print(f'{j.episode_name}|{j.episode_url}')
        print("==============================================")
    print("==============================================")

    # for i in url_list.url_list:
    #     for j in i:
    #         print(f'{j.episode_name}|{j.episode_url}')
