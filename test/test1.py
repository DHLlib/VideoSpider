#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: test1.py
# @time: 2025/8/9 23:22
# @version:
import os

# 获取逻辑 CPU 核心数（通常等于线程数）
thread_count = os.cpu_count()
print(f"CPU 逻辑核心数（线程数）: {thread_count}")
