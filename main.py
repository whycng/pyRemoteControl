# main.py
import sys
import os
# # 获取当前脚本所在的目录
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 将项目根目录添加到 sys.path
# sys.path.append(current_dir)


from server.core import EnhancedServer
from client.core import EnhancedClient
from client.interface import start_interface


def main():
    if len(sys.argv) < 2:
        print("用法: python main.py [server|client]")
        return

    mode = sys.argv[1]

    if mode == 'server':
        server = EnhancedServer()
        server.start()
    elif mode == 'client':
        client = EnhancedClient()
        if len(sys.argv) < 3:
            host = input("输入目标IP: ")
        else:
            host = sys.argv[2]

        if client.connect(host):
            start_interface(client)
    else:
        print("无效的模式")


if __name__ == "__main__":
    main()