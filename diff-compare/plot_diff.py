import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.image as imread
from matplotlib import rcParams
import os

import tonemapping as tm
import plt_config

font_size = 15
rcParams["font.size"] = font_size

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv
import numpy as np


def read_hdr2ldr(filename: str) -> np.ndarray:
    image = np.maximum(
        np.nan_to_num(cv.imread(filename, cv.IMREAD_UNCHANGED)[:, :, :3], nan=0.0, posinf=1e3, neginf=0), 0.0)
    image = tm.tonemapping_uncharted2(image * 1.5)
    image_srgb = np.uint8(np.round(np.clip(np.where(
        image <= 0.00304,
        12.92 * image,
        1.055 * np.power(image, 1.0 / 2.4) - 0.055
    ) * 255, 0, 255)))
    image_srgb = cv.cvtColor(image_srgb, cv.COLOR_BGR2RGB)
    return image_srgb


def plot_diff():
    fig = plt.figure(figsize=(15, 3.6), constrained_layout=True)

    LuisaRender_time = [121.8529209, 0.489846352, 0.7286828565]
    Mitsuba2_time = [1050.295172, 4.489018485, 6.013933237]
    folder = 'diff-compare'
    target_image = read_hdr2ldr(f"target-1024-1024spp.exr")
    initial_image = read_hdr2ldr(f"initial-1024-64spp.exr")
    optimizing_image = read_hdr2ldr(f"optimizing-1024-64spp-iter2.exr")
    final_image = read_hdr2ldr(f"final-1024-64spp.exr")
    images = [target_image, initial_image, final_image]

    gs = fig.add_gridspec(nrows=1, ncols=5, width_ratios=[1, 1, 1, 1, 1], wspace=0.03)
    # picture_gs = gs[0, 0].subgridspec(nrows=1, ncols=3, width_ratios=[x.shape[1] / x.shape[0] for x in images], wspace=0)
    target_picture_ax = fig.add_subplot(gs[0, 0])
    initial_picture_ax = fig.add_subplot(gs[0, 1])
    optimizing_picture_ax = fig.add_subplot(gs[0, 2])
    final_picture_ax = fig.add_subplot(gs[0, 3])
    compare_ax = fig.add_subplot(gs[0, 4])

    # compare_gs = gs[0, 1].subgridspec(nrows=2, ncols=1, height_ratios=[1, 25], hspace=0)
    # compare_ax = fig.add_subplot(compare_gs[1, 0])

    def turn_off_spines(ax):
        ax.set_frame_on(False)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

    turn_off_spines(target_picture_ax)
    turn_off_spines(initial_picture_ax)
    turn_off_spines(optimizing_picture_ax)
    turn_off_spines(final_picture_ax)

    target_picture_ax.set_title('Target', fontsize=font_size)
    target_picture_ax.set_xlabel(f'''Resolution: $1024\\times1024$''', fontsize=font_size)
    initial_picture_ax.set_title('Initial', fontsize=font_size)
    initial_picture_ax.set_xlabel("Iterations #0", fontsize=font_size)
    optimizing_picture_ax.set_title("Optimizing", fontsize=font_size)
    optimizing_picture_ax.set_xlabel("Iteration #2\n(64spp per iteration)", fontsize=font_size)
    final_picture_ax.set_title('Final', fontsize=font_size)
    final_picture_ax.set_xlabel(f'''Iteration #99
Ours: {LuisaRender_time[0]:.0f}s / Mitsuba 2: {Mitsuba2_time[0]:.0f}s''', fontsize=font_size)
    # our_time_text = 'Ours: %.0fs' % LuisaRender_time[0]
    # mitsuba2_time_text = 'Mitsuba2 time: %.0fs' % Mitsuba2_time[0]
    # max_len = max(len(our_time_text), len(mitsuba2_time_text))
    # final_picture_ax.text(50, 100, f'{our_time_text}\n{mitsuba2_time_text}', va="top", color="white",
    # fontsize=font_size)

    target_picture_ax.imshow(target_image)
    initial_picture_ax.imshow(initial_image)
    optimizing_picture_ax.imshow(optimizing_image)
    final_picture_ax.imshow(final_image)

    LuisaRender_diff_time = LuisaRender_time[1:]
    Mitsuba2_diff_time = Mitsuba2_time[1:]
    handle_labels = ['Ours', 'Mitsuba 2']
    x_labels = ["Forward", 'Backward']
    data = [LuisaRender_diff_time, Mitsuba2_diff_time]
    group_num = len(data)
    group_len = len(data[0])
    bar_width = 0.75 / group_len
    space_width = 0.03 / (group_len - 1)
    x_ticks = np.arange(group_num)

    our_color = "#f3724a"
    mi2_color = "#4b8a2c"
    colors = [our_color, mi2_color]
    for i in range(group_len):
        intervals = [x + (bar_width + space_width) * (i + 0.5) - (bar_width + space_width) * 0.5 * group_num for x in x_ticks]
        compare_ax.bar(
            intervals,
            data[i],
            label=handle_labels[i],
            width=bar_width,
            color=colors[i]
        )
        for x, y in zip(intervals, data[i]):
            compare_ax.text(x, y, f"{y:.1f}", ha="center", va="bottom", fontsize=font_size)

    compare_ax.legend(loc="upper left", fontsize=font_size)
    compare_ax.set_xticks(x_ticks, x_labels)
    compare_ax.set_title('Average iteration time', fontsize=font_size)
    compare_ax.yaxis.tick_right()
    y_ticks = np.arange(0, 10, 2)
    compare_ax.set_yticks(y_ticks, labels=[f"{x}s" for x in y_ticks])
    compare_ax.grid(axis="y", linewidth=2, alpha=0.4)
    compare_ax.set_ylim(0, 7)
    compare_ax.set_xlim(-0.65, 1.65)

    plt.show()
    fig.savefig(f"cbox-diff.pdf", dpi=600, bbox_inches='tight')


if __name__ == '__main__':
    plot_diff()
