#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @author: DENGHAOLUAN
# @file: Ffmpeg_control.py
# @time: 2025/8/13 21:25
# @version:
import os.path
import subprocess
from pathlib import Path


# ffmpeg控制器

class Ffmpeg:
    """父类"""

    def __init__(self):
        self.check_ffmpeg_installed()

    @staticmethod
    def check_ffmpeg_installed():
        try:
            # 执行 ffmpeg -version 命令
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f'检测完成，已安装ffmpeg')
                return True
            else:
                print("检测完成：请检查是否配置系统环境变量：PATH")
                return False
        except FileNotFoundError:
            print("检测完成：请安装FFmpeg或者检查环境变量.")
            return False


class FfmpegControl(Ffmpeg):
    def __init__(self, dir, name):
        super().__init__()
        # 获取输出目录
        # self.dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        self.input_path = dir
        self._output_path = os.path.join(self.input_path, f'{name}.mp4')  # （如 "D:/TEMP/output.mp4"）
        self._index_m3u8 = os.path.join(self.input_path, f'index.m3u8')  # （如 "D:/TEMP/index.m3u8"）

    def merge_ts_file(self):
        """
        使用 FFmpeg 合并 M3U8 播放列表中的所有 TS 文件
        :return:
        """
        output_dir = str(Path(self._output_path).resolve())
        index_m3u8 = str(Path(self._index_m3u8).resolve())

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"M3U8 文件不存在: {self.input_path}")

        # 执行合并
        try:
            cmd = [
                "ffmpeg",
                "-protocol_whitelist", "file,http,https,tcp,tls",  # 允许本地文件协议
                "-i", index_m3u8,
                "-c", "copy",  # 直接流复制，不重新编码
                "-y",  # 覆盖输出文件
                output_dir
            ]
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            print(f"合并成功！输出文件: {output_dir}")
            return
        except subprocess.CalledProcessError as e:
            print(f"直接合并失败，尝试备用方法... (错误: {e.stderr.decode('utf-8')[:200]})")


if __name__ == '__main__':
    F = FfmpegControl(1, 1)
