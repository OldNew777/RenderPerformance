import re
import csv


def gather_breakdown():
    with open('results.txt', 'r') as f:
        text = f.readlines()

    results = []
    with open('outputs/results.csv', 'r', newline='') as f:
        f_csv = csv.reader(f)
        for line in f_csv:
            results.append(line)
    results[0] += ['Scene parse time (ms)', 'Scene load time (ms)',
                   'Pipeline create time (ms)', 'Shader compile time (ms)']

    state = -1
    line_index = 0
    scene_parse_time = 0.
    scene_load_time = 0.
    pipeline_create_time = 0.
    shader_compile_time = 0.
    for line in text:
        if line.startswith('Argv'):
            if state != -1:
                while results[line_index][0] != 'LuisaRender':
                    line_index += 1
                results[line_index] += [
                    scene_parse_time, scene_load_time,
                    pipeline_create_time, shader_compile_time
                ]
            line_index += 1
            state = 0
            scene_parse_time = 0.
            scene_load_time = 0.
            pipeline_create_time = 0.
            shader_compile_time = 0.
        elif line.startswith('Scene parse time'):
            scene_parse_time = float(re.search('= ([0-9\.]*) ms', line).group(1))
        elif line.startswith('Scene load time'):
            scene_load_time = float(re.search('= ([0-9\.]*) ms', line).group(1))
        elif line.startswith('Pipeline create time'):
            pipeline_create_time = float(re.search('= ([0-9\.]*) ms', line).group(1))
        elif line.startswith('Shader compile time'):
            shader_compile_time += float(re.search('= ([0-9\.]*) ms', line).group(1))

    if len(results) > line_index:
        results[line_index] += [
            scene_parse_time, scene_load_time,
            shader_compile_time, pipeline_create_time,
        ]

    with open('outputs/results.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)

    wash_breakdown()


def wash_breakdown():
    results = []
    with open('outputs/results.csv', 'r', newline='') as f:
        f_csv = csv.reader(f)
        data = set()
        for line in f_csv:
            line_text = ','.join(line[:10])
            if line_text not in data:
                results.append(line)
                data.add(line_text)

    with open('outputs/results.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)


if __name__ == '__main__':
    gather_breakdown()
