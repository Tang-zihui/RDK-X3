echo 8 8 8 8  > /proc/sys/kernel/printk
for i in 0 3
do
        cd /sys/class/pwm/pwmchip${i}
        echo 0 > export
        echo 1 > export
        echo 2 > export
 
        cd pwm0
        echo 10000 > period
        echo 3000  > duty_cycle
        echo 1 > enable
  
        cd ../pwm1
        echo 10000 > period
        echo 1000  > duty_cycle
        echo 1 > enable
 
        cd ../pwm2
        echo 10000 > period
        echo 1000  > duty_cycle
        echo 1 > enable
done
#以下是进行寄存器读取
echo "pwm0 pinctrl:`devmem 0xa6004010 32`"
echo "pwm1 pinctrl:`devmem 0xa6004058 32`"
echo "pwm2 pinctrl:`devmem 0xa600405C 32`"
echo "pwm3 pinctrl:`devmem 0xa6004060 32`"
echo "pwm4 pinctrl:`devmem 0xa6004064 32`"
echo "pwm5 pinctrl:`devmem 0xa6004048 32`"
echo "pwm6 pinctrl:`devmem 0xa600404C 32`"
echo "pwm7 pinctrl:`devmem 0xa6004030 32`"
echo "pwm8 pinctrl:`devmem 0xa6004034 32`"
 
echo "Regs of PWM 0 1 2:"
echo "PWM_EN      `devmem 0xA500d000 32`"
echo "PWM_SLICE   `devmem 0xA500d004 32`"
echo "PWM_FREQ    `devmem 0xA500d008 32`"
echo "PWM_FREQ1   `devmem 0xA500d00C 32`"
echo "PWM_RATIO   `devmem 0xA500d014 32`"
echo "PWM_SRCPND  `devmem 0xA500d01C 32`"
echo "PWM_INTMASK `devmem 0xA500d020 32`"
 
echo "Regs of PWM 3 4 5:"
echo "PWM_EN      `devmem 0xA500e000 32`"
echo "PWM_SLICE   `devmem 0xA500e004 32`"
echo "PWM_FREQ    `devmem 0xA500e008 32`"
echo "PWM_FREQ1   `devmem 0xA500e00C 32`"
echo "PWM_RATIO   `devmem 0xA500e014 32`"
echo "PWM_SRCPND  `devmem 0xA500e01C 32`"
echo "PWM_INTMASK `devmem 0xA500e020 32`"
