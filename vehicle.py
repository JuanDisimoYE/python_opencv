import cv2
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

        if direction == 0 and self.speed:
            if self.speed > 0:
                self.speed = self.speed - 0.15
                if self.speed < 0:
                    self.speed = 0
            else:
                self.speed = self.speed + 0.15
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


if __name__ == "__main__":

    car = car_visual(200,100,40,20,2,1000,1000)
    car_speed = speed()

    bar_length = car.getBarLength()
    wheel_alignment = 0
    bar_alignment = 0
    direction = 0
    old_alignment = 1

    front_x = 500
    front_y = 500

    while cv2.waitKey(10) != 27:
        
        direction = car_speed.getSpeed()
        wheel_alignment = car_speed.getWheelAlignment()

        if (old_alignment != wheel_alignment) or (direction):
            deviation_front = getFrontDeviation(bar_length, direction, wheel_alignment)
            deviation_right = getRightDeviation(bar_length, direction, wheel_alignment)
            deviation_alignment = getDistanceAngle(bar_length, direction, wheel_alignment)

            front_x, front_y = getNewFrontPosition(front_x, front_y, bar_alignment, deviation_front, deviation_right)
            bar_alignment = bar_alignment - deviation_alignment

            img = car.getImage(-wheel_alignment, front_x, front_y, bar_alignment)
            cv2.imshow("image", img)


        old_alignment = wheel_alignment


    cv2.destroyAllWindows()
