import cv2
import keyboard
import numpy as np
import math
from numba import jit



class vehicle:
    def __init__(self, length, width, wheel_length, wheel_width, line_width, size_x, size_y):
        self.length = length
        self.width = width
        self.wheel_length = wheel_length
        self.wheel_width = wheel_width
        self.line_width = line_width
        self.size_x = size_x
        self.size_y = size_y
        self.alignment = 0

    def getImage(self, alignment_wheel, middle_bar_front_x, middle_bar_front_y, alignment_bar):
        image = np.ones((self.size_y, self.size_x, 3), dtype=np.uint8) * 255

        # middle bar
        middle_bar_back_x = int(middle_bar_front_x - self.getBarLength() * math.cos(degreeToRadians(alignment_bar)))
        middle_bar_back_y = int(middle_bar_front_y - self.getBarLength() * math.sin(degreeToRadians(alignment_bar)))
        cv2.line(image, (int(middle_bar_front_x),int(middle_bar_front_y)), (middle_bar_back_x,middle_bar_back_y), (0,0,0), self.line_width)

        # wheel axle
        wheel_axle_length = self.width - self.wheel_width

        wheel_axle_offset_x = (wheel_axle_length/2) * math.sin(degreeToRadians(alignment_bar))
        wheel_axle_offset_y = (wheel_axle_length/2) * math.cos(degreeToRadians(alignment_bar))

        wheel_axle_front_left_x = int(middle_bar_front_x - wheel_axle_offset_x)
        wheel_axle_front_left_y = int(middle_bar_front_y + wheel_axle_offset_y)
        wheel_axle_front_right_x = int(middle_bar_front_x + wheel_axle_offset_x)
        wheel_axle_front_right_y = int(middle_bar_front_y - wheel_axle_offset_y)

        cv2.line(image, (wheel_axle_front_left_x,wheel_axle_front_left_y), (wheel_axle_front_right_x,wheel_axle_front_right_y), (0,0,0), self.line_width)

        wheel_axle_back_left_x = int(middle_bar_back_x - wheel_axle_offset_x)
        wheel_axle_back_left_y = int(middle_bar_back_y + wheel_axle_offset_y)
        wheel_axle_back_right_x = int(middle_bar_back_x + wheel_axle_offset_x)
        wheel_axle_back_right_y = int(middle_bar_back_y - wheel_axle_offset_y)

        cv2.line(image, (wheel_axle_back_left_x,wheel_axle_back_left_y), (wheel_axle_back_right_x,wheel_axle_back_right_y), (0,0,0), self.line_width)

        # wheels
        self.writeWheel(image, alignment_bar, wheel_axle_back_left_x, wheel_axle_back_left_y)
        self.writeWheel(image, alignment_bar, wheel_axle_back_right_x, wheel_axle_back_right_y)
        self.writeWheel(image, alignment_bar + alignment_wheel, wheel_axle_front_left_x, wheel_axle_front_left_y)
        self.writeWheel(image, alignment_bar + alignment_wheel, wheel_axle_front_right_x, wheel_axle_front_right_y)

        return image
    
    def writeWheel(self, image, alignment, position_x, position_y):
        length_offset_x = (self.wheel_length/2)*math.cos(degreeToRadians(alignment))
        length_offset_y = (self.wheel_length/2)*math.sin(degreeToRadians(alignment))
        width_offset_x = (self.wheel_width/2)*math.sin(degreeToRadians(alignment))
        width_offset_y = (self.wheel_width/2)*math.cos(degreeToRadians(alignment))

        pA_x = int( position_x - length_offset_x - width_offset_x )
        pA_y = int( position_y - length_offset_y + width_offset_y )
        pB_x = int( position_x + length_offset_x - width_offset_x )
        pB_y = int( position_y + length_offset_y + width_offset_y )
        pC_x = int( position_x + length_offset_x + width_offset_x )
        pC_y = int( position_y + length_offset_y - width_offset_y )
        pD_x = int( position_x - length_offset_x + width_offset_x )
        pD_y = int( position_y - length_offset_y - width_offset_y )

        cv2.line(image, (pA_x,pA_y), (pB_x,pB_y), (0,0,0), self.line_width)
        cv2.line(image, (pB_x,pB_y), (pC_x,pC_y), (0,0,0), self.line_width)
        cv2.line(image, (pC_x,pC_y), (pD_x,pD_y), (0,0,0), self.line_width)
        cv2.line(image, (pD_x,pD_y), (pA_x,pA_y), (0,0,0), self.line_width)
    
    def getBarLength(self):
        return self.length - self.wheel_length
    
    
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
def degreeToRadians(degree):
    return (degree/180)*math.pi

@jit
def getBorderedValue(value, max_velue):
    if value > max_velue:
        value = max_velue
    elif value < -max_velue:
        value = -max_velue
    return value


if __name__ == "__main__":

    car = vehicle(200,100,40,20,2,1000,1000)
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
