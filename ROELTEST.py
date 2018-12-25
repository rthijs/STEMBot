#!/usr/bin/env python3

from DeVestenBot import DeVestenBot
import socket, time, json

bot = DeVestenBot()

for _ in range(4):
    bot.rij_centimeters(20)
    bot.draai_links()