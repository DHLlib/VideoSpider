#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: get_video.py
# @time: 2025/8/9 23:13
# @version:
import json
import re
from urllib.parse import urlparse

import requests

URL = "http://api.ffzyapi.com/api.php/provide/vod/?ac=list"
# DETAIL_URL = "http://api.ffzyapi.com/api.php/provide/vod/?ac=detail&ids=30490"
# SEARCH_URL = "http://api.ffzyapi.com/api.php/provide/vod/?ac=search&wd=JOJO"
JOJO = "https://vip.ffzy-play2.com/share/51681a7c14879f9eca39669df858f75b"
SEARCH_URL = "http://api.ffzyapi.com/api.php/provide/vod/?ac=search&wd="
DETAIL_URL = "http://api.ffzyapi.com/api.php/provide/vod/?ac=detail&ids="

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


# 搜索,返回id
def search_video(video_name):
    url = SEARCH_URL + video_name
    result = requests.get(url=url, headers=headers).text
    res_json = json.loads(result)
    list_1 = res_json['list'][0]
    vod_id = list_1['vod_id']
    vod_name = list_1['vod_name']
    return vod_id, vod_name


# 获取详情
def get_detail(vod_id):
    url = DETAIL_URL + str(vod_id)
    result = requests.get(url=url, headers=headers).text
    res_json = json.loads(result)
    list_1 = res_json['list'][0]
    vod_play_url = list_1['vod_play_url']
    # 以$$$拆分成多组
    groups = vod_play_url.split("$$$")

    # 组转列表
    groups_list = []
    for group in groups:
        # 按 # 分割剧集，并过滤空字符串
        episodes = [item for item in group.split("#") if item]
        group_data = []
        for item in episodes:
            episode, url = item.split("$")
            group_data.append({episode: url})
        groups_list.append(group_data)
    return groups_list


# 获取普通地址
def get_normal_url(url):
    result = requests.get(url=url, headers=headers).text
    # 使用正则表达式提取 url
    pattern = r'const url\s*=\s*"([^"]+)"'
    match = re.search(pattern, result)
    # print(match)
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    print(base_url)
    final_url = base_url + match[1]
    return final_url


# 获取m3u8地址
def get_m3u8_url(m3u8_index):
    index_url = m3u8_index
    last_slash_index = index_url.rfind('/')
    player_url = index_url[:last_slash_index + 1]
    result = requests.get(url=index_url, headers=headers).text
    mixed_m3u8 = re.sub('#.*', '', result).strip()  # 提取'2000k/hls/mixed.m3u8'
    # 拼接m3u8
    final_m3u8 = player_url + mixed_m3u8
    ts_play_base_index = final_m3u8.rfind('/')
    ts_play_base_url = final_m3u8[:ts_play_base_index + 1]
    return final_m3u8, ts_play_base_url


# 获取ts文件
def parse_mixed_m3u8(mixed_m3u8_url):
    url = mixed_m3u8_url
    result = requests.get(url=url, headers=headers).text
    ts_files = re.findall(r'([a-f0-9]+\.ts)', result)
    ts_list = []
    for ts_file in ts_files:
        ts_list.append(ts_file)
    return ts_list


# 下载ts
def download_ts_to_mp4(ts, player_url):
    url = player_url + ts
    print(url)
    result = requests.get(url=url, headers=headers).content  # 要用字节
    with open('1.mp4', 'wb') as w:
        w.write(result)


# 直接使用m3u8地址：https://vip.ffzy-play2.com/20221213/9185_83e0890b/index.m3u8
def run1():
    id_, name_ = search_video('JOJO')
    print(f"查询结果：id:{id_},名称：{name_}")
    Episodes_list = get_detail(id_)
    m3u8 = Episodes_list[1]
    m3u8_1 = m3u8[0].get('第01集')
    print(f'详情页：第01集：{m3u8_1}')
    f, p = get_m3u8_url(m3u8_1)
    print(f'final_m3u8：{f}')
    print(f'ts_play_base_url：{p}')
    t_list = parse_mixed_m3u8(f)
    print(f'ts文件列表：{t_list}')
    download_ts_to_mp4(t_list[0], p)

    # 使用普通地址：https://vip.ffzy-play2.com/share/5118af07364440598cd7a922ccf4a955


def run2():
    id_, name_ = search_video('JOJO')
    print(f"查询结果：id:{id_},名称：{name_}")
    Episodes_list = get_detail(id_)
    m3u8 = Episodes_list[0]
    m3u8_1 = m3u8[0].get('第01集')
    print(m3u8_1)
    o = get_normal_url(m3u8_1)
    print(f"ts文件url:{o}")
    f, p = get_m3u8_url(o)
    print(f'final_m3u8：{f}')
    print(f'ts_play_base_url：{p}')
    t_list = parse_mixed_m3u8(f)
    print(f'ts文件列表：{t_list}')
    download_ts_to_mp4(t_list[0], p)


if __name__ == '__main__':
    run2()
