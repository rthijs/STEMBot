#!/usr/bin/env python3

from ev3bot import EV3Bot

bot = EV3Bot()

te_rijden_afstand = bot.meet_afstand_in_cm() - 10

bot.rij_centimeters(te_rijden_afstand)