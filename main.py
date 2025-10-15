import cv2
from vehicle import getFrontDeviation
from vehicle import getRightDeviation
from vehicle import getDistanceAngle
from vehicle import getNewFrontPosition
from vehicle import speed
from vehicle_visual import car_visual





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