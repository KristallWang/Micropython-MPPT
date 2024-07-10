from machine import Pin, PWM, I2C, ADC
import time
from machine import Pin

import  lcd_i2c #mip.install("github:brainelectronics/micropython-i2c-lcd")  
from lcd_i2c import LCD
i2c = I2C(scl=Pin(22), sda=Pin(21))  # ESP32的I2C引脚
lcd = I2C_LCD.I2cLcd(i2c, 0x27, 2, 16)  # 使用I2C地址0x27，2行16列

# SYSTEM PARAMETERS - Pin Definitions with Pin class
backflow_MOSFET = Pin(27, Pin.OUT)  # Backflow MOSFET as output
buck_IN = PWM(Pin(33, Pin.OUT))          # Buck MOSFET Driver PWM Pin as output
buck_EN = Pin(32, Pin.OUT)          # Buck MOSFET Driver Enable Pin as output
LED = Pin(2, Pin.OUT)               # LED Indicator GPIO Pin as output
FAN = Pin(16, Pin.OUT)              # Fan GPIO Pin as output
ADC_ALERT = Pin(34, Pin.IN)         # ADC Alert GPIO Pin as input
TempSensor = Pin(35, Pin.IN)        # Temperature Sensor GPIO Pin as input
buttonLeft = Pin(18, Pin.IN)        # Button Left GPIO Pin as input
buttonRight = Pin(17, Pin.IN)       # Button Right GPIO Pin as input
buttonBack = Pin(19, Pin.IN)        # Button Back GPIO Pin as input
buttonSelect = Pin(23, Pin.IN)      # Button Select GPIO Pin as input


#pwm = PWM(Pin(5))  # 使用GPIO 5
#pwm.freq(5000)  # 设置频率为5kHz
#pwm.duty(512)  # 设置占空比为50% (取值范围在0-1023)


import ads1x15 #https://github.com/robert-hh/ads1x15/blob/master/ads1x15.py


adc = ads1x15.ADS1115(i2c)


# 读取指定通道的值
value = adc.read(0)  # 读取通道0
print(value)

# 调整PWM参数以控制MOSF