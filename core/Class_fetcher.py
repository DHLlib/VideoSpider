#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Class_fetcher.py
# @time: 2025/8/12 17:24
# DO EVERYTHING WHET YOU WANT
import json
import os

from core.Base_fetcher import BaseFetcher


# 获取类别
class ClassFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(type_='index', resource_name='ffzy')
        self._class_list = None
        self._get_class_list()

    # 请求接口
    def _get_class_list(self):
        result = super()._request()
        self._response_handler(result)

    # 处理返回数据
    def _response_handler(self, result):
        if result:
            class_list = result.get('class')
            self._class_list = class_list  # 赋值给类变量
            if class_list:
                self._clean_class_json_file()
                print('正在更新类别列表...')
                with open('../config/Class.json', 'w', encoding='utf-8') as w:
                    json.dump(class_list, w, ensure_ascii=False, indent=4)
                print('更新类别列表成功...')

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
    class_list_ = class_fetcher.get_class_list()
    print(class_list_)
