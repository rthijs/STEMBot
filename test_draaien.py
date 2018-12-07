#!/usr/bin/env python3

import threading
import time

from DeVestenBot import DeVestenBot
from ev3dev2.sensor import INPUT_2
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, LargeMotor

from ev3dev2.sensor.lego import GyroSensor

gyro = GyroSensor(address=INPUT_2)
gyro.mode='GYRO-ANG'

bot = DeVestenBot()

def print_hoek():
    while(1):
        bot.log(gyro.angle)

t_print_hoek = threading.Thread(target=print_hoek)
t_print_hoek.start()


bot.log("start draaien, begin verwacht = 0 , target = 90")
bot.draai_graden(90)

bot.log("slaap 1 seconde")

time.sleep(1)

bot.log("orienteer terug naar 0°")
bot.orienteer(0)
bot.log("orienteren klaaar, verwacht nu 0° van sensor")

bot.log("slaap 1 seconde")

time.sleep(1)

bot.log("einde programma")