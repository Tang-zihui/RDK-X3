#from tracking import tracking
#电机控制指令宏定义
M_HEADER='550106' #电机控制头帧
S_HEADER='550206' #舵机控制头帧
LEFT_FWD='00'   #左侧轮正转指令
LEFT_BCK='FF'   #左侧轮反转指令
RIGHT_FWD='FF'  #右侧轮正转指令
RIGHT_BCK='00'  #右侧轮反转指令
TAIL='BB'

FORWARD=1       #前进
BACK=2          #后退
TRANS_LEFT=3    #向左平移
TRANS_RIGHT=4   #向右平移
LEFT_TURN=5     #向左自转
RIGHT_TURN=6    #向右自转
#舵机控制指令宏定义
SERVO1=1
SERVO2=2
SERVO3=3
SERVO4=4

SMOV='11'
SSTOP='00'
S_NO='00'

SERVO_STEP=3

#夹爪电机宏定义
zhua_m1_PWMA=11
zhua_m1_AIN1=13
zhua_m1_AIN2=13

zhua_m2_PWMB=16
zhua_m2_BIN1=18
zhua_m2_BIN2=22
zhua_STBY=37    #或者直接让STBY接3V3高电平
ZHENG=1
GPIO.setup(zhua_m1_PWMA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(zhua_m1_AIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(zhua_m1_AIN2, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(zhua_m2_PWMB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(zhua_m2_BIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(zhua_m2_BIN2, GPIO.OUT, initial=GPIO.LOW)


def order_gen(spdr,dir):     #指令生成函数
    spd=hex(spdr)            
    spd=spd.replace('0x','').zfill(2)
    if(dir==FORWARD):       #前进指令
        order=M_HEADER + RIGHT_FWD + spd + RIGHT_FWD +spd + LEFT_FWD + spd + LEFT_FWD + spd +TAIL
    elif(dir==BACK):        #后退指令
        order=M_HEADER + RIGHT_BCK + spd + RIGHT_BCK +spd + LEFT_BCK + spd + LEFT_BCK + spd + TAIL
    elif(dir==TRANS_LEFT):  #向左平移  右后轮 反转  右前轮 正转  左后轮 正转  左前轮 反转  
        order=M_HEADER + RIGHT_BCK + spd + RIGHT_FWD +spd + LEFT_FWD + spd + LEFT_BCK + spd + TAIL
    elif(dir==TRANS_RIGHT): #向右平移  右后轮 正转  右前轮 反转  左后轮 反转  左前轮 正转 
        order=M_HEADER + RIGHT_FWD + spd + RIGHT_BCK +spd + LEFT_BCK + spd + LEFT_FWD + spd +TAIL
    elif(dir==LEFT_TURN):   #向左自旋  右后轮 正转  右前轮 正转  左后轮 反转  左前轮 反转  
        order=M_HEADER +  RIGHT_FWD + spd + RIGHT_FWD +spd + LEFT_BCK + spd + LEFT_BCK + spd +TAIL
    elif(dir==RIGHT_TURN):  #向右自旋  右后轮 反转  右前轮 反转  左后轮 反转  左前轮 反转 
        order=M_HEADER + RIGHT_BCK + spd + RIGHT_BCK +spd + LEFT_FWD + spd + LEFT_FWD + spd + TAIL   
    return order

def Servo_order_gen(angle,NUM):
    ANGLE=hex(angle)            
    ANGLE=ANGLE.replace('0x','').zfill(2) 
    if(NUM==SERVO1):
        s_order=S_HEADER + SMOV + ANGLE + SSTOP + S_NO + SSTOP + S_NO + SSTOP + S_NO + TAIL
    elif(NUM==SERVO2):
        s_order=S_HEADER + SSTOP + S_NO + SMOV + ANGLE + SSTOP + S_NO + SSTOP + S_NO + TAIL
    elif(NUM==SERVO3):
        s_order=S_HEADER + SSTOP + S_NO + SSTOP + S_NO + SMOV + ANGLE + SSTOP + S_NO + TAIL
    elif(NUM==SERVO4):
        s_order=S_HEADER + SSTOP + S_NO + SSTOP + S_NO + SSTOP + S_NO + SMOV + ANGLE + TAIL
    return s_order

def spd_gen(spdx):
    spd1=hex(spdx)
    spd1=spd1.replace('0x','').zfill(2) 
    return spd1




def stop(speed,state):     #停止，需要传现在的速度和行进方向，防止电机瞬间减速不稳定
    #if (speed>8 or speed<-8):  #如果当前速度过大
    od_speed=speed-5
    while (od_speed>0):

        
        if(state==FORWARD):
            od=order_gen(od_speed,FORWARD)
        else:
            od=order_gen(od_speed,BACK)
        od_speed=od_speed-5             #加5  
#        write_num=ser.write(od)
  #      time.sleep(0.3)    #等待0.3秒
        
    od=order_gen(0,BACK)           
#    write_num=ser.write(od)

        
   
    #else

def front(speed,tim):       #前进

    od=order_gen(speed,FORWARD)
    d=bytes.fromhex(od)
    #write_num=ser.write(d)          #写串口
    #time.sleep(tim)
    print(d)

def back(speed,tim):       #后退 但是传参speed 速度为正值
    od=order_gen(speed,BACK)
    d=bytes.fromhex(od)    #串口指令
    #write_num=ser.write(d)          #写串口
    #time.sleep(tim)
    print(d)

def left(speed,tim):      #向左平移
    od=order_gen(speed,TRANS_LEFT)
    d=bytes.fromhex(od)
    #write_num=ser.write(d)          #写串口
    #time.sleep(tim)
    print(d)

def right(speed,tim):  #向右平移
    od=order_gen(speed,TRANS_RIGHT)
    d=bytes.fromhex(od)
    #write_num=ser.write(d)          #写串口
    #time.sleep(tim)
    print(d)

def servo1(now,to):
    if(now>to):
        for angle in range (now,to):   #angle 表示希望转到的角度
            s_order=Servo_order_gen(angle,SERVO1)
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)
    else:
            s_order=Servo_order_gen(angle,SERVO1)
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)

    

def servo2(now,to):
    if(now>to):
        for angle in range (now,to):   # 能否为负数
            s_order=Servo_order_gen(angle,SERVO2)
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)
    else:
        for angle in range (now,to,-SERVO_STEP):   
            s_order=Servo_order_gen(angle,SERVO2)    
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)

def servo3(now,to):
    if(now>to):
        for angle in range (now,to):   #angle 表示希望转到的角度
            s_order=Servo_order_gen(angle,SERVO3)
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)
    else:
        for angle in range (now,to,-SERVO_STEP):   
            s_order=Servo_order_gen(angle,SERVO3)    
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)

def servo4(now,to):
    if(now>to):
        for angle in range (now,to):   #angle 表示希望转到的角度
            s_order=Servo_order_gen(angle,SERVO4)
            write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)
    else:
        for angle in range (now,to,-SERVO_STEP):  
            s_order=Servo_order_gen(angle,SERVO4)    
            #write_num=ser.write(s_order)          #写串口
            time.sleep(0.01)

def motor1(tim,dir):    #直接使用上位机引脚控制 ，需要确定正反转
   if(dir==ZHENG):   #AIN1 H  AIN2 L 正转 
        GPIO.output(zhua_m1_AIN1,GPIO.HIGH )
        GPIO.output(zhua_m1_AIN2,GPIO.LOW  )
        GPIO.output(zhua_m1_PWMA,GPIO.HIGH )   
   else:             #AIN1 L  AIN2 H 反转
        GPIO.output(zhua_m1_AIN1,GPIO.LOW )
        GPIO.output(zhua_m1_AIN2,GPIO.HIGH  )
        GPIO.output(zhua_m1_PWMA,GPIO.HIGH )
    

def motor2(tim,dir):
    if(dir==ZHENG):   #AIN1 H  AIN2 L 正转 
        GPIO.output(zhua_m2_BIN1,GPIO.HIGH )
        GPIO.output(zhua_m2_BIN2,GPIO.LOW  )
        GPIO.output(zhua_m2_PWMB,GPIO.HIGH )   
    else:             #AIN1 L  AIN2 H 反转
        GPIO.output(zhua_m2_BIN1,GPIO.LOW )
        GPIO.output(zhua_m2_BIN2,GPIO.HIGH )
        GPIO.output(zhua_m2_PWMB,GPIO.HIGH )

def adjust(model,cap,target):
    pass


def grasp(obj):
    pass

def main():
    #my_order=front(8,2)
    front(8,2)
    back(5,2)
    right(3,2)
    left(3,2)
    stop(20,1)



if __name__=='__main__':
    main()


        # spd=hex(od_speed)               #以每次步长为5的速度减速,直到speed-5            
        # spd=spd.replace('0x','').zfill(2) 
        #spd=spd_gen(od_speed)
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(zhua_pin1, GPIO.OUT, initial=GPIO.LOW)
    # GPIO.setup(zhua_pin2, GPIO.OUT, initial=GPIO.LOW)