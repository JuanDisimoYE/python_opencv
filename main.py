import cv2
import numpy as np

from SharedCalculation import speed
from vehicle_visual import trailer_visual
from car import car
from simple_trailor import simple_trailor





if __name__ == "__main__":

    tatal_car = car(200, 100, 40, 20, 2, 500, 500, 0)
    clutch_x, clutch_y = tatal_car.getBackPosition()
    trailor = simple_trailor(100, 100, 40, 20, 2, clutch_x, clutch_y, 0)
    clutch_x, clutch_y = trailor.getBackPosition()
    sensond_trailor = simple_trailor(100, 100, 40, 20, 2, clutch_x, clutch_y, 0)
    car_speed = speed()

    image = np.ones((1000, 1000, 3), dtype=np.uint8) * 255

    wheel_alignment = 0
    direction = 0
    old_alignment = 1


    while cv2.waitKey(10) != 27:
        
        direction = car_speed.getSpeed()
        wheel_alignment = car_speed.getWheelAlignment()

        if (old_alignment != wheel_alignment) or (direction):
            image = np.ones((1000, 1000, 3), dtype=np.uint8) * 255

            tatal_car.draw(image, direction, wheel_alignment)
            back_x, back_y = tatal_car.getBackPosition()
            trailor.draw(image, back_x, back_y)
            back_x, back_y = trailor.getBackPosition()
            sensond_trailor.draw(image, back_x, back_y)

            cv2.imshow("other", image)


        old_alignment = wheel_alignment


    cv2.destroyAllWindows()