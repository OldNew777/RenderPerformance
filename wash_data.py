import csv

backend_mapping = {
    'cpu': 'ISPC',
    'directX': 'DirectX',
    'cuda': 'CUDA',
}
integrator_mapping = {
    'MegaPath': 'Mega-kernel',
    'WavePath': 'Wavefront',
}


def wash_data():
    results = []
    data = {}
    with open('outputs/results-breakdown.csv', 'r', newline='') as f:
        f_csv = csv.reader(f)
        index = 0
        for line in f_csv:
            if index == 0:
                results.append(line)
            else:
                settings = line[:4]
                settings[1] = backend_mapping[settings[1]]
                settings[2] = integrator_mapping[settings[2]]
                line_text = ','.join(settings)
                if line_text not in data:
                    data[line_text] = {
                        'settings': settings,
                        'count': 0,
                        'time': [0., 0., 0., 0.],
                    }
                data[line_text]['count'] += 1
                for i in range(4):
                    data[line_text]['time'][i] += float(line[4 + i])
            index += 1

    print(results)
    print(data)

    for value in data.values():
        for i in range(len(value['time'])):
            value['time'][i] /= value['count']
        results.append(value['settings'] + value['time'])

    print(results)
    with open('outputs/results-breakdown-washed-all.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)


def wash_data_brief():
    results = [['scene', 'Scene parse time (ms)', 'Scene load time (ms)', 'Pipeline create time (ms)',
                'Shader compile time (ms)']]
    data = {}
    with open('outputs/results-breakdown.csv', 'r', newline='') as f:
        f_csv = csv.reader(f)
        index = 0
        for line in f_csv:
            if index > 0:
                settings = [line[1]]
                settings[0] = backend_mapping[settings[0]]
                line_text = ','.join(settings)
                if line_text not in data:
                    data[line_text] = {
                        'settings': settings,
                        'count': 0,
                        'time': [0., 0., 0., 0.],
                    }
                data[line_text]['count'] += 1
                for i in range(4):
                    data[line_text]['time'][i] += float(line[4 + i])
            index += 1

    print(results)
    print(data)

    for value in data.values():
        for i in range(len(value['time'])):
            value['time'][i] /= value['count']
        results.append(value['settings'] + value['time'])

    print(results)
    with open('outputs/results-breakdown-washed-brief.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)


if __name__ == '__main__':
    # wash_data()
    wash_data_brief()
