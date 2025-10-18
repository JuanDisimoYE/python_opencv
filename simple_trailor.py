import cv2
from vehicle_visual import static_axle_visual, line
from SharedCalculation import getDistance, sin, cos, acos, atan, pow2
import math

x = 0
y = 1

class simple_trailor:
    def __init__(self, length_clutch, width, wheel_length, wheel_width, line_width, start_x, start_y, alignment_start):
        self.length_clutch = length_clutch
        self.width = width
        self.line_width = line_width
        self.position_front = (start_x, start_y)
        self.alignment = alignment_start
        self.position_back = (start_x - length_clutch * cos(alignment_start), start_y - length_clutch * sin(alignment_start))
        self.static_axle = static_axle_visual(width, wheel_length, wheel_width, line_width)

    def draw(self, image, new_position_x, new_position_y):
        self.position_back = self.__getNewBackPosition(new_position_x, new_position_y)
        self.position_front = new_position_x, new_position_y
        self.alignment = self.__getAlignment()

        line(image, self.position_back[x], self.position_back[y], self.position_front[x], self.position_front[y], self.line_width)
        self.static_axle.draw(image, -self.alignment, self.position_back[x], self.position_back[y])
        return
    
    def getBackPosition(self):
        return self.position_back

    def __getRadiusDeviation(self, new_position_x, new_position_y):
        return self.length_clutch - getDistance(new_position_x, new_position_y, self.position_back[x], self.position_back[y])
    
    def __getNewBackPosition(self, new_position_x, new_position_y):
        delta_r = self.__getRadiusDeviation(new_position_x, new_position_y)
        best_x = 0
        best_y = 0
        best_value = 0

        for angle in range(0, 360, 10):
            bx = self.position_back[x] + delta_r * cos(angle)
            by = self.position_back[y] - delta_r * sin(angle)

            value = getDistance(new_position_x, new_position_y, bx, by)
            if abs(value - self.length_clutch) < abs(best_value - self.length_clutch):
                best_value = value
                best_x = bx
                best_y = by
        
        return best_x, best_y
    
    def __getAlignment(self):
        return acos( (self.position_front[x] - self.position_back[x]) / self.length_clutch )
    