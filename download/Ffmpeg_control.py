#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: Ffmpeg_control.py
# @time: 2025/8/13 21:25
# @version:
import os.path
import subprocess

from utils.Log_Manager import log_manager, logger


# ffmpeg控制器

class Ffmpeg:
    """父类"""

    def __init__(self):
        self.check_ffmpeg_installed()

    @staticmethod
    @log_manager.log_method
    def check_ffmpeg_installed():
        try:
            # 执行 ffmpeg -version 命令
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f'检测完成：{result}')
            if result.returncode == 0:
                logger.info(f'检测完成，已安装ffmpeg')
                return True
            else:
                logger.error("检测完成：请检查是否配置系统环境变量：PATH")
                return False
        except FileNotFoundError:
            logger.error("检测完成：请安装FFmpeg或者检查环境变量.")
            return False


class FfmpegControl(Ffmpeg):
    def __init__(self, ts_cache_dir, video_filepath):
        """
        :param ts_cache_dir: ts文件路径，同时index.m3u8也要存放在此处
        :param video_filepath: 视频最终文件路径
        """
        super().__init__() # 调用父类初始化方法
        # 获取输出目录
        self._ts_dir = ts_cache_dir  # （如"E:D:/TEMP/cache/JOJO的奇妙冒险"）
        self._video_filepath = video_filepath  # （如 "D:/TEMP/output/JOJO的奇妙冒险/JOJO的奇妙冒险_第01集.mp4"）
        logger.info(f'输出文件路径: {self._video_filepath}')
        self._index_m3u8 = os.path.join(self._ts_dir, f'index.m3u8')  # （如 "D:/TEMP/index.m3u8"）
        logger.info(f'm3u8&ts文件路径: {self._ts_dir}')

    @log_manager.log_method
    def merge_ts_file(self):
        """
        使用 FFmpeg 合并 M3U8 播放列表中的所有 TS 文件
        :return:
        """
        # output_dir = str(Path(self._video_filepath).resolve())
        # index_m3u8 = str(Path(self._index_m3u8).resolve())

        if not os.path.exists(self._ts_dir):
            logger.error(f"M3U8 文件不存在: {self._ts_dir}")
            raise FileNotFoundError(f"M3U8 文件不存在: {self._ts_dir}")

        # 执行合并
        try:
            cmd = [
                "ffmpeg",
                "-protocol_whitelist", "file,http,https,tcp,tls",  # 允许本地文件协议
                "-i", self._index_m3u8,
                "-c", "copy",  # 直接流复制，不重新编码
                "-y",  # 覆盖输出文件
                self._video_filepath
            ]
            logger.info(f'执行命令：{cmd}')
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            logger.info(f"合并成功！输出文件: {self._video_filepath}")
            return
        except subprocess.CalledProcessError as e:
            logger.error(f"直接合并失败，尝试备用方法... (错误: {e.stderr.decode('utf-8')[:200]})")


if __name__ == '__main__':
    F = FfmpegControl(1, 1)
