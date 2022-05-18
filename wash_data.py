import csv


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
                line_text = ','.join(line[:4])
                if line_text not in data:
                    data[line_text] = {
                        'settings': line[:4],
                        'count': 0,
                        'time': [0., 0., 0., 0.],
                    }
                data[line_text]['count'] += 1
                for i in range (4):
                    data[line_text]['time'][i] += float(line[4 + i])
            index += 1

    print(results)
    print(data)

    for value in data.values():
        for i in range(len(value['time'])):
            value['time'][i] /= value['count']
        results.append(value['settings'] + value['time'])

    print(results)
    with open('outputs/results-breakdown-washed.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)


if __name__ == '__main__':
    wash_data()
