#!/usr/bin/env python3
import sys
import signal
import Hobot.GPIO as GPIO
import time
import os

# 导入python串口库
import serial
import serial.tools.list_ports

HIGH = GPIO.HIGH
LOW = GPIO.LOW

def signal_handler(signal, frame):
    sys.exit(0)

# 定义使用的GPIO通道为38
output_pin = 37 # BOARD 编码 37
GPIO_pin_X1=11;# BOARD 编码 11
GPIO_pin_X2=13;# BOARD 编码 13
GPIO_pin_X3=15;# BOARD 编码 11
GPIO_pin_X4=16;# BOARD 编码 11

def main():
    # 设置管脚编码模式为硬件编号 BOARD
    GPIO.setmode(GPIO.BOARD)
    # 设置为输出模式，并且初始化为高电平
    GPIO.setup(output_pin, GPIO.OUT, initial=LOW)
    GPIO.setup(GPIO_pin_X1,GPIO.IN)
    GPIO.setup(GPIO_pin_X2,GPIO.IN)
    GPIO.setup(GPIO_pin_X3,GPIO.IN)
    GPIO.setup(GPIO_pin_X4,GPIO.IN)
	
    uart_dev='/dev/ttyS3'
    baudrate = 9600

	
    # 记录当前管脚状态
    curr_value = LOW
    print("Starting demo now! Press CTRL+C to exit")
    try:
        ser = serial.Serial(uart_dev, int(baudrate), timeout=1) # 1s timeout
    except Exception as e:
        print("open serial failed!\n")
    try:
        # 间隔1秒时间，循环控制LED灯亮灭
        while True:
            X1=GPIO.input(GPIO_pin_X1)
            X2=GPIO.input(GPIO_pin_X2)
            X3=GPIO.input(GPIO_pin_X3)
            X4=GPIO.input(GPIO_pin_X4)
            if X1==LOW and X2==LOW and X3 == LOW and X4==LOW:
              curr_value = HIGH
            else :
              curr_value = LOW
            GPIO.output(output_pin, curr_value)
            
            test_data = '550106001122003344BB'
            d=bytes.fromhex(test_data)
            write_num = ser.write(d)
            print("Send: ", d)

            received_data = ser.read(write_num).hex()
            print("Recv: ", received_data)
            time.sleep(1)
           
            
    finally:
        GPIO.cleanup()
        ser.close()

if __name__=='__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
