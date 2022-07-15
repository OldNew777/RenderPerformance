import matplotlib.pyplot as plt
from matplotlib import rcParams

import plt_config

font_size = 17
rcParams["font.size"] = font_size


def plot_hash_slots():
    x = [64, 128, 256, 512, 1024, 2048]
    y = [34.49, 9.46, 3.2, 1.51, 1.5, 1.42]

    fig = plt.figure(figsize=(8, 6), constrained_layout=True)
    sub_axis = fig.add_subplot()
    sub_axis.plot(x, y, color="orange", marker='o',
                  linestyle='-', linewidth=2, markersize=8)

    sub_axis.set_xlabel('Hash slot size')
    sub_axis.set_ylabel('Average iteration time (in seconds)')

    # 用x,y绘制折现，横坐标采取log2(x)，纵坐标采取y
    sub_axis.set_xscale('log')
    sub_axis.set_xticks(x, x)
    sub_axis.set_ylim(0, max(y) * 1.2)
    sub_axis.grid(axis="y", linewidth=2, alpha=0.3)
    sub_axis.minorticks_off()

    for dx, dy in zip(x, y):
        sub_axis.text(dx, dy + 3, f"{dy:.2f}", ha="center", va="bottom", fontsize=font_size)

    plt.show()
    fig.savefig(f"hash_slots.pdf", dpi=600, bbox_inches='tight')
    fig.savefig(f"hash_slots.png", dpi=600, bbox_inches='tight')


if __name__ == '__main__':
    plot_hash_slots()
