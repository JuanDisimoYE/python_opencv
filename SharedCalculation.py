import keyboard
import math
from numba import jit


@jit
def degreeToRadians(degree):
    return (degree/180)*math.pi

@jit
def radiansToDegree(radians):
    return (radians/math.pi)*180
    
class speed:
    def __init__(self):
        self.speed = 0
        self.alignment = 0
        self.max_speed = 3
        self.max_alignment = 45
    

    def getWheelAlignment(self):
        if keyboard.is_pressed('a'):
            self.alignment = self.alignment - 2
        if keyboard.is_pressed('d'):
            self.alignment = self.alignment + 2
        self.alignment = getBorderedValue(self.alignment, self.max_alignment)
        return self.alignment
    
    def getSpeed(self):
        if keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
            direction = + 2
        elif keyboard.is_pressed('s') and not keyboard.is_pressed('w'):
            direction = - 2
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
        
        self.speed = getBorderedValue(self.speed, self.max_speed)

        return self.speed

@jit
def getBorderedValue(value, max_velue):
    if value > max_velue:
        value = max_velue
    elif value < -max_velue:
        value = -max_velue
    return value

# Math functions
@jit
def sin(degree):
    return math.sin(degreeToRadians(degree))

@jit
def cos(degree):
    return math.cos(degreeToRadians(degree))

@jit
def tan(degree):
    return math.tan(degreeToRadians(degree))

@jit
def asin(gradient):
    return radiansToDegree(math.asin(gradient))

@jit
def acos(gradient):
    return radiansToDegree(math.acos(gradient))

@jit
def atan(gradient):
    return radiansToDegree(math.atan(gradient))