#!/usr/bin/env python3

import sys
import signal
import os
import time

# 导入python串口库
import serial
import serial.tools.list_ports

def signal_handler(signal, frame):
    sys.exit(0)

def serialTest():

    uart_dev='/dev/ttyS3'
    baudrate = 9600
    try:
        ser = serial.Serial(uart_dev, int(baudrate), timeout=1) # 1s timeout
    except Exception as e:
        print("open serial failed!\n")

    print(ser)

    print("Starting demo now! Press CTRL+C to exit")

    while True:
        test_data = "550106001100001100BB"
        write_num = ser.write(test_data.encode('UTF-8'))
        print("Send: ", test_data)

        received_data = ser.read(write_num).decode('UTF-8')
        print("Recv: ", received_data)

        time.sleep(1)

    ser.close()
    return 0


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    if serialTest() != 0:
        print("Serial test failed!")
    else:
        print("Serial test success!")
