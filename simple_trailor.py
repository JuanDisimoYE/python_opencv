import cv2
from vehicle_visual import static_axle_visual
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
        self.position_front = (new_position_x, new_position_y)
        self.alignment = self.__getAlignment()
        print(f"self.alignment = {self.alignment}")

        cv2.line(image, (int(self.position_back[x]), int(self.position_back[y])), (int(self.position_front[x]), int(self.position_front[y])), (0,0,0), self.line_width)
        # self.static_axle.draw(image, self.alignment, self.position_back[x], self.position_back[y])

    def __getAlignment(self):
        return atan( abs(self.position_front[y] - self.position_back[y]) / abs(self.position_front[x] - self.position_back[x]) )

    def __getNewBackPosition(self, new_position_x, new_position_y):
        steps = 50
        radius_deviation = self.__getTranslationDeviation(new_position_x, new_position_y)
        start = self.position_back[x] - radius_deviation
        end = self.position_back[x] + radius_deviation
        stepsize = self.__getStepsize(start, end, steps)
        best_top = 0
        best_down = 0
        best_x_top = 0
        best_x_down = 0

        for Cnt in range(0, steps):
            _x = Cnt * stepsize + start
            tmp = pow2(radius_deviation) - pow2(_x - self.position_back[x])
            if tmp < 0:
                continue
            circle = math.sqrt(tmp)
            top = circle + self.position_back[y]
            down = -circle + self.position_back[y]

            distance_top = getDistance(new_position_x, new_position_y, _x, top)
            if abs(best_top - self.length_clutch) > abs(distance_top - self.length_clutch):
                best_top = distance_top
                best_x_top = _x

            distance_down = getDistance(new_position_x, new_position_y, _x, down)
            if abs(best_down - self.length_clutch) > abs(distance_down - self.length_clutch):
                best_down = distance_down
                best_x_down = _x

        if abs(best_down - self.length_clutch) > abs(best_top - self.length_clutch):
            best_x = best_x_top
        else:
            best_x = best_x_down
        
        return best_x, math.sqrt( pow2(radius_deviation) - pow2(best_x - self.position_back[x]) ) + self.position_back[y]

    def __getTranslationDeviation(self, new_position_x, new_position_y):
        return getDistance(new_position_x, new_position_y, self.position_back[x], self.position_back[y]) - self.length_clutch
    
    def __getStepsize(self, start, end, steps):
        return (end - start) / steps
