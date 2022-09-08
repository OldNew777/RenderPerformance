import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.image as imread
from matplotlib import rcParams
import os

import image_process
import plt_config
import relMSE

font_size = 15
rcParams["font.size"] = font_size

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv
import numpy as np


def read_hdr2ldr(filename: str) -> np.ndarray:
    image = np.maximum(
        np.nan_to_num(cv.imread(filename, cv.IMREAD_UNCHANGED)[:, :, :3], nan=0.0, posinf=1e3, neginf=0), 0.0)
    image = image_process.tonemapping_uncharted2(image * 1.5)
    image_srgb = np.uint8(np.round(np.clip(np.where(
        image <= 0.00304,
        12.92 * image,
        1.055 * np.power(image, 1.0 / 2.4) - 0.055
    ) * 255, 0, 255)))
    image_srgb = cv.cvtColor(image_srgb, cv.COLOR_BGR2RGB)
    return image_srgb


def plot_diff():
    fig = plt.figure(figsize=(13, 4.2), constrained_layout=True)

    LuisaRender_time = [4280.144527, 3.408386043, 7.291975275]
    Mitsuba3_time = [16417.86908, 11.80204352, 29.24262918]
    folder = 'staircase'
    target_image_name = os.path.join(folder, "target-720-16384spp.exr")
    initial_image_name = os.path.join(folder, "initial-720-512spp.exr")
    optimizing_image_name = os.path.join(folder, "optimizing-720-512spp-iter3.exr")
    final_image_name = os.path.join(folder, "final-720-16384spp.exr")
    target_image = read_hdr2ldr(target_image_name)
    initial_image = read_hdr2ldr(initial_image_name)
    optimizing_image = read_hdr2ldr(optimizing_image_name)
    final_image = read_hdr2ldr(final_image_name)
    rel_mse, diff_image = relMSE.relMSE(
        cv.imread(target_image_name, cv.IMREAD_UNCHANGED),
        cv.imread(final_image_name, cv.IMREAD_UNCHANGED))
    # images = [target_image, initial_image, final_image]

    gs = fig.add_gridspec(nrows=1, ncols=6, width_ratios=[1, 1, 1, 1, 1, 1.5], wspace=0.03)
    # picture_gs = gs[0, 0].subgridspec(nrows=1, ncols=3, width_ratios=[x.shape[1] / x.shape[0] for x in images], wspace=0)
    target_picture_ax = fig.add_subplot(gs[0, 0])
    initial_picture_ax = fig.add_subplot(gs[0, 1])
    optimizing_picture_ax = fig.add_subplot(gs[0, 2])
    final_picture_ax = fig.add_subplot(gs[0, 3])
    diff_picture_ax = fig.add_subplot(gs[0, 4])
    compare_ax = fig.add_subplot(gs[0, 5])

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
    turn_off_spines(diff_picture_ax)

    target_picture_ax.set_title('Target', fontsize=font_size)
    target_picture_ax.set_xlabel(f'''Resolution: $720\\times1280$''', fontsize=font_size)
    initial_picture_ax.set_title('Initial', fontsize=font_size)
    initial_picture_ax.set_xlabel("Iterations #0", fontsize=font_size)
    optimizing_picture_ax.set_title("Optimizing", fontsize=font_size)
    optimizing_picture_ax.set_xlabel("Iteration #2\n(512spp per iteration)", fontsize=font_size)
    final_picture_ax.set_title('Final', fontsize=font_size)
    final_picture_ax.set_xlabel(f'Ours: {LuisaRender_time[0]/3600:.2f}h\nMitsuba 3: {Mitsuba3_time[0]/3600:.2f}h', fontsize=font_size)
    diff_picture_ax.set_title("Difference", fontsize=font_size)
    diff_picture_ax.set_xlabel(f"\n\nrelMSE = {rel_mse:.3e}", fontsize=font_size)
    # our_time_text = 'Ours: %.0fs' % LuisaRender_time[0]
    # mitsuba3_time_text = 'Mitsuba3 time: %.0fs' % Mitsuba3_time[0]
    # max_len = max(len(our_time_text), len(mitsuba3_time_text))
    # final_picture_ax.text(50, 100, f'{our_time_text}\n{mitsuba3_time_text}', va="top", color="white",
    # fontsize=font_size)

    target_picture_ax.imshow(target_image)
    initial_picture_ax.imshow(initial_image)
    optimizing_picture_ax.imshow(optimizing_image)
    final_picture_ax.imshow(final_image)
    diff_picture_ax.imshow(diff_image)
    relMSE.add_colorbar(np.clip(diff_image, 0, 0.002), diff_picture_ax, fig)

    LuisaRender_diff_time = LuisaRender_time[1:]
    Mitsuba3_diff_time = Mitsuba3_time[1:]
    handle_labels = ['Ours', 'Mitsuba 3']
    x_labels = ["Forward", 'Backward']
    data = [LuisaRender_diff_time, Mitsuba3_diff_time]
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
    compare_ax.set_title('Average iteration time (s)', fontsize=font_size)
    compare_ax.yaxis.tick_right()
    y_ticks = np.arange(0, 40, 10)
    compare_ax.set_yticks(y_ticks, labels=[f"{x}" for x in y_ticks])
    compare_ax.grid(axis="y", linewidth=2, alpha=0.4)
    compare_ax.set_ylim(0, 33)
    compare_ax.set_xlim(-0.65, 1.65)

    plt.show()
    fig.savefig(f"staircase-diff.pdf", dpi=600, bbox_inches='tight')


if __name__ == '__main__':
    plot_diff()
