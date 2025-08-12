#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Class_fetcher.py
# @time: 2025/8/12 17:24
# DO EVERYTHING WHET YOU WANT
import json
import os

import requests

from config.setting import YML_CONFIG, USER_AGENT

_yml_config = YML_CONFIG.get('ffzy')


# 获取类别
class ClassFetcher:
    def __init__(self):
        self._base_url = _yml_config.get('base_url')
        self._headers = {
            'user-agent': USER_AGENT
        }
        self._class_list = None
        self._get_class_list()

    # 获取类别列表
    def _get_class_list(self):
        result = requests.get(url=self._base_url, headers=self._headers).json()
        class_list = result.get('class')
        self._class_list = class_list # 赋值给类变量
        if class_list:
            self._clean_class_json_file()
            print('正在更新类别列表...')
            with open('../config/Class.json', 'w',encoding='utf-8') as w:
                json.dump(class_list, w, ensure_ascii=False, indent=4)

    # 清空文件内容
    @staticmethod
    def _clean_class_json_file():
        if os.path.exists('../config/Class.json'):
            with open('../config/Class.json', 'w') as w:
                w.truncate()
            print('清空类别列表成功...')

    # 获取类别列表
    def get_class_list(self):
        return self._class_list



if __name__ == '__main__':
    class_fetcher = ClassFetcher()
    class_list = class_fetcher.get_class_list()
    print(class_list)
