import keyboard
import numpy as np
import math
from numba import jit
from vehicle_visual import car_visual
from vehicle_visual import degreeToRadians

    
    
@jit
def getFrontRadius(bar_length, wheel_alignment):
    return bar_length / math.sin(degreeToRadians(wheel_alignment))

@jit
def getBackRadius(bar_length, wheel_alignment):
    return bar_length * math.cos(degreeToRadians(wheel_alignment))

@jit
def getDistanceAngle(bar_length, distance, wheel_alignment):
    if wheel_alignment == 0:
        distance_angle = 0
    else:
        radius_front = getFrontRadius(bar_length, wheel_alignment)
        distance_angle = (distance * 180) / (math.pi * radius_front)
    return distance_angle

@jit
def getFrontDeviation(bar_length, distance, wheel_alignment):
    if wheel_alignment == 0:
        front_deviation = distance
    else:
        alpha = 90 - 0.5*getDistanceAngle(bar_length, distance, wheel_alignment)
        front_deviation = distance * math.cos(degreeToRadians( (90-alpha) + wheel_alignment))
    return front_deviation

@jit
def getRightDeviation(bar_length, distance, wheel_alignment):
    if wheel_alignment == 0:
        right_deviation = 0
    else:
        alpha = 90 - 0.5*getDistanceAngle(bar_length, distance, wheel_alignment)
        right_deviation = distance * math.sin(degreeToRadians( (90-alpha) + wheel_alignment))

    return right_deviation

@jit
def getNewFrontPosition(current_front_x, current_front_y, current_alignment, front_deviation, right_deviation):
    front_x = current_front_x + front_deviation * math.cos(degreeToRadians(current_alignment)) + right_deviation * math.sin(degreeToRadians(current_alignment))
    front_y = current_front_y + front_deviation * math.sin(degreeToRadians(current_alignment)) - right_deviation * math.cos(degreeToRadians(current_alignment))
    return front_x, front_y
    
class speed:
    def __init__(self):
        self.speed = 0
        self.alignment = 0
        self.max_speed = 3
        self.max_alignment = 45
    

    def getWheelAlignment(self):
        if keyboard.is_pressed('a'):
            self.alignment = self.alignment + 2
        if keyboard.is_pressed('d'):
            self.alignment = self.alignment - 2
        return getBorderedValue(self.alignment, self.max_alignment)
    
    def getSpeed(self):
        if keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
            direction = + 0.5
        elif keyboard.is_pressed('s') and not keyboard.is_pressed('w'):
            direction = - 0.5
        else:
            direction = 0

        self.speed = self.speed + direction

        if direction == 0 and abs(self.speed):
            if self.speed > 0:
                self.speed = self.speed - 0.3
                if self.speed < 0:
                    self.speed = 0
            else:
                self.speed = self.speed + 0.3
                if self.speed > 0:
                    self.speed = 0

        return getBorderedValue(self.speed, self.max_speed)

@jit
def getBorderedValue(value, max_velue):
    if value > max_velue:
        value = max_velue
    elif value < -max_velue:
        value = -max_velue
    return value