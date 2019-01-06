#!/usr/bin/env python3

from DeVestenBot import DeVestenBot

bot = DeVestenBot()

for _ in range(4):
    bot.rij_centimeters(20)
    bot.grijper_sluit()
    bot.grijper_open()
    bot.draai_graden_geen_gyro(-90)

bot.exit_program()