#!/usr/bin/env python3

import sys

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveTank, Motor)
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4


class DeVestenBot():
    '''Basisklasse voor de robot van De Vesten'''

    def __init__(self):
        self.motor_links_poort = OUTPUT_B
        self.motor_rechts_poort = OUTPUT_C
        self.motor_links = LargeMotor(self.motor_links_poort)
        self.motor_rechts = LargeMotor(self.motor_rechts_poort)

    def log(self, text_to_print):
        '''print output naar console in VSCode'''
        print(text_to_print, file=sys.stderr)

    def rij_centimeters(self, centimeters):
        '''
        geef het aantal centimeters dat de bot moet rijden

        de wielen hebben een diameter van 5,6 cm
        een volledige rotatie is daarom 5,6 * PI cm = 17,5929188601 cm
        Een rotatie van 1° komt overeen met 17,5929188601 cm / 360° = 0,048869219 cm
        om 1 cm te rijden moeten we dus 20,462778421° draaien, helaas heeft de motor
        maar een precisie van 1° dus er zal een afwijking zijn.

        De bot zal rijden op halve snelheid
        '''
        afwijking = 1.02 #correctiefactor, experimenteel te bepalen.
        hoek_voor_een_cm = 20.462778421
        graden = centimeters * hoek_voor_een_cm * afwijking
        robot_tank_drive = MoveTank(left_motor_port=self.motor_links_poort, right_motor_port=self.motor_rechts_poort)

        robot_tank_drive.on_for_degrees(left_speed=25, right_speed=25, degrees=graden)

    def noodstop(self):
        self.motor_links.stop(stop_action='brake')
        self.motor_rechts.stop(stop_action='brake')

    def draai_graden(self, graden):
        '''
        aantal graden dat de robot moet draaien, wijzerzin is positief.

        De robot draait om zijn as met deze functie. De robot heeft een breedte van 15cm,
        maar we nemen het midden van de wielen als de buitenste maat voor de cirkel die we gebruiken 
        in de berekening. Een wiel is 2,8cm breed, 2 halve wielen aftrekken van 15cm geeft 12,2cm.

        Voor een volledige draai van 360° moet elk wiel dus 12,2*PI (= 38,3274303738) cm  rijden in tegengestelde zin.
        1° draaien is dus 0,106465084 cm voor elk wiel en dat komt overeen met 2,178571423° wielrotatie
        '''
        wielrotatie_per_graad = 2.178571423
        wielrotatie = wielrotatie_per_graad * graden
        wielrotatie_links = wielrotatie
        wielrotatie_rechts = wielrotatie * -1

        self.motor_links.run_to_rel_pos(position_sp=wielrotatie_links, stop_action="hold", speed=25)
        self.motor_rechts.run_to_rel_pos(position_sp=wielrotatie_rechts, stop_action="hold", speed=25)

        self.motor_links.wait_while('running')
        self.motor_rechts.wait_while('running')

    def draai_links(self):
        self.draai_graden(-90)

    def draai_rechts(self):
        self.draai_graden(90)

    def keer_om(self):
        self.draai_graden(180)

    def grijper_open(self):
        motor_grijper=MediumMotor(OUTPUT_A)
        motor_grijper.on_for_degrees(degrees=180,speed=50)
        motor_grijper.off()

    def grijper_sluit(self):
        motor_grijper=MediumMotor(OUTPUT_A)
        motor_grijper.on_for_degrees(degrees=-180,speed=50)
        motor_grijper.off()

    def meet_afstand_in_cm(self):
        sensor = UltrasonicSensor(INPUT_4)
        afstand = sensor.distance_centimeters
        print("gemeten afstand in cm: " + str(sensor.distance_centimeters), file=sys.stderr)
        return afstand
        