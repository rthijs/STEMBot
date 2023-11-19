#!/usr/bin/env python3

from ev3bot import EV3Bot

bot = EV3Bot()

def rijd_n_hoek(aantal_hoeken= 4, lengte_zijde=25):
    hoek = (aantal_hoeken -2) * 180 / aantal_hoeken
    for _ in range(aantal_hoeken):
        bot.rij_centimeters(lengte_zijde)
        bot.draai_graden(hoek)
        
rijd_n_hoek() #default is vierkant
