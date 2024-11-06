# utils/crypto.py
from cryptography.fernet import Fernet
import base64

# 使用固定的密钥
DEFAULT_KEY = b'your_fixed_key_here_make_it_32_bytes!'  # 32字节的密钥


class CryptoHandler:
    def __init__(self, key=DEFAULT_KEY):
        if isinstance(key, str):
            key = key.encode()

        # 确保密钥是32字节
        key = key[:32].ljust(32, b'0')
        # 转换为Fernet可用的格式
        self.key = base64.urlsafe_b64encode(key)
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        try:
            return self.cipher_suite.encrypt(data)
        except Exception as e:
            print(f"加密错误: {e}")
            return data

    def decrypt(self, data):
        try:
            decrypted = self.cipher_suite.decrypt(data)
            try:
                return decrypted.decode()
            except UnicodeDecodeError:
                return decrypted
        except Exception as e:
            print(f"解密错误: {e}")
            return data