import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.image as imread
import os

import plt_config

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv
import numpy as np


def read_hdr2ldr(filename: str) -> np.ndarray:
    image = np.maximum(
        np.nan_to_num(cv.imread(filename, cv.IMREAD_UNCHANGED)[:, :, :3], nan=0.0, posinf=1e3, neginf=0), 0.0)
    image_srgb = np.uint8(np.round(np.clip(np.where(
        image <= 0.00304,
        12.92 * image,
        1.055 * np.power(image, 1.0 / 2.4) - 0.055
    ) * 255, 0, 255)))
    cv.imwrite(f"{filename[:-4]}.png", image_srgb)
    image_srgb = cv.cvtColor(image_srgb, cv.COLOR_BGR2RGB)
    return image_srgb


def plot_diff():
    fig = plt.figure(figsize=(20, 6), constrained_layout=True)

    LuisaRender_time = [121.8529209, 0.489846352, 0.7286828565]
    Mitsuba2_time = [1050.295172, 4.489018485, 6.013933237]
    folder = 'diff-compare'
    target_image = read_hdr2ldr(f"{folder}/target-1024-1024spp.exr")
    initial_image = read_hdr2ldr(f"{folder}/initial-1024-64spp.exr")
    final_image = read_hdr2ldr(f"{folder}/final-1024-64spp.exr")
    images = [target_image, initial_image, final_image]

    gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[6, 1], wspace=0)
    picture_gs = gs[0, 0].subgridspec(nrows=1, ncols=3, width_ratios=[x.shape[1] / x.shape[0] for x in images], wspace=0)
    target_picture_ax = fig.add_subplot(picture_gs[0, 0])
    initial_picture_ax = fig.add_subplot(picture_gs[0, 1])
    final_picture_ax = fig.add_subplot(picture_gs[0, 2])
    compare_ax = fig.add_subplot(gs[0, 1])
    # compare_gs = gs[0, 1].subgridspec(nrows=2, ncols=1, height_ratios=[1, 25], hspace=0)
    # compare_ax = fig.add_subplot(compare_gs[1, 0])

    target_picture_ax.axis("off")
    initial_picture_ax.axis("off")
    final_picture_ax.axis("off")

    target_picture_ax.text(50, 50, 'Target', va="top", color="white")
    initial_picture_ax.text(50, 50, 'Initial', va="top", color="white")
    our_time_text = 'Our time: %.2fs' % LuisaRender_time[0]
    mitsuba2_time_text = 'Mitsuba2 time: %.2fs' % Mitsuba2_time[0]
    max_len = max(len(our_time_text), len(mitsuba2_time_text))
    # our_time_text = ' ' * (max_len - len(our_time_text)) + our_time_text
    # mitsuba2_time_text = ' ' * (max_len - len(mitsuba2_time_text)) + mitsuba2_time_text
    final_picture_ax.text(50, 50, f'Final', va="top", color="white")
    final_picture_ax.text(50, 100, f'{our_time_text}\n{mitsuba2_time_text}', va="top", color="white", fontsize="smaller")

    target_picture_ax.imshow(target_image)
    initial_picture_ax.imshow(initial_image)
    final_picture_ax.imshow(final_image)

    LuisaRender_diff_time = LuisaRender_time[1:]
    Mitsuba2_diff_time = Mitsuba2_time[1:]
    handle_labels = ['Ours', 'Mitsuba 2']
    data = [LuisaRender_diff_time, Mitsuba2_diff_time]
    group_num = len(data)
    group_len = len(data[0])
    bar_width = 0.8 / group_len
    x_ticks = np.arange(group_num)

    for i in range(group_len):
        intervals = [x + bar_width * (i + 0.5) - bar_width * 0.5 * group_num for x in x_ticks]
        compare_ax.bar(
            intervals,
            data[i],
            label=handle_labels[i],
            width=bar_width,
        )
        for x, y in zip(intervals, data[i]):
            compare_ax.text(x, y, f"{y:.1f}", ha="center", va="bottom", fontsize="smaller")

    compare_ax.legend(loc="upper left", fontsize="smaller")
    x_labels = ["forward time", 'backward time']
    compare_ax.set_xticks(x_ticks, x_labels, va="top")
    compare_ax.set_ylabel('Average time (s) / iteration')
    compare_ax.yaxis.tick_right()
    compare_ax.grid(axis="y", linewidth=2, alpha=0.4)

    plt.show()
    fig.savefig(f"{folder}/cbox-diff.pdf", dpi=1000, bbox_inches='tight', pad_inches=0.2)


if __name__ == '__main__':
    plot_diff()
