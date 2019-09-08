import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import time
import datetime
import subprocess
import threading
from gpiozero import MCP3204
import os
import pickle
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(14, GPIO.OUT)

global beep, yn_txt, temp, step, menu_txt, menu_step, setting_step, setting_txt, yn_step
step = 0
menu_txt=["back","setting","infomation","shutdown","reboot"," "]
menu_step = 0
setting_txt=["back","beep","temp","save","load","delete","reset"," "]
setting_step = 0
temp = 0
beep = 0
yn_txt = ["YES","NO","CANCEL"," "]
yn_step = 0

def load():
    global beep, temp
    if os.path.exists("/home/pi/var.txt"):
        txt = open("/home/pi/var.txt", "rb")
        load = pickle.load(txt)
        beep = load[0]
        temp = load[1]
        txt.close()
        return 0
    else:
        return 1

class menu():
    def __init__(*null):
        global step, setting_txt, menu_txt, setting_step, menu_step, yn_step, yn_txt
        lcd.clear()
        if step == 1:
             lcd.message(">" + menu_txt[menu_step] + "\n " + menu_txt[menu_step + 1])
        elif step == 2:
            lcd.message(">" + setting_txt[setting_step] + "\n " + setting_txt[setting_step + 1])
        elif step == 3:
            lcd.message(">" + yn_txt[yn_step] + "\n " + yn_txt[yn_step + 1])
    def up(*null):
        global menu_step, setting_step, step, yn_step
        if step == 1:
            if menu_step == 0:
                pass
            else:
                menu_step = menu_step - 1
                menu()
        elif step == 2:
            if setting_step == 0:
                pass
            else:
                setting_step = setting_step - 1
                menu()
        elif step == 3:
            if yn_step == 0:
                pass
            else:
                yn_step = yn_step - 1
                menu()
    def down(*null):
        global menu_step, setting_step, step, yn_step
        if step == 1:
            if menu_step == len(menu_txt) - 2:
                pass
            else:
                menu_step = menu_step + 1
                menu()
        elif step == 2:
            if setting_step == len(setting_txt) - 2:
                pass
            else:
                setting_step = setting_step + 1
                menu()
        elif step == 3:
            if yn_step == len(yn_txt) - 2:
                pass
            else:
                yn_step = yn_step + 1
                menu()
    def enter(*null):
        global temp, menu_step, step, setting_step, beep, yn_step
        if step == 1:
            if menu_txt[menu_step] == "back":
                lcd.clear()
                step=0
            elif menu_txt[menu_step] == "setting":
                lcd.clear()
                step=2
                menu()
            elif menu_txt[menu_step] == "shutdown":
                lcd.clear()
                subprocess.Popen(["/home/pi/shutdown.sh"], shell=True)
            elif menu_txt[menu_step] == "reboot":
                lcd.clear()
                subprocess.Popen(["/home/pi/reboot.sh"], shell=True)
            elif menu_txt[menu_step] == "infomation":
                lcd.clear()
                info=["beep="+str(beep),"temp="+str(temp)]
                for i in range(len(info)):
                    lcd.clear()
                    lcd.message(info[i])
                    time.sleep(1)
                menu()
            else:
                pass
        elif step == 2:
            if setting_txt[setting_step] == "back":
                step=1
                menu()
            elif setting_txt[setting_step] == "beep":
                step=3
                menu()
            elif setting_txt[setting_step] == "save":
                lcd.clear()
                lcd.message("saving...")
                if os.path.exists("/home/pi/var.txt"):
                    os.remove("/home/pi/var.txt")
                txt = open("/home/pi/var.txt", "wb")
                pickle.dump([beep, temp], txt)
                lcd.clear()
                lcd.message("saving...OK")
                time.sleep(1)
                txt.close()
                menu()
            elif setting_txt[setting_step] == "load":
                lcd.clear()
                lcd.message("loading...")
                if load() == 0:
                    lcd.clear()
                    lcd.message("loading...OK")
                else:
                    lcd.clear()
                    lcd.message("loading...error")
                time.sleep(1)
                menu()
            elif setting_txt[setting_step] == "delete":
                lcd.clear()
                lcd.message("removeing...")
                if os.path.exists("/home/pi/var.txt"):
                    os.remove("/home/pi/var.txt")
                    lcd.clear()
                    lcd.message("removing...OK")
                else:
                    lcd.clear()
                    lcd.message("removing...error")
                time.sleep(1)
                menu()
            elif setting_txt[setting_step] == "reset":
                lcd.clear()
                lcd.message("removing...")
                if os.path.exists("/home/pi/var.txt"):
                    os.remove("/home/pi/var.txt")
                    lcd.clear()
                    lcd.message("removing...OK")
                else:
                    lcd.clear()
                    lcd.message("removing...error")
                time.sleep(1)
                lcd.clear()
                lcd.message("reseting...")
                beep=1
                lcd.clear()
                lcd.message("reseting...OK")
                time.sleep(1)
                menu()
            elif setting_txt[setting_step] == "temp":
                step=3
                menu()
            else:
                pass
        elif step == 3:
            if yn_txt[yn_step] == "YES":
                if setting_txt[setting_step] == "beep":
                    beep=1
                    step=2
                    menu()
                elif setting_txt[setting_step] == "temp":
                    temp=1
                    step=2
                    menu()
                else:
                    pass
            elif yn_txt[yn_step] == "NO":
                if setting_txt[setting_step] == "beep":
                    beep=0
                    step=2
                    menu()
                elif setting_txt[setting_step] == "temp":
                    temp=0
                    step=2
                    menu()
                else:
                    pass
            elif yn_txt[yn_step] == "CANCEL":
                if setting_txt[setting_step] == "beep":
                    step=2
                    menu()
                elif setting_txt[setting_step] == "temp":
                    step=2
                    menu()
                else:
                    pass

def main():
    global temp
    while 1:
        def get_adc():
            ret = MCP3204(channel=0).value
            return ret
        if step == 1:
            pass
        elif step == 2:
            pass
        elif step == 3:
            pass
        else:
            lcd.clear()
            msg = ""
            dt = datetime.datetime.now()
            msg = str(dt.year) + "/" + str(dt.month) + "/" + str(dt.day) + " " + str(dt.hour) +":" + str(dt.minute)
            if temp == 1:
                t0=(get_adc()*3.3/1024-0.5)/0.01*-1
                msg = msg + "\nTemp:" + str(t0) + "C'"
            lcd.message(msg)
        time.sleep(0.5)

def bp():
    GPIO.output(19, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(19, GPIO.LOW)

def SW1(null):
    global step
    print("sw1")
    if beep == 1:
        bp()
    if step == 0:
        step=1
        menu()
    elif step == 1:
        menu.enter()
    elif step == 2:
        menu.enter()
    elif step == 3:
        menu.enter()
def SW2(null):
    global step
    print("sw2")
    if beep == 1:
        bp()
    if step == 0:
        step=1
        menu()
    elif step == 1:
        menu.down()
    elif step == 2:
        menu.down()
    elif step == 3:
        menu.down()
def SW3(null):
    global step
    print("sw3")
    if beep == 1:
        bp()
    if step == 0:
        step=1
        menu()
    elif step == 1:
        menu.up()
    elif step == 2:
        menu.up()
    elif step == 3:
        menu.up()

def bp2(argv):
    if argv == "start":
        GPIO.output(19, GPIO.HIGH)
    else:
        GPIO.output(19, GPIO.LOW)

def rain(null):
    print("rain")
#    net.sendall(b'rain')
    for i in range(5):
        bp2("start")
        GPIO.output(14, 1)
        time.sleep(0.5)
        GPIO.output(14, 0)
        bp2("stop")

GPIO.add_event_detect(26, GPIO.RISING, callback=rain, bouncetime=100)
GPIO.add_event_detect(16, GPIO.RISING, callback=SW3, bouncetime=150)
GPIO.add_event_detect(20, GPIO.RISING, callback=SW2, bouncetime=150)
GPIO.add_event_detect(21, GPIO.RISING, callback=SW1, bouncetime=150)

lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 3
lcd_columns   = 16
lcd_rows      = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.clear()
lcd.message("HELLO!!\nstarting...")
lcd.set_backlight(0)
load()
lcd.clear()
lcd.message("HELLO!!\nstarting...OK")
time.sleep(0.5)
#net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#net.connect(("192.168.42.1", 49152))
try:
    main()
#    while 1:
#        pass
except KeyboardInterrupt:
    lcd.clear()
    lcd.set_backlight(1)
    GPIO.cleanup()
except:
    lcd.clear()
    lcd.message("starting safemode...")
