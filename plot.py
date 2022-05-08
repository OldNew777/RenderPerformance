import seaborn as sns
import matplotlib.pyplot as plt
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


def load_data() -> list:
    csv_path = 'outputs/results-all.csv'
    raw = pd.read_csv(csv_path)

    def get_hue(df):
        return f"{df['render']}-{df['backend']}-{df['integrator']}"

    raw.loc[:, 'hue'] = raw.apply(get_hue, axis=1)
    raw = raw[raw['scene'].map(lambda x: x in settings['scene'])]

    ans = []
    data_filtered = [pd.DataFrame({}) for i in range(100)]
    description = {}

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

    for data, description in data_list:
        plt.figure(figsize=(10, 8))

        hue_order_temp = []
        for hue in hue_order:
            if hue in set(data['hue']):
                hue_order_temp.append(hue)

        g = sns.barplot(data=data, x='scene', y='seconds', hue='hue', hue_order=hue_order_temp, orient='v')

        time_arr = np.zeros(0, dtype=np.float64)
        time_min = g.containers[0].datavalues
        ylim = g.containers[0].datavalues
        for container in g.containers:
            time_min = np.minimum(time_min, container.datavalues)
            ylim = np.maximum(ylim, container.datavalues)
            time_arr = np.append(time_arr, container.datavalues)
        ylim = max(set(time_arr) - set(ylim)) * 2
        labels = []
        for container in g.containers:
            labels_t = []
            values = container.datavalues / time_min
            for value in values:
                labels_t.append('%.1fx' % value)
            labels.append(labels_t)

        plt.clf()
        plt.cla()
        plt.ylim([0, ylim])
        data['seconds'] = np.minimum(data['seconds'], np.ones(shape=len(data['seconds']), dtype=np.float64) * ylim)
        g = sns.barplot(data=data, x='scene', y='seconds', hue='hue', hue_order=hue_order_temp, orient='v')

        index = 0
        for container in g.containers:
            g.bar_label(container, labels=labels[index])
            index += 1
        plt.show()

        g.get_figure().savefig(
            f"outputs/figures/{description['spectrum']}-{description['rr depth']}rr_depth-{description['max depth']}max_depth.png",
            dpi=1000)


if __name__ == '__main__':
    data_all = load_data()
    plot(data_all)
