#!/usr/bin/env python3

import sys, threading, time

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveTank, Motor)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4


class DeVestenBot():
    '''Basisklasse voor de robot van De Vesten'''

    def __init__(self):
        # motors
        self.motor_links_poort = OUTPUT_B
        self.motor_rechts_poort = OUTPUT_C
        self.motor_links = LargeMotor(self.motor_links_poort)
        self.motor_rechts = LargeMotor(self.motor_rechts_poort)

        # sensors
        self.gyro = GyroSensor(address=INPUT_2)

    #
    # Helper functies
    #

    def log(self, text_to_print):
        '''print output naar console in VSCode'''
        print(text_to_print, file=sys.stderr)

    #
    # Functies ivm rijden
    #

    def rij_centimeters(self, centimeters):
        '''
        geef het aantal centimeters dat de bot moet rijden

        de wielen hebben een diameter van 5,6 cm
        een volledige rotatie is daarom 5,6 * PI cm = 17,5929188601 cm
        Een rotatie van 1° komt overeen met 17,5929188601 cm / 360° = 0,048869219 cm
        om 1 cm te rijden moeten we dus 20,462778421° draaien, helaas heeft de motor
        maar een precisie van 1° dus er zal een afwijking zijn.

        De bot zal rijden op een kwart van de maximale snelheid
        '''
        afwijking = 1.02 #correctiefactor, experimenteel te bepalen.
        hoek_voor_een_cm = 20.462778421
        graden = centimeters * hoek_voor_een_cm * afwijking
        robot_tank_drive = MoveTank(left_motor_port=self.motor_links_poort, right_motor_port=self.motor_rechts_poort)

        robot_tank_drive.on_for_degrees(left_speed=25, right_speed=25, degrees=graden)

    def noodstop(self):
        '''
        Gebruik deze functie als je wil dat de robot stopt. Elke actie op de wielen die nog bezig is wordt afgesloten
        en de robot zal remmen, dit wil zeggen dat hij niet uitbolt maar actief zal proberen te stoppen.
        '''
        self.log("### (noodstop)")
        self.motor_links.stop(stop_action='brake')
        self.motor_rechts.stop(stop_action='brake')

    #
    # Functies ivm draaien
    #

    def orienteer(self,richting):
        '''
        Draai de robot naar de gegeven richting. Bij de start van het programma is recht vooruit 0°.
        Deze functie is handig als de robot al veel draaibewegingen heeft moeten maken, deze hebben telkens
        een kleine afwijking, met deze functie kan je heroriënteren. Deze functie heeft een maximale afwijking
        van ongeveer 3° (experimenteel bepaald, afwijking meestal door overshoot in de draairichting.)
        '''
        huidige_orientatie = self.gyro.angle
        wijzerzin = 1
        tegenwijzerzin = -1
        rotatiesnelheid = 50

        self.log("### (orienteer) orienteer naar: " + str(richting) +  ", huidige orientatie = " + str(huidige_orientatie))

        def roteer(self, zin):
            self.motor_links.run_forever(speed_sp=rotatiesnelheid * zin, stop_action='brake')
            self.motor_rechts.run_forever(speed_sp=-rotatiesnelheid * zin, stop_action='brake')

        if(richting < huidige_orientatie):
            #draai tegenwijzerzin
            self.log("### (orienteer) roteer tegenwijzerzin")
            t_roteren = threading.Thread(target=roteer, args=[self,tegenwijzerzin])
            t_roteren.start()
            while(richting < self.gyro.angle):
                self.log("### (orienteer) : " + str(richting) +" < " + str(self.gyro.angle))
                pass
            self.log("### (orienteer) noodstop")
            self.noodstop()
        else:
            #draai wijzerzin
            self.log("### (orienteer) roteer wijzerzin")
            t_roteren = threading.Thread(target=roteer, args=[self,wijzerzin])
            t_roteren.start()
            while(richting > self.gyro.angle):
                self.log("### (orienteer) : " + str(richting) +" > " + str(self.gyro.angle))
                pass
            self.log("### (orienteer) noodstop")
            self.noodstop()

    def orienteer_noord(self):
        ''' Draai de robot zodat hij dezelfde orientatie krijgt als toen het programma startte.'''
        self.orienteer(0)    
    
    def orienteer_oost(self):
        '''Orienteer de robot 90° rechts ten opzichte van de orientatie bij het begin van het programma.'''
        self.orienteer(90) 
    
    def orienteer_zuid(self):
        '''Orienteer de robot 180° ten opzichte van de orientatie bij het begin van het programma.'''
        self.orienteer(180) 
    
    def orienteer_west(self):
        '''Orienteer de robot 90° links ten opzichte van de orientatie bij het begin van het programma.'''
        self.orienteer(-90)

    def draai_graden(self, graden):
        '''
        Roteer de robot het gegeven aantal graden. Een kleine afwijking is te verwachten, de robot roteert
        vaak 2 à 3° te ver. Gebruik negatieve graden om naar links te draaien. Gebruik een van de orienteer_*-functies
        om een opeenstapeling van afwijkingen te vermijden.
        '''
        huidige_orientatie = self.gyro.angle
        doel_orientatie = huidige_orientatie + graden

        self.log("### (draai_graden) orienteer naar: " + str(doel_orientatie))

        self.orienteer(doel_orientatie)

    def draai_links(self):
        '''Draai de robot 90° naar links, een kleine afwijking (tot 3°) is mogelijk, meestal door overshoot.'''
        self.draai_graden(-90)

    def draai_rechts(self):
        '''Draai de robot 90° naar rechts, een kleine afwijking (tot 3°) is mogelijk, meestal door overshoot.'''
        self.draai_graden(90)

    def keer_om(self):
        '''Draai de robot 180° naar rechts, een kleine afwijking (tot 3°) is mogelijk, meestal door overshoot.'''
        self.draai_graden(180)

    #
    # Functies ivm de grijper
    #

    def grijper_open(self):
        '''Zet de grijper omhoog.'''
        motor_grijper=MediumMotor(OUTPUT_A)
        motor_grijper.on_for_degrees(degrees=180,speed=50)
        motor_grijper.off()

    def grijper_sluit(self):
        '''Doe de grijper omlaag.'''
        motor_grijper=MediumMotor(OUTPUT_A)
        motor_grijper.on_for_degrees(degrees=-180,speed=50)
        motor_grijper.off()

    #
    # Functies ivm de sensoren
    #

    # Ultrasoon

    def meet_afstand_in_cm(self):
        sensor = UltrasonicSensor(INPUT_4)
        afstand = sensor.distance_centimeters
        print("gemeten afstand in cm: " + str(sensor.distance_centimeters), file=sys.stderr)
        return afstand
        
    # Gyroscoop

    # Druksensor

    # Kleursensor