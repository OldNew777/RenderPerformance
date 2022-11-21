import os
import sys

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def turn_off_spines(ax):
    ax.set_frame_on(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


def relMSE(ref_image, rendered_image):
    diff_image = np.mean(np.square(rendered_image - ref_image) / (np.square(ref_image) + 0.01), axis=2)
    return np.mean(diff_image), diff_image


def add_colorbar(image, ax, fig):
    im = ax.imshow(image)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="100%", pad=0.05)
    fig.colorbar(im, ax=cax, orientation="horizontal", shrink=0.6)
    cax.set_xticks([0, 1e-3], labels=['0', '1e-3'])
    cax.set_xlim([0, 1e-3])


if __name__ == '__main__':
    ref_image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
    rendered_image = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)
    value, diff_image = relMSE(ref_image, rendered_image)
    print(f'relMSE = {value}')
    exp = 0.0
    # add_colorbar(tm.tonemapping(diff_image * (2 ** exp)))
    # add_colorbar(tm.tonemapping(diff_image))
    fig = plt.figure(figsize=(3, 6), constrained_layout=True)
    ax = fig.add_subplot()
    add_colorbar(np.clip(diff_image, 0, 0.002), ax, fig)
    turn_off_spines(ax)
    plt.show()
    cv2.imwrite('diff-falsecolor.exr', diff_image)
    fig.savefig('diff-falsecolor.png')
    fig.savefig('diff-falsecolor.pdf')
