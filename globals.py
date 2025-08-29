# import json

# # 配置文件路径
# CONFIG_PATH = "config.json"


# def load_config():
#     """加载JSON配置文件并更新全局变量实例"""
#     try:
#         with open(CONFIG_PATH, "r") as f:
#             config = json.load(f)
#             # 更新实例属性
#             for key, value in config.items():
#                 if hasattr(globals_instance, key):
#                     setattr(globals_instance, key, value)
#     except FileNotFoundError:
#         # 创建默认配置文件
#         default_config = {
#             "resolution": 1,
#         }
#         with open(CONFIG_PATH, "w") as f:
#             json.dump(default_config, f, indent=4)
#         print(f"已创建默认配置文件: {CONFIG_PATH}")
import os
import yaml
import pathlib

CONFIG_PATH = pathlib.Path(__file__).with_name("config.yaml")  # 改成 .yaml 后缀


def load_config():
    """加载带注释的 YAML 配置文件并更新全局变量实例"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}  # 空文件时返回 {}
        for key, value in config.items():
            if hasattr(globals_instance, key):
                setattr(globals_instance, key, value)
    except FileNotFoundError:
        # 创建带注释的默认配置文件
        default_config_yaml = """\
# 画面分辨率 1=1920x1080 / 2=2560x1440
resolution: 1

# 驱动来源 "RP2040" / "ARDUINO"
deviceType: "ARDUINO"
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
        self.mouse_L = False
        self.mouse_R = False
        self.device = None
        self.deviceType = "ARDUINO"  # "RP2040"/"ARDUINO"


# 创建全局变量实例
globals_instance = Globals()

# 加载配置文件
load_config()
