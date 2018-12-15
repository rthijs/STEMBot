#!/usr/bin/env python3

import sys, threading, time, collections

from ev3dev2.motor import (OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor,
                           MediumMotor, MoveTank, Motor)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2 import sound


class DeVestenBot():
    '''Basisklasse voor de robot van De Vesten'''

    def __init__(self):
        # motors
        self.motor_links_poort = OUTPUT_B
        self.motor_rechts_poort = OUTPUT_C
        self.motor_links = LargeMotor(self.motor_links_poort)
        self.motor_rechts = LargeMotor(self.motor_rechts_poort)
        self.geluid = sound.Sound()

        # sensors
        self.gyro = GyroSensor(address=INPUT_2)
        self.touch = TouchSensor(address=INPUT_1)
        self.kleur = ColorSensor(address=INPUT_3)

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

    def rij_tot_kleur_gelijk_aan(self,kleur):
        '''
        Rijdt rechtdoor tot de gegeven kleur herkent wordt.

        .. code:: python

            bot.rij_tot_kleur_gelijk_aan(bot.kleur.COLOR_RED)

        '''
        def _rij(self):
            self.log("### in _rij: run forever")
            robot_tank_drive = MoveTank(left_motor_port=self.motor_links_poort, right_motor_port=self.motor_rechts_poort)
            robot_tank_drive.on(left_speed=50, right_speed=50)

        t_rij = threading.Thread(target=_rij, args=(self,))
        t_rij.start()

        while self.get_kleur() != kleur:
            self.log(str(self.get_kleur()))
            pass
        
        self.noodstop()

    def rij_tot_kleur_verschillend_van(self,kleur):
        '''
        Rij rechtdoor tot de gegeven kleur niet meer gemeten wordt.

        .. code:: python

            bot.rij_tot_kleur_verschillend_van(bot.kleur.COLOR_RED)

        '''
        def _rij(self):
            self.log("### in _rij: run forever")
            robot_tank_drive = MoveTank(left_motor_port=self.motor_links_poort, right_motor_port=self.motor_rechts_poort)
            robot_tank_drive.on(left_speed=50, right_speed=50)

        t_rij = threading.Thread(target=_rij, args=(self,))
        t_rij.start()

        while self.get_kleur() == kleur:
            self.log(str(self.get_kleur()))
            pass
        
        self.noodstop()

    #
    # Functies ivm draaien
    #

    def draai_graden(self,graden):
        '''
        Draai de robot het gegeven aantal graden.

        Deze functie gebruikt de gyro-sensor en omdat deze nogal traag is en neiging heeft tot driften is deze functie
        nogal complex. De robot zal eerst trachten het correcte aantal graden te draaien, vervolgens wachten tot de gyro
        een stabiele uitlezing geeft en daarna een eventuele correctie toepassen. Moest de gyro beginnen driften zal de
        uitlezing gestopt worden na 1 seconde, de afwijking in dat geval is enkele graden (ongeveer 3).

        Let op dat de afwijking cumulatief is, hoe meer gedraai hoe groter de afwijking, vooral als er veel in dezelfde
        richting gedraaid wordt.
        '''
        # deze waarden kan je tunen
        SNELHEID_HOOG = 100
        SNELHEID_LAAG = 40
        MAX_GYRO_METING_ITERATIES = 10 #als de gyro begint te driften duurt het eeuwig, stop daarom na 10 metingreeksen (1 seconde)

        # deze niet veranderen
        WIJZERZIN = 1
        TEGENWIJZERZIN = -1

        def _wacht_tot_gyro_meting_stabiel():

            def _gyro_stabiel(metingen):

                def _meting_volledig():
                    if len(metingen) == 10:
                        return True
                    else:
                        return False

                def _10_metingen_gelijk():
                    self.log(str(meting_ring))
                    for i in range(1,10):
                        if metingen[i] != metingen[0]:
                            return False
                    return True

                if _meting_volledig():
                    return _10_metingen_gelijk()
                else:
                    return False

            meting_ring = collections.deque(maxlen=10)
            iteraties = 0

            while _gyro_stabiel(meting_ring) == False:
                if iteraties >= MAX_GYRO_METING_ITERATIES:
                    break
                meting_ring.append(self.gyro.angle)
                iteraties = iteraties + 1
                time.sleep(0.1)

        def _roteer_robot_graden(hoek,snelheid):

            def _reset_gyro():
                self.gyro.mode = self.gyro.MODE_GYRO_RATE
                _wacht_tot_gyro_meting_stabiel()
                self.gyro.mode = self.gyro.MODE_GYRO_ANG
                _wacht_tot_gyro_meting_stabiel()

            def _get_rotatie_zin(graden):
                if graden > 0:
                    return WIJZERZIN
                return TEGENWIJZERZIN

            def _wacht_tot_gewenste_hoek_bereikt(hoek):

                def _blijf_draaien(graden):
                    if _get_rotatie_zin(graden) == WIJZERZIN:
                        if self.gyro.angle < graden:
                            return True
                    else:
                        if self.gyro.angle > graden:
                            return True
                    return False

                while _blijf_draaien(hoek):
                    self.log(str(self.gyro.angle))
                    pass

            def _draai_robot_in_thread(zin, snelheid):

                def _draai_robot(zin, snelheid):
                    self.motor_links.run_forever(speed_sp=snelheid * zin, stop_action='brake')
                    self.motor_rechts.run_forever(speed_sp=-snelheid * zin, stop_action='brake')

                t_draaien = threading.Thread(target=_draai_robot, args=(zin,snelheid))
                t_draaien.start()

            _reset_gyro()
            _draai_robot_in_thread(_get_rotatie_zin(hoek),snelheid)
            _wacht_tot_gewenste_hoek_bereikt(hoek)
            self.noodstop()

        def _corrigeer_overshot():
            _wacht_tot_gyro_meting_stabiel()
            overshoot_correctie = graden - self.gyro.angle
            _roteer_robot_graden(overshoot_correctie,SNELHEID_LAAG)       

        _roteer_robot_graden(graden,SNELHEID_HOOG)
        _corrigeer_overshot()

    def draai_graden_geen_gyro(self, graden):
        '''
        Gebruik deze functie om de robot te draaien zonder gebruik te maken van de gyro-sensor. Afhankelijk
        van de robot en sensor kan dit nauwkeuriger zijn, geef het aantal graden dat de robot moet draaien, 
        wijzerzin is positief.

        De robot heeft een breedte van 15cm,  maar we nemen het midden van de wielen als de buitenste maat voor 
        de cirkel die we gebruiken in de berekening. Een wiel is 2,8cm breed, 2 halve wielen aftrekken van 15cm 
        geeft 12,2cm. Voor een volledige draai van 360° moet elk wiel dus 12,2*PI (= 38,3274303738) cm  rijden 
        in tegengestelde zin. 1° draaien is dus 0,106465084 cm voor elk wiel en dat komt overeen met 2,178571423° 
        wielrotatie
        '''
        wielrotatie_per_graad = 2.178571423
        correctiefactor = 1.00
        wielrotatie = wielrotatie_per_graad * graden * correctiefactor
        wielrotatie_links = wielrotatie
        wielrotatie_rechts = wielrotatie * -1
        self.motor_links.run_to_rel_pos(position_sp=wielrotatie_links, stop_action="hold", speed_sp=75)
        self.motor_rechts.run_to_rel_pos(position_sp=wielrotatie_rechts, stop_action="hold", speed_sp=75)
        self.motor_links.wait_while('running')
        self.motor_rechts.wait_while('running')

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

    # Druksensor

    def is_druksensor_ingedrukt(self):
        '''antwoord met True als de sensor ingedrukt is, anders False'''
        return self.touch.is_pressed

    # Kleursensor

    def get_kleur(self):
        return self.kleur.color

    #
    # Functies voor output die de robot kan doen
    #

    # Console logging (remote)

    def log(self, text_to_print):
        '''print output naar console in VSCode'''
        print(text_to_print, file=sys.stderr)

    # Scherm

    # TODO

    # Geluid

    def spreek(self, zin, wacht=False):
        '''
        Text to speech, geef de zin die de robot moet zeggen als parameter.
        Deze functie werkt assynchroon dus de robot gaat verder met zijn anderen handelingen
        terwijl hij spreekt. Wil je die niet gebruik dan "wacht=True".
        '''
        def _spreek():
            self.geluid.speak(zin)

        if (wacht):
            _spreek().wait()
        else:
            _spreek()

    def speel(self, wav, wacht=False):
        '''
        Speel een wav file. Deze functie is asynchroon, wil je dat je robot wacht tot het geluid klaar is met spelen
        gebruik dan "wacht=True". 
        
        Let er op dat de file niet te groot is, het duurt dan langer om je programma
        te starten (bij elke start van een script worden alle files geupload naar de robot) en het geheugen
        is beperkt. Met Audacity kan je 16 bit mono wavs maken.
        '''
        def _speel():
            self.geluid.play(wav)

        if (wacht):
            _speel().wait()
        else:
            _speel().play(wav)

   #
   # Ev3dev ondersteunt nog veel meer manieren om je robot geluid te laten maken, zo is er bv nog de mogelijkheid om beepjes
   # te maken, noten op de juiste toon en met de gewenste duur te spelen en zelfs hele muziekstukken. Moest dit je interesseren
   # kan dit een leuke oefening zijn om zelf een functie te implementeren die dit toestaat. De help tekst van de Sound library
   # kan je op weg helpen.
   #