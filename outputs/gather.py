import csv


def gather():
    input_path = [
        'results-LuisaRender.csv',
        'results-Mitsuba2.csv',
        'results-PBRT-v4.csv',
    ]
    output_path = 'results-all.csv'
    headers = []
    data = []
    for path in input_path:
        with open(path, 'r') as f:
            f_csv = csv.reader(f)
            line = 0
            for row in f_csv:
                if line == 0:
                    headers = row
                else:
                    data.append(row)
                line += 1
    with open(output_path, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(data)


if __name__ == '__main__':
    gather()
