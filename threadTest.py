#!/usr/bin/env python3

import threading
import time

from DeVestenBot import DeVestenBot

bot = DeVestenBot()

def meet_afstand():
    while(1):
        if (bot.meet_afstand_in_cm() < 7):
            bot.log("OMG WE GAAN BOTSEN!")
            return True

def rij_vooruit():
    bot.log("rijden maar")
    bot.rij_centimeters(100)

thread_rijden = threading.Thread(target=rij_vooruit)

thread_rijden.start()

while(meet_afstand() == False):
    bot.log("niets aan de hand")

bot.noodstop()

time.sleep(3)

bot.grijper_sluit()
bot.grijper_open()
bot.grijper_sluit()
bot.grijper_open()

bot.rij_centimeters(-50)

bot.draai_links()
bot.draai_links()

bot.rij_centimeters(50)