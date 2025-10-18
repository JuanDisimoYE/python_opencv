import cv2
import numpy as np

from SharedCalculation import speed
from vehicle_visual import trailer_visual
from car import car





if __name__ == "__main__":

    tatal_car = car(200, 100, 40, 20, 2, 500, 500, 0)
    car_speed = speed()
    trailor_vis = trailer_visual(200, 100, 40, 20, 2)

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

            cv2.imshow("other", image)


        old_alignment = wheel_alignment


    cv2.destroyAllWindows()