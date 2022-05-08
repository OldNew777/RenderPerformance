import os

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

settings = {
    'rr_max_depth': [
        {
            'rr depth': 2,
            'max depth': 8,
        },
        {
            'rr depth': 5,
            'max depth': 16,
        },
    ],
    'scene': [
        # 'living-room',
        'coffee',
        'glass-of-water',
        'spaceship',
        'staircase',
    ],
}

hue_order = [
    # GPU
    'LuisaRender-directX-WavePath',
    'LuisaRender-directX-MegaPath',
    'LuisaRender-cuda-WavePath',
    'LuisaRender-cuda-MegaPath',
    # 'LuisaRender-metal-WavePath',
    # 'LuisaRender-metal-MegaPath',
    'PBRT-v4-cuda-WavePath',
    'PBRT-v4-cuda-MegaPath',
    'Mitsuba2-cuda-WavePath',
    'Mitsuba2-cuda-MegaPath',

    # CPU
    'LuisaRender-cpu-WavePath',
    'LuisaRender-cpu-MegaPath',
    'PBRT-v4-cpu-WavePath',
    'PBRT-v4-cpu-MegaPath',
    'Mitsuba2-cpu-WavePath',
    'Mitsuba2-cpu-MegaPath',
]


def load_data(csv_path) -> list:
    raw = pd.read_csv(csv_path)
    # wash data
    raw = raw[raw['time consumption'] != 'Error']

    def get_hue(df):
        return f"{df['render']}-{df['backend']}-{df['integrator']}"

    def get_seconds(df):
        time_consumption = df['time consumption']
        unit = time_consumption[-1]
        value = float(time_consumption[:-1])
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60.
        else:
            raise Exception(f'results parse error in "{time_consumption}"')

    raw.loc[:, 'seconds'] = raw.apply(get_seconds, axis=1)
    raw.loc[:, 'hue'] = raw.apply(get_hue, axis=1)
    raw = raw[raw['scene'].isin(settings['scene'])]

    ans = []
    data_filtered = [pd.DataFrame({}) for i in range(100)]
    description = {}

    # separate data into several parts
    for spectrum in set(raw['spectrum']):
        k = 0
        description['spectrum'] = spectrum
        data = raw
        data_filtered[k] = data[data['spectrum'] == spectrum]

        for setting in settings['rr_max_depth']:
            k = 1
            rr_depth = setting['rr depth']
            max_depth = setting['max depth']
            description['rr depth'] = rr_depth
            description['max depth'] = max_depth
            data = data_filtered[k - 1]
            data_filtered[k] = data[(data['rr depth'] == rr_depth) & (data['max depth'] == max_depth)]

            ans.append((data_filtered[k], description.copy()))

    return ans


def plot(data_list: list):
    sns.set_theme(style='whitegrid')
    sns.set_color_codes("bright")
    myfont = fm.FontProperties(fname='Linux-Biolinum.ttf')
    sns.set(font=myfont.get_family())

    for data, description in data_list:
        plt.figure(figsize=(10, 8))

        # get existing hue
        hue_order_temp = []
        for hue in hue_order:
            if hue in set(data['hue']):
                hue_order_temp.append(hue)

        ax = sns.barplot(data=data, x='scene', y='seconds', hue='hue', hue_order=hue_order_temp, orient='v')

        # get ylim/time_min
        time_arr = np.zeros(0, dtype=np.float64)
        time_min = ax.containers[0].datavalues
        ylim = ax.containers[0].datavalues
        for container in ax.containers:
            time_min = np.minimum(time_min, container.datavalues)
            ylim = np.maximum(ylim, container.datavalues)
            time_arr = np.append(time_arr, container.datavalues)
        ylim = max(set(time_arr) - set(ylim)) * 2

        magnifications_all = []
        for container in ax.containers:
            magnifications_all.append(container.datavalues / time_min)

        # clear figure drew during the first pass
        plt.clf()
        plt.cla()
        # trim figure to certain height
        plt.ylim([0, ylim])
        # trim data to that height so that we can see labels
        data['seconds'] = np.minimum(data['seconds'], np.ones(shape=len(data['seconds']), dtype=np.float64) * ylim)
        ax = sns.barplot(data=data, x='scene', y='seconds', hue='hue', hue_order=hue_order_temp, orient='v')

        # add labels
        index = 0
        for container in ax.containers:
            magnifications = magnifications_all[index]
            exceeds = magnifications * time_min > container.datavalues + 5
            labels = []
            for magnification, exceed in zip(magnifications, exceeds):
                if exceed:
                    labels.append('%.1fx\n/\\\n|' % magnification)
                else:
                    labels.append('%.1fx' % magnification)
            ax.bar_label(container, labels=labels)
            index += 1

        # format
        ax.legend_.set_title(None)
        plt.setp(ax.get_legend().get_texts(), fontsize=18)
        plt.xlabel('scene', fontsize=18)
        plt.ylabel('time(seconds)', fontsize=18)
        plt.show()

        # save
        ax.get_figure().savefig(
            f"outputs/figures/{description['spectrum']}-{description['rr depth']}rr_depth-{description['max depth']}max_depth.pdf",
            dpi=1000)


if __name__ == '__main__':
    data_all = load_data('outputs/results-all.csv')
    plot(data_all)
