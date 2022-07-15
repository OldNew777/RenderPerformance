import os
import sys
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv
import numpy as np


if __name__ == '__main__':
    filename0 = sys.argv[1]
    filename1 = sys.argv[2]
    image0 = cv.imread(filename0, cv.IMREAD_UNCHANGED)
    image1 = cv.imread(filename1, cv.IMREAD_UNCHANGED)
    for i in range(image0.shape[0]):
        for j in range(image0.shape[1]):
            if j >= image0.shape[0] / 2:
                image0[i, j] = image1[i, j]
    cv.imwrite('merge.exr', image0)
