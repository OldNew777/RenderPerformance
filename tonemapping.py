import numpy as np


def rgb2srgb(image):
    return np.uint8(np.round(np.clip(np.where(
        image <= 0.00304,
        12.92 * image,
        1.055 * np.power(image, 1.0 / 2.4) - 0.055
    ) * 255, 0, 255)))


def tonemapping(x):
    a = 2.51
    b = 0.03
    c = 2.43
    d = 0.59
    e = 0.14
    return rgb2srgb(x * (a * x + b) / (x * (c * x + d) + e))

def tonemapping_uncharted2(x):
    def F(x):
        A = 0.22
        B = 0.30
        C = 0.10
        D = 0.20
        E = 0.01
        F = 0.30
        return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F
    return rgb2srgb(F(x))
