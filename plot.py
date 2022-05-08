import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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
    ]
}


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
    for data, description in data_list:
        fig = sns.barplot(data=data, x='scene', y='seconds', hue='hue')
        plt.show()
        fig.get_figure().savefig(
            f"outputs/pictures/{description['spectrum']}-{description['rr depth']}rr_depth-{description['max depth']}max_depth.png",
            dpi=1000)


if __name__ == '__main__':
    data_all = load_data()
    print(data_all)
    plot(data_all)
