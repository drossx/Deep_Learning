import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import string
import os

import cv2

import glob

jpgFiles = glob.glob("./images/*.jpg")


def from_yolo_to_cor(box, shape):
    img_h, img_w = shape
    # x1, y1 = ((x + witdth)/2)*img_width, ((y + height)/2)*img_height
    # x2, y2 = ((x - witdth)/2)*img_width, ((y - height)/2)*img_height
    x1, y1 = int((box[0] + box[2] / 2) * img_w), int((box[1] + box[3] / 2) * img_h)
    x2, y2 = int((box[0] - box[2] / 2) * img_w), int((box[1] - box[3] / 2) * img_h)
    return x1, y1, x2, y2


cwd = os.getcwd()

for i in jpgFiles:

    i = cwd + i[1:] #jpeg file
    img = cv2.imread("%s" % i)

    try:

        j = i[:-4] + ".txt" #txt annotations file
        f = open("%s" % j)

        print("file opened")

        for line in f:

            box = line[2:]

            box = box.split(" ")
            box = [float(i) for i in box]
            shape = [720, 1280]

            x1, y1, x2, y2 = from_yolo_to_cor(box, shape)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)



    except FileNotFoundError:
        break

    cv2.imshow('image', img)
    cv2.waitKey(1100)
    cv2.destroyAllWindows()

