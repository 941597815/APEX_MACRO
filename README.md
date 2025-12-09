# Apex-Macro

需要硬件 RP2040_HOST / RP2350-USB-A

#### 功能：

- 抖枪（抖动以抵消后坐力，capsLock 打开或关闭。只在鼠标左右键同时按下时启动）
- 一键换甲（仅适用于 1920x1080/2560x1440。按键E打开死亡之箱后不移动鼠标，然后松开E键就会执行换甲操作并关闭死亡之箱。如果按键E打开死亡之箱后移动了鼠标就不会执行换甲）
- 快速拾取（按住鼠标侧键x2）
- 变向TS（按住鼠标侧键x1）
- SG（鼠标滚轮向上滚动，会模拟按下SPACE + C ）
- 快速上绳（按住lshift,视角向上对准绳子按E）
- 自动触发MB/SG（只适配了1920x1080,其他分辨率自己修改图片模板和截图位置.需要设置攀爬加速激活->LCRTRL,攀爬加速UI->完整.按住空格时自动触发攀爬加速(成功率>99%),按住lshift时自动触发SG(效果不太好,而且会与攀爬加速冲突)）

#### 软件安装

安装 python >= 3.10.11

安装项目依赖 requirements.txt 若缺少模块请手动安装，如果运行run.bat后闪退一般是有些依赖没有安装

en:
```bash
pip install -r requirements.txt
```
cn:
```bash
pip install -r requirements.txt -i https://mirrors.huaweicloud.com/repository/pypi/simple
```

#### 运行

连接硬件后以管理员身份运行main.py或run.bat

###### HOME/断开硬件 退出程序

###### 配置文件 config.yaml，可以配置启用哪些功能
