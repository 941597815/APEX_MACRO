import sys, os
import yaml
from pathlib import Path

# 1. 拿到 exe（或脚本）所在目录
if getattr(sys, "frozen", False):  # 打包后的 exe
    BASE_DIR = Path(sys.executable).parent
else:  # 源码调试
    BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.yaml"
# CONFIG_PATH = pathlib.Path(__file__).with_name("config.yaml")  # 改成 .yaml 后缀


def load_config():
    """加载带注释的 YAML 配置文件并更新全局变量实例"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        for key, value in config.items():
            if hasattr(globals_instance, key):
                setattr(globals_instance, key, value)
    except FileNotFoundError:
        default_config_yaml = """\
# 画面分辨率 1=1920x1080 / 2=2560x1440,桌面分辨率与游戏分辨率需要一致,缩放100%
resolution: 1

# 驱动来源 "RP2040_HOST"
deviceType: "RP2040_HOST"

# 启用或禁用某些功能 YES=启用, NO=禁用
AerialSteering: "YES" #空中转向

Jitter: "YES" #抖动以抵消后坐力

ArmorChange: "YES" #一键更换护甲

QuickPickup: "YES" #快速拾取

SuperGlide: "YES" #滚轮向上 SG

QuickRope: "YES" #快速上绳索
"""
        CONFIG_PATH.write_text(default_config_yaml, encoding="utf-8")
        print(f"已创建默认配置文件: {CONFIG_PATH}")


def save_config():
    """把当前 globals_instance 的数据写回 YAML"""
    # 读取现有 YAML（保留注释）
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # 同步需要保存的字段
    for key in data.keys():
        if hasattr(globals_instance, key):
            data[key] = getattr(globals_instance, key)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


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
        self.fast_rope = False
        self.mouse_L = False
        self.mouse_R = False
        self.device = None
        self.deviceType = "RP2040_HOST"
        self.AerialSteering = "YES"
        self.Jitter = "YES"
        self.QuickPickup = "YES"
        self.SuperGlide = "YES"
        self.QuickRope = "YES"
        self.ArmorChange = "YES"


# 创建全局变量实例
globals_instance = Globals()

# 加载配置文件
load_config()
