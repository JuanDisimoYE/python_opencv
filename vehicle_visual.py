import cv2
import numpy as np
import math
from numba import jit



@jit
def degreeToRadians(degree):
    return (degree/180)*math.pi

class wheel_visual:
    def __init__(self, length, width, line_width):
        self.length = length
        self.width = width
        self.line_width = line_width

    def draw(self, image, alignment, center_x, center_y):
        length_offset_x = (self.length/2)*math.cos(degreeToRadians(alignment))
        length_offset_y = (self.length/2)*math.sin(degreeToRadians(alignment))
        width_offset_x = (self.width/2)*math.sin(degreeToRadians(alignment))
        width_offset_y = (self.width/2)*math.cos(degreeToRadians(alignment))

        pA_x = int( center_x - length_offset_x - width_offset_x )
        pA_y = int( center_y - length_offset_y + width_offset_y )
        pB_x = int( center_x + length_offset_x - width_offset_x )
        pB_y = int( center_y + length_offset_y + width_offset_y )
        pC_x = int( center_x + length_offset_x + width_offset_x )
        pC_y = int( center_y + length_offset_y - width_offset_y )
        pD_x = int( center_x - length_offset_x + width_offset_x )
        pD_y = int( center_y - length_offset_y - width_offset_y )

        cv2.line(image, (pA_x,pA_y), (pB_x,pB_y), (0,0,0), self.line_width)
        cv2.line(image, (pB_x,pB_y), (pC_x,pC_y), (0,0,0), self.line_width)
        cv2.line(image, (pC_x,pC_y), (pD_x,pD_y), (0,0,0), self.line_width)
        cv2.line(image, (pD_x,pD_y), (pA_x,pA_y), (0,0,0), self.line_width)

class static_axle_visual:
    def __init__(self, car_width, wheel_length, wheel_width, line_width):
        self.width = car_width - wheel_width
        self.wheel = wheel_visual(wheel_length, wheel_width, line_width)
        self.line_width = line_width

    def draw(self, image, alignment, center_x, center_y):
        pRight_x = int(center_x - ( self.width / 2) * math.sin(degreeToRadians(-alignment)))
        pRight_y = int(center_y - ( self.width / 2) * math.cos(degreeToRadians(-alignment)))

        pLeft_x = int(center_x + ( self.width / 2) * math.sin(degreeToRadians(-alignment)))
        pLeft_y = int(center_y + ( self.width / 2) * math.cos(degreeToRadians(-alignment)))

        cv2.line(image, (pRight_x,pRight_y), (pLeft_x,pLeft_y), (0,0,0), self.line_width)
        
        self.wheel.draw(image, alignment, pRight_x, pRight_y)
        self.wheel.draw(image, alignment, pLeft_x, pLeft_y)

class car_visual:
    def __init__(self, length, width, wheel_length, wheel_width, line_width, size_x, size_y):
        self.length = length
        self.width = width
        self.wheel = wheel_visual(wheel_length, wheel_width, line_width)
        self.static_axle = static_axle_visual(width, wheel_length, wheel_width, line_width)
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
        wheel_axle_length = self.width - self.wheel.width

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

        # cv2.line(image, (wheel_axle_back_left_x,wheel_axle_back_left_y), (wheel_axle_back_right_x,wheel_axle_back_right_y), (0,0,0), self.line_width)
        self.static_axle.draw(image, alignment_bar, middle_bar_back_x, middle_bar_back_y)

        # wheels
        # self.wheel.draw(image, alignment_bar, wheel_axle_back_left_x, wheel_axle_back_left_y)
        # self.wheel.draw(image, alignment_bar, wheel_axle_back_right_x, wheel_axle_back_right_y)
        self.wheel.draw(image, alignment_bar + alignment_wheel, wheel_axle_front_left_x, wheel_axle_front_left_y)
        self.wheel.draw(image, alignment_bar + alignment_wheel, wheel_axle_front_right_x, wheel_axle_front_right_y)

        return image
    
    def getBarLength(self):
        return self.length - self.wheel.length