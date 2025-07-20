import json

# 配置文件路径
CONFIG_PATH = "config.json"


def load_config():
    """加载JSON配置文件并更新全局变量实例"""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            # 更新实例属性
            for key, value in config.items():
                if hasattr(globals_instance, key):
                    setattr(globals_instance, key, value)
    except FileNotFoundError:
        # 创建默认配置文件
        default_config = {
            "resolution": 1,
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)
        print(f"已创建默认配置文件: {CONFIG_PATH}")


# 定义全局变量
class Globals:
    class version:
        version = 1

    def __init__(self):
        self.status = False
        self.running = False
        self.resolution = 1
        self.zhuanxiang = False
        self.douqiang = False
        self.e = False
        self.mouse_L = False
        self.mouse_R = False


# 创建全局变量实例
globals_instance = Globals()

# 加载配置文件
load_config()
