#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor, TouchSensor, InfraredSensor, GyroSensor, UltrasonicSensor, ColorSensor)  
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick

import random

#------------------------------------------------------------------------------
# Initialization

distance_sensor = UltrasonicSensor(Port.S1)
gyro_sensor = GyroSensor(Port.S2)
obstacle_sensor = InfraredSensor(Port.S4)
color_sensor = ColorSensor(Port.S3)
ev3 = EV3Brick()

robot = DriveBase(left_motor=Motor(Port.B), right_motor=Motor(Port.C), wheel_diameter=62.4, axle_track=109.605)  # mm
robot.settings(straight_speed=60, straight_acceleration=60, turn_rate=60, turn_acceleration=60)

data = DataLog('time / s', 'distance / m', 'angle motors / °', 'angle gyro / °', name='C:\\UNSA\\robotica\\final', timestamp=False)
watch = StopWatch()

#------------------------------------------------------------------------------
# Function to Convert Color to Name
def get_color_name(detected_color):
    """Convert the detected color to a human-readable name."""
    return {
        Color.RED: "Red",
        Color.BLUE: "Blue",
        Color.GREEN: "Green",
        Color.YELLOW: "Yellow",
        Color.BLACK: "Black",
        Color.WHITE: "White",
        None: "No color"
    }.get(detected_color, "Unknown")

#------------------------------------------------------------------------------
# Main Script

angle = 0
running = True  # Variable de control
robot.straight(+2000)  # mm
robot.turn(90)  # Girar 90° a la derecha
while running:
    print(running)
    robot.drive(speed=100, turn_rate=0)  # mm/s, deg/s

    while (obstacle_sensor.distance() < 20 or distance_sensor.distance() < 200) and running:
        wait(100)  # ms
        ev3.speaker.beep()
        robot.straight(+180)  # mm
        wait(200)
        # Detectar el color
        detected_color = color_sensor.color()  
        color_name = get_color_name(detected_color)  # Llamar a la función para obtener el nombre del color

        # Verificar si el color es rojo o azul (víctima detectada)
        if detected_color in [Color.RED, Color.BLUE]:
            print("Victim detected:", color_name)  
            ev3.speaker.say("Victim detected")  # Decir "Victim detected"
            running = False  # Detener el bucle principal
            robot.stop()  # Detener el robot
            break

        # Si no es rojo ni azul (caso contrario)
        print("Detected color:", color_name)  
        ev3.speaker.say(color_name)  
        
        # Retroceder 5 cm y girar 90° a la derecha
        robot.straight(-50)  # Retroceder 50 mm (5 cm)
        robot.turn(-90)  # Girar 90° a la derecha
        
        # Salir del bucle interno
        break

# Detén el robot al salir del bucle externo
robot.stop()
print("Program finished.")