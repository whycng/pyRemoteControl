# utils/network.py
import struct
import json
from utils.crypto import CryptoHandler


class SecureSocket:
    def __init__(self, sock, crypto_handler=None):
        self.sock = sock
        self.crypto = crypto_handler or CryptoHandler()

    def send(self, data):
        try:
            # 将数据转换为JSON字符串
            json_data = json.dumps(data)
            # 加密数据
            encrypted_data = self.crypto.encrypt(json_data.encode('utf-8'))
            # 发送数据长度
            self.sock.sendall(struct.pack('>I', len(encrypted_data)))
            # 发送加密数据
            self.sock.sendall(encrypted_data)
            return True
        except Exception as e:
            print(f"发送数据时出错: {e}")
            return False

    def receive(self):
        try:
            # 接收数据长度
            raw_msglen = self.recvall(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]

            # 接收加密数据
            encrypted_data = self.recvall(msglen)
            if not encrypted_data:
                return None

            # 解密数据
            decrypted_data = self.crypto.decrypt(encrypted_data)
            # 解析JSON
            return json.loads(decrypted_data)
        except Exception as e:
            print(f"接收数据时出错: {e}")
            return None

    def recvall(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)