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


class axle:
    def __init__(self, width):
        self.width = width

    def getRightPoint(self, alignment, center_x, center_y):
        pRight_x = int(center_x - ( self.width / 2) * math.sin(degreeToRadians(-alignment)))
        pRight_y = int(center_y - ( self.width / 2) * math.cos(degreeToRadians(-alignment)))
        return pRight_x, pRight_y
    
    def getleftPoint(self, alignment, center_x, center_y):
        pLeft_x = int(center_x + ( self.width / 2) * math.sin(degreeToRadians(-alignment)))
        pLeft_y = int(center_y + ( self.width / 2) * math.cos(degreeToRadians(-alignment)))
        return pLeft_x, pLeft_y


class turntable_axis_visual:
    def __init__(self, car_width, wheel_length, wheel_width, line_width):
        self.width = car_width - wheel_width
        self.wheel = wheel_visual(wheel_length, wheel_width, line_width)
        self.line_width = line_width
    
    def draw(self, image, alignment, wheel_alignment, center_x, center_y):
        angle = -(alignment+wheel_alignment)
        pRight_x = int(center_x - ( self.width / 2) * math.sin(degreeToRadians(angle)))
        pRight_y = int(center_y - ( self.width / 2) * math.cos(degreeToRadians(angle)))

        pLeft_x = int(center_x + ( self.width / 2) * math.sin(degreeToRadians(angle)))
        pLeft_y = int(center_y + ( self.width / 2) * math.cos(degreeToRadians(angle)))

        cv2.line(image, (pRight_x,pRight_y), (pLeft_x,pLeft_y), (0,0,0), self.line_width)

        self.wheel.draw(image, -angle, pRight_x, pRight_y)
        self.wheel.draw(image, -angle, pLeft_x, pLeft_y)

class static_axle_visual(axle):
    def __init__(self, car_width, wheel_length, wheel_width, line_width):
        self.width = car_width - wheel_width
        self.wheel = wheel_visual(wheel_length, wheel_width, line_width)
        self.line_width = line_width
        axle.__init__(self, self.width)

    def draw(self, image, alignment, center_x, center_y):
        pRight_x, pRight_y = self.getRightPoint(alignment, center_x, center_y)
        pLeft_x, pLeft_y = self.getleftPoint(alignment, center_x, center_y)

        cv2.line(image, (pRight_x,pRight_y), (pLeft_x,pLeft_y), (0,0,0), self.line_width)
        
        self.wheel.draw(image, alignment, pRight_x, pRight_y)
        self.wheel.draw(image, alignment, pLeft_x, pLeft_y)


class parallel_axle_visual(axle):
    def __init__(self, car_width, wheel_length, wheel_width, line_width):
        self.width = car_width - wheel_width
        self.wheel = wheel_visual(wheel_length, wheel_width, line_width)
        self.line_width = line_width
        axle.__init__(self, self.width)

    def draw(self, image, alignment, wheel_alignment, center_x, center_y):
        pRight_x, pRight_y = self.getRightPoint(alignment, center_x, center_y)
        pLeft_x, pLeft_y = self.getleftPoint(alignment, center_x, center_y)

        cv2.line(image, (pRight_x,pRight_y), (pLeft_x,pLeft_y), (0,0,0), self.line_width)
        
        self.wheel.draw(image, alignment + wheel_alignment, pRight_x, pRight_y)
        self.wheel.draw(image, alignment + wheel_alignment, pLeft_x, pLeft_y)


class car_visual:
    def __init__(self, length, width, wheel_length, wheel_width, line_width, size_x, size_y):
        self.length = length
        self.width = width
        self.line_width = line_width
        self.size_x = size_x
        self.size_y = size_y
        self.static_axle = static_axle_visual(width, wheel_length, wheel_width, line_width)
        self.parallel_axle = parallel_axle_visual(width, wheel_length, wheel_width, line_width)

    def getImage(self, alignment_wheel, middle_bar_front_x, middle_bar_front_y, alignment_bar):
        image = np.ones((self.size_y, self.size_x, 3), dtype=np.uint8) * 255

        # middle bar
        middle_bar_back_x = int(middle_bar_front_x - self.getBarLength() * math.cos(degreeToRadians(alignment_bar)))
        middle_bar_back_y = int(middle_bar_front_y - self.getBarLength() * math.sin(degreeToRadians(alignment_bar)))
        cv2.line(image, (int(middle_bar_front_x),int(middle_bar_front_y)), (middle_bar_back_x,middle_bar_back_y), (0,0,0), self.line_width)

        # axles
        self.static_axle.draw(image, alignment_bar, middle_bar_back_x, middle_bar_back_y)
        self.parallel_axle.draw(image, alignment_bar, alignment_wheel, middle_bar_front_x, middle_bar_front_y)

        return image
    
    def getBarLength(self):
        return self.length - self.static_axle.wheel.length
    

class trailer_visual:
    def __init__(self, length, width, wheel_length, wheel_width, line_width):
        self.length = length
        self.width = width
        self.line_width = line_width
        self.static_axle = static_axle_visual(width, wheel_length, wheel_width, line_width)
        self.turntable_axle = turntable_axis_visual(width, wheel_length, wheel_width, line_width)

    def getImage(self, image, alignment_wheel, middle_bar_front_x, middle_bar_front_y, alignment_bar):
        # middle bar
        middle_bar_back_x = int(middle_bar_front_x - self.getBarLength() * math.cos(degreeToRadians(alignment_bar)))
        middle_bar_back_y = int(middle_bar_front_y - self.getBarLength() * math.sin(degreeToRadians(alignment_bar)))
        cv2.line(image, (int(middle_bar_front_x),int(middle_bar_front_y)), (middle_bar_back_x,middle_bar_back_y), (0,0,0), self.line_width)

        # axles
        self.static_axle.draw(image, alignment_bar, middle_bar_back_x, middle_bar_back_y)
        self.turntable_axle.draw(image, alignment_bar, alignment_wheel, middle_bar_front_x, middle_bar_front_y)

        # clutch
        cv2.line(image, (int(middle_bar_front_x),int(middle_bar_front_y)), (int(middle_bar_front_x + 100),int(middle_bar_front_y)), (0,0,0), self.line_width)
    
    def getBarLength(self):
        return self.length - self.static_axle.wheel.length