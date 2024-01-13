# #!/usr/bin/env python3

# import Hobot.GPIO as GPIO
# import time

# # 支持PWM的管脚: 32 and 33
# output_pin = 33

# def main():
#     # Pin Setup:
#     # Board pin-numbering scheme
#     GPIO.setmode(GPIO.BOARD)
#     # RDK X3支持的频率范围： 48KHz ~ 192MHz
#     # RDK Ultra支持的频率范围： 1Hz ~ 12MHz
#     p = GPIO.PWM(output_pin, 48000)
#     # 初始占空比 25%， 先每0.25秒增加5%占空比，达到100%之后再每0.25秒减少5%占空比
#     val = 25
#     incr = 5
#     p.start(val)

#     print("PWM running. Press CTRL+C to exit.")
#     try:
#         while True:
#             time.sleep(0.25)
#             if val >= 100:
#                 incr = -incr
#             if val <= 0:
#                 incr = -incr
#             val += incr
#             p.ChangeDutyCycle(val)
#     finally:
#         p.stop()
#         GPIO.cleanup()

# if __name__ == '__main__':
#     main()
#!/usr/bin/env python3

import Hobot.GPIO as GPIO
import time

# 定义寻迹模块使用的GPIO通道
track_1 = 15 # BOARD 编码 15   X1
track_2= 16 # BOARD 编码 16    X2
track_3 = 22 # BOARD 编码 22     X3
track_4 = 26 # BOARD 编码 26 X4
#定义寻迹模块返回值 --模式
STRAIGHT=1
LEFT=2
RIGHT=3
WHITE=4
BLACK=5
#定义控制对象
MOTOR=1
SERVO=2
#定义行进模式状态机
Gmode=0

def track_get(): # 找到循迹模式
    value_1 = GPIO.input(track_1)
    value_2 = GPIO.input(track_2)
    value_3 = GPIO.input(track_3)
    value_4 = GPIO.input(track_4)
    val=[]
    val.append(value_2)
    val.append(value_1)
    val.append(value_3)
    val.append(value_4)
    # 四个GPIO都是白色
    # if value_1==0 and value_2==0 and value_3==0 and value_4==0 : pass
    # elif value_1==1 and value_2==1 and value_3==1 and value_4==1: pass
    # else: pass
    if val==[1,0,0,1] : return STRAIGHT 
    elif val==[0,0,1,1]: return LEFT
    elif val==[1,1,0,0]: return RIGHT 
    elif val==[1,1,1,1]: return WHITE
    elif val==[0,0,0,0]: return BLACK
    else: pass
#obj:控制对象  order:电机方向/舵机转向，value:速度值，或者角度值
def order_gen(obj,order,value): # 生成串口指令
    if obj== MOTOR:#电机控制
        if order==STRAIGHT:
            o='55010600xxxx00xxxxBB'
            d=bytes.fromhex(o)
            return d
        elif order==LEFT:
            o='55010600xxxx00xxxxBB'
            d=bytes.fromhex(o)
            return d
        elif order==RIGHT:
            o='55010600xxxx00xxxxBB'
            d=bytes.fromhex(o)
            return d
    elif obj== SERVO:#舵机控制
        if order==RIGHT:
            o='55020600xxxx00xxxxBB'
            d=bytes.fromhex(o)
            return d
        elif order==LEFT:
            o='5502060000xx0000xxBB'
            d=bytes.fromhex(o)
            return d
    return 
def Init_robot(): #初始化上位机GPIO
    return
def robot_go_straight(speed):  #设置初速度向前走
    od=order_gen(MOTOR,STRAIGHT,speed)
    write_num = ser.write(od)   
    print("go_straight: ", od)
    return od
def robot_turn_right():   #右转
    return
def robot_stop():         #停止
    return
def robot_translation_right():   #向右平移
    return





def main():
    Init_robot()

    # 设置管脚编码模式为硬件编码 BOARD
    GPIO.setmode(GPIO.BOARD)
    # 寻迹模块IO口设置为输入模式
    GPIO.setup(track_1, GPIO.IN)
    GPIO.setup(track_2, GPIO.IN)
    GPIO.setup(track_3, GPIO.IN)
    GPIO.setup(track_4, GPIO.IN)

    print("Starting demo now! Press CTRL+C to exit")
    try:
        #1.打开串口
        print("open and set the serial...")
        ser = serial.Serial("/dev/ttyS3", 115200, timeout=0.1)
        print("succes!")
    except Exception as e:
        print("open serial failed!\n")
    #2.进入初始化状态，设置向前速度
    robot_go_straight(10)   #让机器人直行，直到遇到黑线
    Gmode=0


    while track_get()==WHITE: 
        Gmode=0
        print("WHITE!")
    
    robot_stop()          #遇到黑线机器人停止
    #3.进入寻迹模式
    try:
        while True:
            ####### 判断循迹模式，根据寻迹模块的值决定如何控制电机#######
            if(Gmode==0):
                if track_get() == BLACK:
                    robot_translation_right()   #向右平移
                else:
                    robot_stop()
                    Gmode=1   

            elif(Gmode==1):
                if track_get() != BLACK:
                    robot_go_straight()          #向前移动
                else:
                    robot_stop()
                    Gmode=2 
            elif(Gmode==2):                      #抓取右侧2分
                if track_get() == BLACK:         #然后平移至一分处
                    robot_translation_right()
                else:
                    robot_stop()
                    Gmode=3
            elif(Gmode==3):                     #抓取右侧1分
                if track_get() == BLACK:        #然后平移至出发点位置
                    pass
                else:
                    robot_stop()
                    Gmode=4
            # elif(Gmode==4):
            #     if track_get() == BLACK:
            #         robot_translation_right()
            #     else:
            #         robot_stop()
            #         Gmode=5
            # elif(Gmode==5):
            #     if track_get() == BLACK:
            #         robot_translation_right()
            #     else:
            #         robot_stop()
            #         Gmode=1

            ##################################################
            time.sleep(0.01)
    finally:
        GPIO.cleanup()
        ser.close()

if __name__=='__main__':
    main()


    # test_data = '550106001122003344BB'
    # d=bytes.fromhex(test_data)
    # write_num = ser.write(d)
    # print("Send: ", d)

    # received_data = ser.read(write_num).hex()
    # print("Recv: ", received_data)
    # time.sleep(1)                if track_get() == LEFT:    
                #     print("Value read from pin {} : {}".format(input_pin, value_str))
                # elif track_get() == RIGHT: 
                #     pass
                # elif track_get() == STRAIGHT:
                #     pass
                # else: pass