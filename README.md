
搭起了框架，具体功能（截图，键盘记录）实现仍存在问题，比如x11问题

---

win11作为客户端，ubuntu虚拟机作为服务器，通信、命令执行没有问题

---

remote_control/
│
├── server/
│   ├── init.py
│   ├── core.py          # 核心服务端功能
│   ├── keylogger.py     # 键盘记录模块
│   ├── screenshot.py    # 屏幕截图模块
│   ├── stealth.py       # 隐藏进程模块
│   └── persistence.py   # 自启动模块
│
├── client/
│   ├── init.py
│   ├── core.py          # 核心客户端功能
│   └── interface.py     # 用户界面
│
└── utils/
├── init.py
├── crypto.py        # 加密通信
└── network.py       # 网络传输
![image](https://github.com/user-attachments/assets/3db76ba4-aa94-4c24-9530-f7197c365f25)
