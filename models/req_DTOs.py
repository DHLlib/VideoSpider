#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: req_DTOs.py
# @time: 2025/8/25 21:22
# @version:
from pydantic import BaseModel

"""请求模板"""


@classmethod
class BaseReqModel(BaseModel):
    """基础请求参数模板"""
    sources: list = None,
    action: str = None,
    page: int = 1,
    page_size: int = 20
