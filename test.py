import numpy as np


def normalize(array: np.ndarray) -> np.ndarray:
    x = np.linalg.norm(array, ord=2)
    return array / x


transform_mitsuba = np.array(
    [[-9.90690e-01, 7.03500e-03, 1.35953e-01, -5.19664e-01],
     [9.40074e-10, 9.98664e-01, -5.16768e-02, 8.17007e-01],
     [-1.36134e-01, -5.11957e-02, -9.89367e-01, 3.82439e+00],
     [0.00000e+00, 0.00000e+00, 0.00000e+00, 1.00000e+00]]
)

position = np.array(
    [
        -0.5196635723114014,
        0.8170070052146912,
        3.824389696121216
    ]
)
look_at = np.array(
    [
        -0.0668703019618988,
        0.6448959708213806,
        0.5292789936065674
    ]
)
up = np.array([0., 1., 0.])
right = normalize(np.cross(look_at, up))
new_up = normalize(np.cross(look_at, right))
look_at = normalize(look_at)
transform_pbrt = np.array([
    right, new_up, look_at, position
])
transform_pbrt = np.r_[transform_pbrt.transpose(), [[0., 0., 0., 1.]]]
print(f'transform_pbrt = \n{transform_pbrt}\n')
print(f'transform_mitsuba = \n{transform_mitsuba}\n')

# print(right / transform_mitsuba[:3, 0])
# print(new_up / transform_mitsuba[:3, 1])
# print(look_at / transform_mitsuba[:3, 2])
