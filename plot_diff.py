import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.image as imread
import os

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
    font_manager.fontManager.addfont('Linux-Biolinum.ttf')
    plt.rcParams['font.family'] = 'Linux Biolinum'
    fig = plt.figure(figsize=(20, 6), constrained_layout=True)

    LuisaRender_time = [121.8529209, 0.489846352, 0.7286828565]
    Mitsuba2_time = [1050.295172, 4.489018485, 6.013933237]
    x_labels = ["Ours (RBP)", 'Mitsuba2 (RBP)']
    folder = 'diff-compare'
    target_image = read_hdr2ldr(f"{folder}/target-1024-1024spp.exr")
    initial_image = read_hdr2ldr(f"{folder}/initial-1024-64spp.exr")
    final_image = read_hdr2ldr(f"{folder}/final-1024-64spp.exr")

    forward_time = [LuisaRender_time[1], Mitsuba2_time[1]]
    backward_time = [LuisaRender_time[2], Mitsuba2_time[2]]

    gs = plt.GridSpec(nrows=1, ncols=4, figure=fig, width_ratios=[2, 2, 2, 1], wspace=0, hspace=0)
    target_picture_ax = fig.add_subplot(gs[0, 0])
    initial_picture_ax = fig.add_subplot(gs[0, 1])
    final_picture_ax = fig.add_subplot(gs[0, 2])
    compare_ax = fig.add_subplot(gs[0, 3])

    target_picture_ax.get_xaxis().set_visible(False)
    target_picture_ax.get_yaxis().set_visible(False)
    initial_picture_ax.get_xaxis().set_visible(False)
    initial_picture_ax.get_yaxis().set_visible(False)
    final_picture_ax.get_xaxis().set_visible(False)
    final_picture_ax.get_yaxis().set_visible(False)

    target_picture_ax.set_title('target', y=-0.07)
    initial_picture_ax.set_title('initial', y=-0.07)
    our_time_text = 'Our time: %.2fs' % LuisaRender_time[0]
    mitsuba2_time_text = 'Mitsuba2 time: %.2fs' % Mitsuba2_time[0]
    max_len = max(len(our_time_text), len(mitsuba2_time_text))
    our_time_text = ' ' * (max_len - len(our_time_text)) + our_time_text
    mitsuba2_time_text = ' ' * (max_len - len(mitsuba2_time_text)) + mitsuba2_time_text
    final_picture_ax.set_title(f'final\n{our_time_text}\n{mitsuba2_time_text}', y=-0.15)

    target_picture_ax.imshow(target_image)
    initial_picture_ax.imshow(initial_image)
    final_picture_ax.imshow(final_image)
    compare_ax.bar(
        x_labels,
        forward_time,
        width=0.4,
        label='forward time',
    )
    compare_ax.bar(
        x_labels,
        backward_time,
        width=0.4,
        bottom=forward_time,
        label='backward time',
    )
    compare_ax.legend()
    compare_ax.set_ylabel('Average time (s) / iteration')
    baseline = min(min(forward_time), min(backward_time))
    for x_label, forward_seconds, backward_seconds in zip(x_labels, forward_time, backward_time):
        compare_ax.text(x_label, forward_seconds * 0.5, '%.1fX' % (forward_seconds / baseline), ha='center',
                        va='center')
        compare_ax.text(x_label, forward_seconds + backward_seconds * 0.5, '%.1fX' % (backward_seconds / baseline),
                        ha='center', va='center')

    plt.show()
    fig.savefig(f"{folder}/cbox-diff.pdf", dpi=1000, bbox_inches='tight', pad_inches=0.2)


if __name__ == '__main__':
    plot_diff()
