#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: Detail_fetcher.py
# @time: 2025/8/10 23:42
# @version:

from core.Base_fetcher import BaseFetcher
from models.DTOs import VideoEpisodeDTO, VideoDetailDTO
from utils.Log_Manager import *


# 获取视频详情

class DetailFetcher(BaseFetcher):
    def __init__(self, vod_id):
        fetcher_type = 'detail'
        super().__init__(type_=fetcher_type, resource_name='ffzy')
        self._local_params = self._params.copy()

        self._vod_id = vod_id  # 视频id
        self._vod_name = None
        self._vod_status = None
        self._vod_remarks = None
        self._vod_total = None
        self._play_url_lists = None  # 播放列表
        # -----------先定义变量，再实现方法-----------------
        self._get_detail()  # 请求详情

    # 解析detail
    @log_manager.log_method
    def _parse_detail_json(self, result):
        self._vod_name = result.get('vod_name').strip()
        self._vod_status = result.get('vod_status')
        self._vod_remarks = result.get('vod_remarks')
        self._vod_total = result.get('vod_total')  # 总集数
        vod_play_url_str = result.get('vod_play_url')  # 播放列表
        groups = vod_play_url_str.split("$$$")
        logger.info(
            f"剧集名称：{self._vod_name},"
            f"剧集状态：{self._vod_status},"
            f"总集数：{self._vod_total},"
            f"备注：{self._vod_remarks},"
            f"播放列表：{groups}")

        # 创建VideoDetailDTO对象
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
        logger.info(f"获取详情成功:{video_detail}")
        self._play_url_lists = video_detail

    # 获取页面详情
    def _get_detail(self):
        self._local_params['ids'] = self._vod_id
        result = super()._request(self._local_params)  # 请求详情
        list_ = result.get('list')
        if list_:
            self._parse_detail_json(list_[0])
        else:
            raise ValueError(f"返回结果为空:{list_}")

    @log_manager.log_method
    def get_name(self):
        return self._vod_name

    @log_manager.log_method
    def get_status(self):
        return self._vod_status

    @log_manager.log_method
    def get_id(self):
        return self._vod_id

    @log_manager.log_method
    def get_play_lists(self):
        return self._play_url_lists


if __name__ == '__main__':
    # 30490
    detail_fetcher = DetailFetcher('19212')
    url_list = detail_fetcher.get_play_lists()
    print(f'剧名：{url_list.name}')
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
