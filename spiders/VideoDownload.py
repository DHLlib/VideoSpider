#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: VideoSpider.py
# @time: 2025/8/10 00:26
# @version:
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests

from config import user_agent

USER_AGENT = user_agent.USER_AGENTS[0]
# config = source.ff
# BASE_URL = config.get('base_url')
# DETAIL = config.get('detail')

"""
传入任意剧集的URL，并且传入类型：0:m3u8;1:normal
"""



# 任意一集的m3u8，下载器
class VideoDownload:
    def __init__(self, url, name, type_=0):
        """
        :param url:
        :param type_: 0:m3u8,1:normal
        :param name 剧集名称
        """
        self.headers = {
            "user-agent": USER_AGENT
        }
        self.name = name
        self.url = url
        self.type = type_
        self.m3u8_url = self.classifier()  # https://vip.ffzy-play2.com/20221213/9185_83e0890b/
        self.base_m3u8_url = self.extracting_url(
            self.m3u8_url)  # https://vip.ffzy-play2.com/20221213/9185_83e0890b/2000k/hls/
        self.ts_base_url = None
        self.output = f"{os.path.dirname(os.path.dirname(__file__))}/output"

    # 分流器
    def classifier(self):
        if self.type == 0:
            m3u8_url = self.url
        else:
            m3u8_url = self.normal_to_m3u8()
        return m3u8_url

    @staticmethod
    def extracting_url(url):
        # 解析URL
        parsed_url = urlparse(url)

        # 获取基础域名和路径，然后去掉文件名部分
        base_with_path = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        # 找到最后一个/的位置，去掉文件名部分
        last_slash_index = base_with_path.rfind('/')
        m3u8_base_url = base_with_path[:last_slash_index + 1]

        return m3u8_base_url  # 输出: https://vip.ffzy-play2.com/20221213/9185_83e0890b/

    # 普通地址转m3u8
    def normal_to_m3u8(self):
        """
        :return: https://vip.ffzy-play2.com/20221213/9185_83e0890b/index.m3u8?sign=a220641044bd92b4a5c8e614b26400b9
        """
        result = requests.get(url=self.url, headers=self.headers).text
        # 使用正则表达式提取 url
        pattern = r'const url\s*=\s*"([^"]+)"'
        match = re.search(pattern, result)
        parsed_url = urlparse(self.url)
        top_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        mixed_m3u8_url = top_url + match[1]
        return mixed_m3u8_url

    # 提取标准m3u8地址，获取ts列表文件地址
    def m3u8_to_tsfile(self):
        result = requests.get(url=self.m3u8_url, headers=self.headers).text
        mixed_m3u8 = re.sub('#.*', '', result).strip()  # 提取'2000k/hls/mixed.m3u8'
        ts_list_url = self.base_m3u8_url + mixed_m3u8
        self.ts_base_url = self.extracting_url(ts_list_url)
        return ts_list_url

    # 获取ts列表文件地址，并解析ts列表
    def get_ts_list(self, url):
        result = requests.get(url=url, headers=self.headers).text
        ts_files = re.findall(r'([a-f0-9]+\.ts)', result)
        ts_list = []
        for ts_file in ts_files:
            ts_list.append(ts_file)
        return ts_list

    # 下载ts
    def download_single_ts(self, ts_index, ts):
        url = self.ts_base_url + ts
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                print(f"正在下载片段 {ts_index + 1}: {ts} (尝试 {attempt + 1}/{max_retries})")
                response = requests.get(
                    url=url,
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                content = response.content
                return ts_index, content, len(content)  # 保持返回3个值

            except Exception as e:
                error_msg = str(e)
                if ("Remote end closed connection" in error_msg or
                        "Connection aborted" in error_msg):
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"连接问题，{wait_time}秒后重试...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"重试{max_retries}次后仍然失败: {ts}")
                else:
                    print(f"下载失败 {ts}: {e}")

                if attempt == max_retries - 1:
                    return ts_index, None, 0  # 失败时也返回3个值

        return ts_index, None, 0  # 确保总是返回3个值

    def Multithreading_download_ts_to_mp4(self, ts_list, max_workers):
        filename = f'{self.name}.mp4'

        # 预创建文件
        with open(filename, 'wb') as w:
            pass
        path = self.output + '/' + filename
        # 存储下载结果
        download_results = {}

        # 多线程下载
        successful_downloads = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交任务
            futures = [executor.submit(self.download_single_ts, i, ts) for i, ts in enumerate(ts_list)]

            # 收集结果
            for future in as_completed(futures):
                index, content, size = future.result()
                if content is not None:
                    download_results[index] = content
                    successful_downloads += 1
                    print(f"已完成下载: {successful_downloads}/{len(ts_list)}")

        # 按顺序写入文件
        print("正在合并文件...")
        with open(f'{path}', 'ab') as w:
            for i in range(len(ts_list)):
                if i in download_results:
                    w.write(download_results[i])

        print(f'写入完成: 成功 {successful_downloads}/{len(ts_list)} 个片段')

    def Multithreading_download_ts_to_mp4_v2(self, ts_list, max_workers):
        # 确保输出目录存在
        os.makedirs(self.output, exist_ok=True)
        filepath = os.path.join(self.output, f'{self.name}.mp4')

        # 创建索引映射，确保按顺序写入
        download_order = {}  # 存储下载完成的片段
        download_lock = threading.Lock()

        def download_and_cache(ts_index, ts):
            url = self.ts_base_url + ts
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    response = requests.get(url=url, headers=self.headers, timeout=30)
                    response.raise_for_status()
                    # 直接返回内容，不存储在全局变量中
                    return ts_index, response.content

                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        print(f"下载失败 {ts}: {e}")
                        return ts_index, None

            return ts_index, None

        # 使用信号量限制并发数
        semaphore = threading.Semaphore(min(max_workers, 5))  # 限制最大并发数

        def limited_download(limit_index, ts):
            with semaphore:
                return download_and_cache(limit_index, ts)

        # 下载所有片段
        completed_count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(limited_download, i, ts)
                       for i, ts in enumerate(ts_list)]

            # 按顺序写入文件
            with open(filepath, 'wb') as final_file:
                # 等待每个片段按顺序完成
                for i in range(len(ts_list)):
                    # 查找对应索引的future
                    for future in futures:
                        index, content = future.result()
                        if index == i:
                            if content is not None:
                                final_file.write(content)
                                completed_count += 1
                            break
                    print(f"已完成: {i + 1}/{len(ts_list)}")

        print(f'写入完成: 成功 {completed_count}/{len(ts_list)} 个片段')

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
