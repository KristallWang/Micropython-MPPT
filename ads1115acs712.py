from machine import I2C, Pin # type: ignore
from ads1x15 import ADS1115
import time

class SensorModule:
    def __init__(self, i2c, config_file='MPPT-settings.json'):
        # 加载配置文件 avgCountVS=10, avgCountCS=10, inVoltageDivRatio=1.0, outVoltageDivRatio=1.0, currentMidPoint=2.5, currentSensV=0.185):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.avgCountVS = config.get('avgCountVS', 3)
        self.avgCountCS = config.get('avgCountCS', 4)
        self.inVoltageDivRatio = config.get('inVoltageDivRatio', 40.2156)
        self.outVoltageDivRatio = config.get('outVoltageDivRatio', 24.5000)
        self.currentMidPoint = config.get('currentMidPoint', 2.5250)
        self.currentSensV = config.get('currentSensV', 0.0660)
        # 其他初始化代码...
        self.i2c = i2c
        
        #self.ads = ADS1115(i2c)
        #self.ads.gain = 1
        #self.avgCountVS = avgCountVS
        #self.avgCountCS = avgCountCS
        #self.inVoltageDivRatio = inVoltageDivRatio
        #self.outVoltageDivRatio = outVoltageDivRatio
        #self.currentMidPoint = currentMidPoint
        #self.currentSensV = currentSensV

    def read_voltage(self, channel):
        voltage_sum = 0.0
        for _ in range(self.avgCountVS):
            voltage_sum += self.ads.read(channel) * self.ads.v_per_bit
        return voltage_sum / self.avgCountVS

    def read_current(self, channel):
        current_sum = 0.0
        for _ in range(self.avgCountCS):
            current_sum += self.ads.read(channel) * self.ads.v_per_bit
        return current_sum / self.avgCountCS

    def get_sensor_data(self):
        VSI = self.read_voltage(3)
        VSO = self.read_voltage(1)
        voltageInput = VSI * self.inVoltageDivRatio
        voltageOutput = VSO * self.outVoltageDivRatio

        CSI = self.read_current(2)
        CSI_converted = CSI * 1.3300
        currentInput = ((CSI_converted - self.currentMidPoint) * -1) / self.currentSensV
        if currentInput < 0:
            currentInput = 0.0
        if voltageOutput <= 0:
            currentOutput = 0.0
        else:
            currentOutput = (voltageInput * currentInput) / voltageOutput

        if voltageInput <= 3 and voltageOutput <= 3:
            inputSource = 0
        elif voltageInput > voltageOutput:
            inputSource = 1
        else:
            inputSource = 2

        return {
            "voltageInput": voltageInput,
            "voltageOutput": voltageOutput,
            "currentInput": currentInput,
            "currentOutput": currentOutput,
            "inputSource": inputSource,
            "currentMidPoint": self.currentMidPoint
        }

    def calibrate_current_sensor(self, buckEnable, FLV, OOV):
        if buckEnable == 0 and FLV == 0 and OOV == 0:
            CSI = self.read_current(2)
            self.currentMidPoint = (CSI * 1.3300) - 0.003
