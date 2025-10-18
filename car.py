import cv2
import numpy as np
import math
from numba import jit

from SharedCalculation import sin, cos

from vehicle_visual import static_axle_visual
from vehicle_visual import parallel_axle_visual

x = 0
y = 1


class car:
    def __init__(self, length, width, wheel_length, wheel_width, line_width, start_x, start_y, alignment_start):
        self.length = length
        self.width = width
        self.line_width = line_width
        self.position_front = (start_x, start_y)
        self.alignment = alignment_start
        self.position_back = (0, 0)
        self.static_axle = static_axle_visual(width, wheel_length, wheel_width, line_width)
        self.parallel_axle = parallel_axle_visual(width, wheel_length, wheel_width, line_width)

    def draw(self, image, distance, alignment_wheel):
        front_deviation = self.__getFrontDeviation(distance, alignment_wheel)
        right_deviation = self.__getRightDeviation(distance, alignment_wheel)
        self.position_front = self.__getNewFrontPosition(self.alignment, front_deviation, right_deviation)
        self.alignment = self.alignment + self.__getDistanceAngle(distance, alignment_wheel)
        self.position_back = self.__getBackPosition()

        # middle bar
        cv2.line(image, (int(self.position_front[x]),int(self.position_front[y])), (int(self.position_back[x]),int(self.position_back[y])), (0,0,0), self.line_width)

        # axles
        self.parallel_axle.draw(image, self.alignment, alignment_wheel, self.position_front[x], self.position_front[y])        
        self.static_axle.draw(image, self.alignment, self.position_back[x], self.position_back[y])

    def getBarLength(self):
        return self.length - self.static_axle.wheel.length 

    def __getFrontRadius(self, wheel_alignment):
        return self.getBarLength() / sin(wheel_alignment)
    
    def __getDistanceAngle(self, distance, wheel_alignment):
        if wheel_alignment == 0:
            distance_angle = 0
        else:
            radius_front = self.__getFrontRadius(wheel_alignment)
            distance_angle = (distance * 180) / (math.pi * radius_front)
        return distance_angle

    def __getFrontDeviation(self, distance, wheel_alignment):
        if wheel_alignment == 0:
            front_deviation = distance
        else:
            alpha = 90 - 0.5*self.__getDistanceAngle(distance, wheel_alignment)
            front_deviation = distance * cos((90-alpha) + wheel_alignment)
        return front_deviation
    
    def __getRightDeviation(self, distance, wheel_alignment):
        if wheel_alignment == 0:
            right_deviation = 0
        else:
            alpha = 90 - 0.5*self.__getDistanceAngle(distance, wheel_alignment)
            right_deviation = distance * sin((90-alpha) + wheel_alignment)

        return right_deviation

    def __getNewFrontPosition(self, current_alignment, front_deviation, right_deviation):
        front_x = self.position_front[x] + front_deviation * cos(current_alignment) - right_deviation * sin(current_alignment)
        front_y = self.position_front[y] + front_deviation * sin(current_alignment) + right_deviation * cos(current_alignment)
        return front_x, front_y
    
    def __getBackPosition(self):
        back_x = self.position_front[x] - self.getBarLength() * cos(self.alignment)
        back_y = self.position_front[y] - self.getBarLength() * sin(self.alignment)
        return back_x, back_y