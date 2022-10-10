import os
import sys

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np

if __name__ == '__main__':
    image_path = sys.argv[1]
    point_position = image_path.rfind('.')
    output_path = image_path[:point_position] + '-cut' + image_path[point_position:]
    area_path = image_path[:point_position] + '-area' + image_path[point_position:]

    area = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    image_cut = image[area[2]:area[3], area[0]:area[1]]
    image_area = image.copy()
    fill_color = np.array([0.5, 0.5, 0.0, 1.0])
    line_width = 5
    half_line_width = line_width // 2
    for i in range(max(0, area[2] - half_line_width), min(image.shape[0], area[3] + half_line_width)):
        for j in range(line_width):
            k = area[0] - half_line_width + j
            if 0 <= k < image.shape[1]:
                image_area[i, k] = fill_color
            k = area[1] - half_line_width + j
            if 0 <= k < image.shape[1]:
                image_area[i, k] = fill_color
    for j in range(max(0, area[0] - half_line_width), min(image.shape[1], area[1] + half_line_width)):
        for i in range(line_width):
            k = area[2] - half_line_width + i
            if 0 <= k < image.shape[0]:
                image_area[k, j] = fill_color
            k = area[3] - half_line_width + i
            if 0 <= k < image.shape[0]:
                image_area[k, j] = fill_color

    cv2.imwrite(output_path, image_cut)
    cv2.imwrite(area_path, image_area)
