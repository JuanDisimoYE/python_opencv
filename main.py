import cv2
from vehicle import car_kinematic
from vehicle import speed
from vehicle_visual import car_visual





if __name__ == "__main__":

    car_vis = car_visual(200,100,40,20,2,1000,1000)
    bar_length = car_vis.getBarLength()
    car_kin = car_kinematic(bar_length)
    car_speed = speed()

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
            deviation_front = car_kin.getFrontDeviation(direction, wheel_alignment)
            deviation_right = car_kin.getRightDeviation(direction, wheel_alignment)
            deviation_alignment = car_kin.getDistanceAngle(direction, wheel_alignment)

            front_x, front_y = car_kin.getNewFrontPosition(front_x, front_y, bar_alignment, deviation_front, deviation_right)
            bar_alignment = bar_alignment - deviation_alignment

            img = car_vis.getImage(-wheel_alignment, front_x, front_y, bar_alignment)
            cv2.imshow("image", img)


        old_alignment = wheel_alignment


    cv2.destroyAllWindows()