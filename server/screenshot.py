# server/screen_capture.py
import io
import base64
import subprocess
import os
import tempfile
import time

class ScreenCapture:
    @staticmethod
    def capture():
        try:
            print("[截图] 开始创建临时文件...")
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
            print(f"[截图] 临时文件创建成功: {temp_path}")

            # 首先尝试使用import命令
            print("[截图] 尝试使用import命令...")
            try:
                result = subprocess.run(
                    ['import', '-window', 'root', temp_path],
                    check=True,
                    capture_output=True,
                    text=True,
                    env={'DISPLAY': ':0'}
                )
                print("[截图] import命令执行完成")
            except FileNotFoundError:
                print("[截图] import命令未找到，尝试使用gnome-screenshot...")
                # 如果import不可用，尝试使用gnome-screenshot
                try:
                    result = subprocess.run(
                        ['gnome-screenshot', '-f', temp_path],
                        check=True,
                        capture_output=True,
                        text=True,
                        env={'DISPLAY': ':0'}
                    )
                    print("[截图] gnome-screenshot命令执行完成")
                except FileNotFoundError:
                    print("[截图] gnome-screenshot未找到，尝试使用scrot...")
                    # 如果gnome-screenshot也不可用，使用scrot
                    result = subprocess.run(
                        ['scrot', '-z', '-q', '100', temp_path],
                        check=True,
                        capture_output=True,
                        text=True,
                        env={'DISPLAY': ':0'}
                    )
                    print("[截图] scrot命令执行完成")

            # 等待确保文件写入完成
            time.sleep(1)

            # 获取并打印当前用户信息
            user_info = subprocess.run(['whoami'], capture_output=True, text=True)
            print(f"[截图] 当前用户: {user_info.stdout.strip()}")

            # 检查X11权限
            print("[截图] 检查X11权限...")
            xauth_info = subprocess.run(['xauth', 'list'], capture_output=True, text=True)
            print(f"[截图] X11授权信息: {xauth_info.stdout.strip()}")

            # 检查文件是否存在和权限
            if os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                file_perms = oct(os.stat(temp_path).st_mode)[-3:]
                print(f"[截图] 临时文件大小: {file_size} bytes")
                print(f"[截图] 临时文件权限: {file_perms}")
            else:
                print("[截图] 错误: 临时文件不存在")
                return None

            print("[截图] 开始读取图片数据...")
            with open(temp_path, 'rb') as f:
                screenshot_data = f.read()
            print(f"[截图] 读取完成，数据大小: {len(screenshot_data)} bytes")

            print("[截图] 删除临时文件...")
            os.unlink(temp_path)
            print("[截图] 临时文件已删除")

            if len(screenshot_data) == 0:
                print("[截图] 错误: 截图数据为空")
                return None

            print("[截图] 转换为base64...")
            base64_data = base64.b64encode(screenshot_data).decode('utf-8')
            print(f"[截图] base64转换完成，数据大小: {len(base64_data)} chars")

            return base64_data

        except subprocess.CalledProcessError as e:
            print(f"[截图] 命令执行失败: {e}")
            print(f"[截图] 错误输出: {e.stderr if hasattr(e, 'stderr') else 'None'}")
            return None
        except Exception as e:
            print(f"[截图] 发生错误: {e}")
            print(f"[截图] 错误类型: {type(e)}")
            return None