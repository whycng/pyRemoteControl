# server/stealth.py
import sys
import os
import ctypes


class Stealth:
    @staticmethod
    def hide_console():
        if sys.platform == "win32":
            try:
                kernel32 = ctypes.WinDLL('kernel32')
                user32 = ctypes.WinDLL('user32')
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.ShowWindow(hwnd, 0)
            except:
                pass
        else:
            # Linux下可以使用其他方式隐藏进程
            try:
                os.setpgrp()  # 将进程从终端分离
            except:
                pass

    @staticmethod
    def hide_process():
        if sys.platform == "win32":
            try:
                # Windows专用代码
                import win32process
                import win32con
                handle = win32process.GetCurrentProcess()
                win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
            except:
                pass
        else:
            # Linux下的进程隐藏
            try:
                os.nice(19)  # 设置最低优先级
            except:
                pass

    @staticmethod
    def run_as_service():
        if sys.platform == "win32":
            # Windows服务实现
            pass
        else:
            # Linux守护进程实现
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)  # 父进程退出
            except OSError:
                pass

            # 修改工作目录
            os.chdir('/')
            # 设置新的会话
            os.setsid()
            # 修改文件创建掩码
            os.umask(0)

            # 第二次fork
            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)  # 第二个父进程退出
            except OSError:
                pass