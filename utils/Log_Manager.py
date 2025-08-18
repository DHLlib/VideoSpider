#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: DENGHAOLUAN
# @file: Log_Manager.py
# @time: 2025/8/18 10:25
# DO EVERYTHING WHET YOU WANT
import logging
import os
import time
from functools import wraps
from logging.handlers import RotatingFileHandler

from config.setting import SYS_CONFIG


# 日志类
class LogManager:
    _instance = None  # 单例模式标志

    def __new__(cls, *args, **kwargs):
        """
        单例模式实现，确保只创建一次实例
        """
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化日志配置（仅执行一次）
        """
        # 避免重复初始化
        if hasattr(self, 'logger'):
            return
        self.now_data = time.strftime("%Y-%m-%d", time.localtime())

        # 将字符串等级转为 logging 模块的等级常量
        self.level = getattr(logging, SYS_CONFIG['log_level'].upper(), logging.INFO)

        # 获取根 logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.level)

        # 定义格式
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 设置日志文件路径：项目根目录下的 logs/app.log
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_dir = os.path.join(project_root, 'logs')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file_path = os.path.join(self.log_dir, f'VideoSpider_{self.now_data}.log')

        # 自动创建 logger
        self.create_logger()

    def create_logger(self):
        """
        创建并返回一个带控制台和文件输出的日志器
        """
        # 避免重复添加 handler
        if not self.logger.handlers:
            # 创建日志目录（如果不存在）
            os.makedirs(self.log_dir, exist_ok=True)


            # 使用 RotatingFileHandler 实现日志拆分
            file_handler = RotatingFileHandler(
                self.log_file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=100,  # 最多保留 5 个备份文件
                encoding='utf-8'
            )
            file_handler.setLevel(self.logger.level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

            # 控制台输出,为 True，则 输出到控制台
            if SYS_CONFIG['debug']:
                # 控制台 Handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(self.logger.level)
                console_handler.setFormatter(self.formatter)
                self.logger.addHandler(console_handler)

        return self.logger

    def log_method(self, func):
        """
        装饰器方法，用于记录被装饰函数的调用信息
        :param func: 被装饰的方法
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取 func的所在的类名，如果不存在，则为  None
            class_name = func.__qualname__.split('.')[0] if '.' in func.__qualname__ else None
            class_method = f"{class_name}.{func.__name__}"  # 组装
            self.logger.info(f"正在调用方法: {class_method}, 参数: args={args}, kwargs={kwargs}")
            # 获取第一个参数（优先 args[1]，否则取 kwargs 的第一个 key-value）
            if len(args) > 1:
                first_arg = args[1]
            elif kwargs:
                first_key = next(iter(kwargs.keys()))
                first_arg = f"{first_key}={kwargs[first_key]}"
            else:
                first_arg = None
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                self.logger.info(f"方法 {class_method} 执行完成，耗时: {end_time - start_time:.4f} 秒")
                self.logger.info(f"方法返回值: {result}")
                self.logger.info(f"请求接口: {first_arg}")
                return result
            except Exception as e:
                self.logger.error(f"方法 {func.__name__} 抛出异常: {e}", exc_info=True)
                raise

        return wrapper


log_manager = LogManager()  # 👈 第一次实例化会自动初始化日志系统
logger = log_manager.logger  # 可选：直接获取 logger 对象