#!/usr/bin/env python3

from DeVestenBot import DeVestenBot
import socket, time, json

bot = DeVestenBot()

for _ in range(4):
    bot.log("rij 10 centimeter")
    bot.rij_centimeters(10)
    bot.log("draai links")
    bot.draai_links()