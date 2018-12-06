#!/usr/bin/env python3

from DeVestenBot import DeVestenBot

bot = DeVestenBot()

afstand = bot.meet_afstand_in_cm()

bot.rij_centimeters(afstand)

bot.log("grijper sluiten")

bot.grijper_sluit()

bot.rij_centimeters(-20)

bot.log("grijper open")

bot.grijper_open()

bot.rij_centimeters(-20)