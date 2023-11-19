#!/usr/bin/env python3

from ev3bot import EV3Bot

bot = EV3Bot()

bot.spreek('Hi everybody! Welcome to the Continuum Jidoka Hackaton!')

te_rijden_afstand = bot.meet_afstand_in_cm() - 10

bot.rij_centimeters(te_rijden_afstand)

bot.spreek("oh no, I just can not go on!")

quit()