#!/usr/bin/env python3

import threading

from ev3dev2.motor import (
    OUTPUT_B,
    OUTPUT_C,
    LargeMotor,
    MoveTank,
)

from ev3dev2.sensor import INPUT_3, lego

""""
De robot wordt met de sensor aan de linkerkant van de lijn geplaatst en rijdt
in een gekromde lijn zodat hij steeds afwijkt in de richting van de lijn. Als
de lijn gedecteerd wordt draait de robot even naar links, weg van de lijn en
daarna gaat hij weer verder in een kromme lijn.
"""

#initializeer motors en kleursensor
MOTOR_LINKS = LargeMotor(OUTPUT_B)
MOTOR_RECHTS = LargeMotor(OUTPUT_C)
KLEURSENSOR = lego.ColorSensor(address=INPUT_3)

def _rijd_kromme():
    robot_tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
    robot_tank_drive.on(left_speed=30, right_speed=20)

while True:
    # rijden in kromme moet in apparte thread
    t_rij = threading.Thread(target=_rijd_kromme, args=())
    t_rij.start()

    # oneindige lus controleert of sensor op de lijn komt
    while KLEURSENSOR.color == KLEURSENSOR.COLOR_WHITE:
        pass
    
    # in dit deel van de code komen we pas als de sensor niet meer wit detecteert
    MOTOR_LINKS.stop(stop_action='brake')
    MOTOR_RECHTS.stop(stop_action='brake')
    MoveTank(OUTPUT_B, OUTPUT_C).on_for_degrees(left_speed=-50, right_speed=50, degrees=45)
