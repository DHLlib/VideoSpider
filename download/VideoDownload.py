#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: VideoSpider.py
# @time: 2025/8/10 00:26
# @version:
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests

from config.setting import USER_AGENTS
from utils.Log_Manager import *
from .Ffmpeg_control import FfmpegControl

# USER_AGENT = user_agent.USER_AGENTS[0]
# config = source.ff
# BASE_URL = config.get('base_url')
# DETAIL = config.get('detail')

"""
传入任意剧集的URL，并且传入类型：0:m3u8;1:normal
"""


# 任意一集的m3u8，下载器
class VideoDownload:
    def __init__(self, url, name, episode_name, type_=0):
        """
        :param url:
        :param type_: 0:m3u8,1:normal
        :param episode_name 剧集名称
        """
        self.headers = {
            "user-agent": random.choice(USER_AGENTS)
        }
        self.episode_name = episode_name  # 集数名称
        self.name = name  # 剧名
        self.url = url
        self.type = type_
        self.m3u8_url = self.classifier()  # https://vip.ffzy-play2.com/20221213/9185_83e0890b/
        self.base_m3u8_url = self.extracting_url(
            self.m3u8_url)  # https://vip.ffzy-play2.com/20221213/9185_83e0890b/2000k/hls/
        self.ts_base_url = None
        self.output = f"{os.path.dirname(os.path.dirname(__file__))}/output"
        self.video_dir = self.dir_check_and_mkdir()
        self.ffmpeg = FfmpegControl(self.video_dir, self.episode_name)

    # 分流器
    @log_manager.log_method
    def classifier(self):
        if 'index.m3u8' in self.url:
            m3u8_url = self.url
        else:
            m3u8_url = self.normal_to_m3u8()
        return m3u8_url

    # 检查文件夹
    @log_manager.log_method
    def dir_check_and_mkdir(self):
        name_path = os.path.join(self.output, self.name)  # 剧名目录
        if not os.path.exists(name_path):
            os.mkdir(name_path)
        return name_path

    @staticmethod
    @log_manager.log_method
    def extracting_url(url):
        # 解析URL
        parsed_url = urlparse(url)
        logger.info("原始URL:", parsed_url)
        # 获取基础域名和路径，然后去掉文件名部分
        base_with_path = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        logger.info("基础域名和路径:", base_with_path)
        # 找到最后一个/的位置，去掉文件名部分
        last_slash_index = base_with_path.rfind('/')
        m3u8_base_url = base_with_path[:last_slash_index + 1]

        return m3u8_base_url  # 输出: https://vip.ffzy-play2.com/20221213/9185_83e0890b/

    # 普通地址转m3u8
    @log_manager.log_method
    def normal_to_m3u8(self):
        """
        :return: https://vip.ffzy-play2.com/20221213/9185_83e0890b/index.m3u8?sign=a220641044bd92b4a5c8e614b26400b9
        """
        result = requests.get(url=self.url, headers=self.headers).text
        # 使用正则表达式提取 url
        pattern = r'const url\s*=\s*"([^"]+)"'
        match = re.search(pattern, result)
        parsed_url = urlparse(self.url)
        logger.info("原始URL:", parsed_url)
        top_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        logger.info("基础域名和路径:", top_url)
        mixed_m3u8_url = top_url + match[1]
        return mixed_m3u8_url

    # 提取标准m3u8地址，获取ts列表文件地址
    @log_manager.log_method
    def m3u8_to_tsfile(self):
        result = requests.get(url=self.m3u8_url, headers=self.headers).text
        mixed_m3u8 = re.sub('#.*', '', result).strip()  # 提取'2000k/hls/mixed.m3u8'
        ts_list_url = self.base_m3u8_url + mixed_m3u8
        self.ts_base_url = self.extracting_url(ts_list_url)
        return ts_list_url

    # 获取ts列表文件地址，并解析ts列表
    @log_manager.log_method
    def get_ts_list(self, url):
        result = requests.get(url=url, headers=self.headers).text
        ts_files = re.findall(r'([a-f0-9]+\.ts)', result)
        with open(f'{self.video_dir}/index.m3u8', 'w', encoding='utf-8') as w:
            w.write(result)
        ts_list = []
        for ts_file in ts_files:
            ts_list.append(ts_file)
        return ts_list

    # 下载ts
    @log_manager.log_method
    def download_single_ts(self, ts_index, ts):
        url = self.ts_base_url + ts
        logger.info(f'下载链接：{url}')
        max_retries = 3  # 最大重试次数
        retry_delay = 1  # 重试延迟

        for attempt in range(max_retries):
            try:
                logger.info(f"正在下载片段 {ts_index + 1}: {ts} (尝试 {attempt + 1}/{max_retries})")
                response = requests.get(
                    url=url,
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                content = response.content
                # 直接写入ts
                with open(f'{self.video_dir}/{ts}', 'wb') as ts_w:  # 使用二进制模式
                    ts_w.write(content)
                return ts_index, None  # 保持返回3个值

            except Exception as e:
                error_msg = str(e)
                if attempt < max_retries - 1:  # 尝试次数未达到最大值
                    wait_time = retry_delay * (2 ** attempt)
                    logger.error(f"请求失败：{error_msg}，{wait_time}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"重试{max_retries}次后仍然失败: {error_msg}")
                if attempt == max_retries - 1:
                    return ts_index, ts  # 失败时返回索引和ts文件名
        return ts_index, ts  # 确保失败时返回索引和ts文件名

    @log_manager.log_method
    def Multithreading_download_ts_to_mp4(self, ts_list, max_workers):
        # 多线程下载
        false_list = []
        successful_downloads = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            futures = [executor.submit(self.download_single_ts, i, ts) for i, ts in enumerate(ts_list)]
            logger.info("正在下载...")
            logger.info(f'{futures}')
            # 收集结果
            for future in as_completed(futures):
                index, ts = future.result()
                if ts is None:
                    successful_downloads += 1
                else:
                    false_list.append(ts)
                logger.info(f"已完成下载: {successful_downloads}/{len(ts_list)}")
        # todo 增加重试机制，将失败的ts集合返回，并重新重试

        # 使用ffmpeg合并ts
        self.ffmpeg.merge_ts_file()

    def main(self, max_workers=10):
        max_workers = int(max_workers)
        # 提取ts文件链接
        ts_url = self.m3u8_to_tsfile()
        # 获取ts列表
        ts_list = self.get_ts_list(ts_url)
        # print(ts_list)
        # 多线程下载
        self.Multithreading_download_ts_to_mp4(ts_list, max_workers)


if __name__ == '__main__':
    video1 = VideoDownload("https://vip.ffzy-play2.com/share/51681a7c14879f9eca39669df858f75b", '第01集', 1)
    video1.main()

    # video2 = VideoDownload("https://vip.ffzy-play2.com/20221213/9185_83e0890b/index.m3u8", 0,'第01集')
