import cv2
import time


def main():

    # blue_index = 0
    # timestamp = time.time()
    img = cv2.imread("images/blank.png", 1)
    print(type(img))

    # while blue_index < 255:

    #     if (time.time() - timestamp) >= 0.1:
    #         img_with_line = cv2.line(img.copy(), (0,0), (200,200), (blue_index,0,0), 10)
    #         cv2.imshow("image", img_with_line)
    #         timestamp = time.time()
    #         blue_index = blue_index + 1
    #         print(blue_index)
    #         cv2.waitKey(1)

    for blue_index in range(0, 255):
        img_with_line = cv2.line(img.copy(), (0,0), (200,200), (blue_index,0,0), 10)
        cv2.imshow("image", img_with_line)
        if cv2.waitKey(100) == 27: # 27 = ESC
            print("animation skipped")
            break

    print("wait for key")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def experiemnt():
    img = cv2.imread("images/blank.png", 1)
    cv2.imshow("image", img)
    if cv2.waitKey(0) == ord("w"):
        print("w")
    cv2.destroyAllWindows()



if (__name__ == "__main__"):
    # main()
    experiemnt()

