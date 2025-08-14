#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: DTOs.py
# @time: 2025/8/14 10:29
# DO EVERYTHING WHET YOU WANT

# 数据传输对象模型
from dataclasses import dataclass
from typing import List


@dataclass
class VideoEpisodeDTO:  # 视频集
    episode_name: str  # 集名
    episode_url: str  # 集的URL


@dataclass
class VideoDetailDTO:
    name: str
    url_list: list[list[VideoEpisodeDTO]]
    status: str
    total: str
    remarks: str


@dataclass
class SearchEpisodeDTO:  # 搜索集
    name: str
    vod_id: str


@dataclass
class VideoSearchDTO:
    search_list: List[SearchEpisodeDTO]
