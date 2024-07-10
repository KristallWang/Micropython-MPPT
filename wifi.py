# wifi.py
import time
import network
'_cat_house_', 'timeistime'

def wifi_connect(ssid, password):
    # 创建 WIFI 连接对象
    wlan = network.WLAN(network.STA_IF)
    # 激活 wlan 接口
    wlan.active(True)

    # 断开之前的链接
    wlan.disconnect()
    # 扫描允许访问的 WiFi
    print('扫描周围信号源：', wlan.scan())

    print("正在连接 WiFi 中", end="")
    # 连接 wifi
    wlan.connect(ssid, password)

    # 如果一直没有连接成功，则每隔 0.1s 在命令号中打印一个 .
    while not wlan.isconnected():
      print(".", end="")
      time.sleep(0.1)

    # 连接成功之后，打印出 IP、子网掩码(netmask)、网关(gw)、DNS 地址
    print(f"\n{wlan.ifconfig()}")
# 连接 wifi 并获取网络接口对象