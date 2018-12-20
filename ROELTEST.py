#!/usr/bin/env python3

from DeVestenBot import DeVestenBot
import socket, time, json

bot = DeVestenBot()

HOST = '10.42.0.1'  # The server's hostname or IP address
PORT = 2444        # The port used by the server

#bot.log(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])

#[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] 
#or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])

#for ip in socket.gethostbyname_ex(socket.gethostname())

MOTOR_LINKS = 'MOTOR_LINKS'
MOTOR_RECHTS = 'MOTOR_RECHTS'
GRIJPER = 'GRIJPER'
GYRO = 'GYRO'
AFSTAND = 'AFSTAND'
KLEUR = 'KLEUR'
DRUK = 'DRUK'

sensor_data = {
    MOTOR_LINKS : None,
    MOTOR_RECHTS : None,
    GRIJPER : None,
    GYRO : None,
    AFSTAND : None,
    KLEUR : None,
    DRUK : None
}

def get_sensor_data():
    sensor_data['TIMESTAMP'] = round(time.clock(),2)
    sensor_data[MOTOR_LINKS] = round(bot.motor_links.degrees)
    sensor_data[MOTOR_RECHTS] = round(bot.motor_rechts.degrees)
    sensor_data[GRIJPER] = round(bot.motor_grijper.degrees)
    sensor_data[GYRO] = round(bot.gyro.angle)
    sensor_data[AFSTAND] = round(bot.meet_afstand_in_cm(),2)
    sensor_data[KLEUR] = bot.get_kleur()
    sensor_data[DRUK] = bot.is_druksensor_ingedrukt()
    return sensor_data

def get_sensor_data_as_json():
    return json.dumps(get_sensor_data())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(get_sensor_data_as_json().encode())
        time.sleep(0.25)