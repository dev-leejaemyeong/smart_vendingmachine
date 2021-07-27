import drivers
from time import sleep
import smbus
import RPi.GPIO as GPIO
import threading
import socket

display = drivers.Lcd()
bus = smbus.SMBus(1)  # I2C 1
add = 0x48  #PCF8591 주소값
num=0
flagggg = False
#led_pin =17

servo_pin = 20# 스프라이트 
servo_pin2 = 19 # 펩시 
servo_pin3 = 22 # 코카콜라

button_pin = 27 # 스프라이트 
button_pin2 = 16# 펩시 
button_pin3 = 25 # 코카콜라 

sprite_pin= 12# led
pepsi_pin= 6
coke_pin= 5

analog =0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('220.69.249.219', 8100))


GPIO.setmode(GPIO.BCM)
buttonInput=0 # 스프라이트 버튼
buttonInput2=0
buttonInput3=0
#----------------------------------
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(button_pin2, GPIO.IN)
GPIO.setup(button_pin3, GPIO.IN)

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)
GPIO.setup(servo_pin3, GPIO.OUT)

GPIO.setup(sprite_pin, GPIO.OUT)
GPIO.setup(pepsi_pin, GPIO.OUT)
GPIO.setup(coke_pin, GPIO.OUT)


#servo===========================
pwm = GPIO.PWM(servo_pin, 50) # 50Hz
pwm.start(2.5) # 0.6ms


pwm.ChangeDutyCycle(3.5)
sleep(1.0)
GPIO.setup(servo_pin, GPIO.IN)


pwm2 = GPIO.PWM(servo_pin2, 50) # 50Hz
pwm2.start(2.5) # 0.6ms

pwm2.ChangeDutyCycle(3.5)
sleep(1.0)
GPIO.setup(servo_pin2, GPIO.IN)


pwm3 = GPIO.PWM(servo_pin3, 50) # 50Hz
pwm3.start(2.5) # 0.6ms

pwm3.ChangeDutyCycle(3.5)
sleep(1.0)


sleep(1.0)


GPIO.setup(servo_pin3, GPIO.IN)
#===============================


def servo_angle(degree):
    num1 = (degree * 0.055555555555556)+2.5
    pwm.ChangeDutyCycle(num1)
    time.sleep(1.0)

#----------------------------------

#GPIO.setup(led_pin, GPIO.OUT, initial=True); # pinmode

def t1_main():
    while True:
       pass

#t1 = threading.Thread(target=t1_main)
#t1.start()
# Main body of code
display.lcd_display_string("  Please insert", 1)
display.lcd_display_string("      coin", 2)

GPIO.output(sprite_pin,True)
GPIO.output(pepsi_pin,True)
GPIO.output(coke_pin,True)
try:
    while True:

        bus.write_byte(add, 0x00)  # 0번째 아날로그핀 값을 읽도록 설정 (ADC start)
        sleep(0.05)           # ADC 완료까지 대기
        if flagggg==False:
            bus.read_byte(add)
            flagggg=True
            continue
        analog = bus.read_byte(add)
        sleep(0.05)
        print(analog)
        if(analog>200):
            display.lcd_clear()
            num=num+100
            display.lcd_display_string("you insert coin", 1)
            display.lcd_display_string("     "+str(num)+"won", 2)
            
            
        if(num == 300):
            
            while(buttonInput == 0 and buttonInput2 == 0 and buttonInput3 == 0):
                buttonInput = GPIO.input(button_pin)
                buttonInput2 = GPIO.input(button_pin2)
                buttonInput3 = GPIO.input(button_pin3)
                
                print("1 button : "+ str(buttonInput))
                print("2 button : "+ str(buttonInput2))
                print("3 button : "+ str(buttonInput3))
                sleep(0.5)
                
                if buttonInput == 1: # 스프라이트일때
                    GPIO.setup(servo_pin, GPIO.OUT)
                    
                    GPIO.setup(sprite_pin, GPIO.OUT)
                    GPIO.setup(pepsi_pin, GPIO.IN)
                    GPIO.setup(coke_pin, GPIO.IN)
                    
                    GPIO.output(servo_pin, buttonInput)
                    #print("push!!")
                    s.send("s".encode())
                    display.lcd_clear()
                    display.lcd_display_string("You select sprite!", 2)
                    #sleep(1.0)
                    pwm.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    pwm.ChangeDutyCycle(4.5)
                    sleep(1.0)
                    pwm.ChangeDutyCycle(5.5)
                    sleep(1.0)
                    pwm.ChangeDutyCycle(6.5)
                    sleep(1.0)
#                     pwm.ChangeDutyCycle(7.2)
#                     sleep(1.0)
               
                    pwm.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    GPIO.setup(servo_pin, GPIO.IN)

                    num =0
                    buttonInput =0
                    
                    GPIO.setup(sprite_pin, GPIO.OUT)
                    GPIO.setup(pepsi_pin, GPIO.OUT)
                    GPIO.setup(coke_pin, GPIO.OUT)
                    
                    display.lcd_clear()
                    display.lcd_display_string("  Please insert", 1)
                    display.lcd_display_string("      coin", 2)
                    flagggg=False
                    break
                
            #while(buttonInput2 == 0):
                
                if buttonInput2 == 1: # 펩시 일때
                    GPIO.setup(servo_pin2, GPIO.OUT)
                    
                    GPIO.setup(sprite_pin, GPIO.IN)
                    GPIO.setup(pepsi_pin, GPIO.OUT)
                    GPIO.setup(coke_pin, GPIO.IN)
                    
                    GPIO.output(servo_pin2, buttonInput2)
                    #print("push!!")
                    s.send("p".encode())
                    display.lcd_clear()
                    display.lcd_display_string("You select pepsi!", 2)
                    #sleep(1.0)
                    pwm2.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    pwm2.ChangeDutyCycle(4.5)
                    sleep(1.0)
                    pwm2.ChangeDutyCycle(5.5)
                    sleep(1.0)
                    pwm2.ChangeDutyCycle(6.5)
                    sleep(1.0)
#                     pwm.ChangeDutyCycle(7.2)
#                     sleep(1.0)
               
                    pwm2.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    GPIO.setup(servo_pin2, GPIO.IN)

                    
                    flagggg=False
                    num =0
                    buttonInput2 =0
                    GPIO.setup(sprite_pin, GPIO.OUT)
                    GPIO.setup(pepsi_pin, GPIO.OUT)
                    GPIO.setup(coke_pin, GPIO.OUT)
                    display.lcd_clear()
                    display.lcd_display_string("  Please insert", 1)
                    display.lcd_display_string("      coin", 2)
                    break
            #while(buttonInput3 ==0):
                
                if buttonInput3 == 1: # 코카라 일때
                    GPIO.setup(servo_pin3, GPIO.OUT)

                    GPIO.setup(sprite_pin, GPIO.IN)
                    GPIO.setup(pepsi_pin, GPIO.IN)
                    GPIO.setup(coke_pin, GPIO.OUT)

                    GPIO.output(servo_pin3, buttonInput3)
                    #print("push!!")
                    s.send("c".encode())
                    display.lcd_clear()
                    display.lcd_display_string("You select coke!", 2)
                    pwm3.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    pwm3.ChangeDutyCycle(4.5)
                    sleep(1.0)
                    pwm3.ChangeDutyCycle(5.5)
                    sleep(1.0)
                    pwm3.ChangeDutyCycle(6.5)
                    sleep(1.0)
#                     pwm.ChangeDutyCycle(7.2)
#                     sleep(1.0)
               
                    pwm3.ChangeDutyCycle(3.5)
                    sleep(1.0)
                    GPIO.setup(servo_pin3, GPIO.IN)

                    flagggg=False
                    num =0
                    buttonInput3 =0
                    
                    GPIO.setup(sprite_pin, GPIO.OUT)
                    GPIO.setup(pepsi_pin, GPIO.OUT)
                    GPIO.setup(coke_pin, GPIO.OUT)
                    
                    display.lcd_clear()
                    display.lcd_display_string("  Please insert", 1)
                    display.lcd_display_string("      coin", 2)
                    break
                                          
finally:
    display.lcd_clear()
    GPIO.cleanup()
 
    print("clean!!")