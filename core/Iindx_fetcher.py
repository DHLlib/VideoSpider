#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Iindx_fetcher.py
# @time: 2025/8/12 14:29
# DO EVERYTHING WHET YOU WANT

import requests

from config.setting import YML_CONFIG, USER_AGENT

_yml_config = YML_CONFIG.get('ffzy')

# 获取首页信息
