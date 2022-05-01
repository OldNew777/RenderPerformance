import os
import re
import csv

renderer_settings = {
    'LuisaRender': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/LuisaRender/cmake-build-release/bin/luisa-render-cli.exe',
            'spectrum': 'undefined',
            'integrator': {
                'name': {
                    'WavePath': '',
                    'MegaPath': '',
                },
                'order': '{}',
            },
            'device': '-d {}',
            'output': '',
            'appendix': '-b dx',
        },
        'scene_file': {
            'scene_file_name': 'scene.luisa',
            'output_file': {
                'regex': 'file { "output\.exr" }',
                'replace': 'file {{ "{}.exr" }}',
            },
            'resolution': [
                {
                    'regex': 'resolution { [, 0-9]* }',
                    'replace': 'resolution {{ {} }}'
                },
            ],
            'max_depth': {
                'regex': 'depth { [0-9]* }',
                'replace': 'depth {{ {} }}',
            },
            'spp': {
                'regex': 'spp { [0-9]* }',
                'replace': 'spp {{ {} }}',
            },
            'sampler': {
                'name': {
                    'Independent': 'Independent',
                },
                'regex': 'sampler : [a-zA-Z]* \{\}',
                'replace': 'sampler : {} {{}}',
            },
            'spectrum': {
                'name': {
                    'RGB': 'sRGB',
                    'Spectral': 'Hero',
                },
                'regex': 'spectrum : [a-zA-Z]* \{\}',
                'replace': 'spectrum : {} {{}}',
            },
            'integrator': {
                'name': {
                    'WavePath': 'WavePath',
                    'MegaPath': 'MegaPath',
                },
                'regex': 'integrator : [a-zA-Z]* {',
                'replace': 'integrator : {} {{',
            },
        },
        'results_regex': {
            'time': '\(([0-9a-zA-Z\.]*) \| 100\.0%\)',
        },
    },
    'Mitsuba2': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/Mitsuba2/build/dist/mitsuba.exe',
            'spectrum': {
                'name': {
                    'RGB': 'gpu_rgb',
                    'Spectral': 'gpu_spectral',
                },
                'order': '-m {}',
            },
            'integrator': {
                'name': {
                    'WavePath': '',
                    'MegaPath': '',
                },
                'order': '{}',
            },
            'device': 'undefined',
            'output': '--output {}',
            'appendix': '',
        },
        'scene_file': {
            'scene_file_name': 'scene.xml',
            'output_file': {
                'regex': '<string name="filename" value="output\.exr" />',
                'replace': '<string name="filename" value="{}.exr" />',
            },
            'resolution': [
                {
                    'regex': '<integer name="width" value="[0-9]*" />',
                    'replace': '<integer name="width" value="{}" />',
                },
                {
                    'regex': '<integer name="height" value="[0-9]*" />',
                    'replace': '<integer name="height" value="{}" />',
                },
            ],
            'max_depth': {
                'regex': '<integer name="max_depth" value="[0-9]*" />',
                'replace': '<integer name="max_depth" value="{}" />',
            },
            'spp': {
                'regex': '<integer name="sample_count" value="[0-9]*" />',
                'replace': '<integer name="sample_count" value="{}" />',
            },
            'sampler': {
                'name': {
                    'Independent': 'independent',
                },
                'regex': '<sampler type="[a-zA-Z]*" >',
                'replace': '<sampler type="{}" >',
            },
            'spectrum': 'undefined',
            'integrator': {
                'name': {
                    'WavePath': 'path',
                    'MegaPath': 'undefined',
                },
                'regex': '<integrator type="[a-zA-Z]*" >',
                'replace': '<integrator type="{}" >',
            },
        },
        'results_regex': {
            'time': 'Rendering finished\. \(took ([0-9a-zA-Z\.]*)\)',
        },
    },
    'PBRT-v4': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/pbrt-v4/build-vs/Release/pbrt.exe',
            'spectrum': {
                'name': {
                    'RGB': 'undefined',
                    'Spectral': '',
                },
                'order': '{}',
            },
            'integrator': {
                'name': {
                    'WavePath': '--wavefront',
                    'MegaPath': '',
                },
                'order': '{}',
            },
            'device': '--gpu-device {}',
            'output': '',
            'appendix': '',
        },
        'scene_file': {
            'scene_file_name': 'scene-v4.pbrt',
            'output_file': {
                'regex': '"string filename" \[ "output\.exr" \]',
                'replace': '"string filename" [ "{}.exr" ]',
            },
            'resolution': [
                {
                    'regex': '"integer xresolution" \[ [0-9]* \]',
                    'replace': '"integer xresolution" [ {} ]',
                },
                {
                    'regex': '"integer yresolution" \[ [0-9]* \]',
                    'replace': '"integer yresolution" [ {} ]',
                },
            ],
            'max_depth': {
                'regex': '"integer maxdepth" \[ [0-9]* \]',
                'replace': '"integer maxdepth" [ {} ]',
            },
            'spp': {
                'regex': '"integer pixelsamples" \[ [0-9]* \]',
                'replace': '"integer pixelsamples" [ {} ]',
            },
            'sampler': {
                'name': {
                    'Independent': 'independent',
                },
                'regex': 'Sampler "[a-zA-Z]*"',
                'replace': 'Sampler "{}"',
            },
            'spectrum': 'undefined',
            'integrator': {
                'name': {
                    'WavePath': 'path',
                    'MegaPath': 'undefined',
                },
                'regex': 'Integrator "[a-zA-Z]*"',
                'replace': 'Integrator "{}"',
            },
        },
        'results_regex': {
            'time': 'Rendering: \[[\+]*\]  \(([0-9a-zA-Z\.]*)\)',
        },
    },
}

target_settings = {
    'renderer': [
        # 'LuisaRender',
        # 'Mitsuba2',
        'PBRT-v4',
    ],
    'scene': {
        # 'classroom': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        'coffee': {
            'resolution': [
                (800, 1000),
            ],
        },
        # 'dining-room': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        'glass-of-water': {
            'resolution': [
                (1920, 1080),
            ],
        },
        'living-room': {
            'resolution': [
                (1920, 1080),
            ],
        },
        'spaceship': {
            'resolution': [
                (1920, 1080),
            ],
        },
        'staircase': {
            'resolution': [
                (720, 1280),
            ],
        },
    },
    'integrator': [
        'WavePath',
        'MegaPath',
    ],
    'spectrum': [
        'RGB',
        'Spectral',
    ],
    'sampler': [
        'Independent',
    ],
    'spp': [
        16,
        64,
        256,
        1024,
        4096,
    ],
    'max_depth': [
        12,
        16,
    ],
}


def test_targets():
    results = []
    results_save_file_path = os.path.join(os.path.dirname(__file__), 'outputs', 'results.csv')
    errors_save_file_path = os.path.join(os.path.dirname(__file__), 'outputs', 'errors.txt')
    error_index = 0
    scene = ['' for i in range(100)]
    order = ['' for i in range(100)]

    with open(results_save_file_path, 'w', newline='') as f:
        # init results-saving file
        f_csv = csv.writer(f)
        header = ['render', 'scene', 'integrator', 'sampler', 'resolution', 'spp', 'max depth', 'spectrum',
                  'time consumption']
        f_csv.writerow(header)
    with open(errors_save_file_path, 'w') as f:
        # init errors-saving file
        pass

    for renderer in target_settings['renderer']:
        k = 0

        settings = renderer_settings[renderer]

        order[k] = settings['exe']['path'] + ' ' + settings['exe']['appendix']

        for scene_name, scene_targets in target_settings['scene'].items():
            k = 1

            render_directory = os.path.join(os.path.realpath(os.path.dirname(__file__)), renderer)
            scene_directory = os.path.join(render_directory, scene_name)
            scene_file_settings = settings['scene_file']
            scene_file_path = os.path.join(scene_directory, scene_file_settings['scene_file_name'])

            with open(scene_file_path, 'r') as scene_file:
                scene[k] = scene_file.read()
            order[k] = order[k - 1]

            for integrator in target_settings['integrator']:
                k = 2

                integrator_name = scene_file_settings['integrator']['name'][integrator]
                if integrator_name == 'undefined':
                    continue
                scene[k] = re.sub(scene_file_settings['integrator']['regex'],
                                  scene_file_settings['integrator']['replace'].
                                  format(integrator_name), scene[k - 1])
                order[k] = order[k - 1] + ' ' + settings['exe']['integrator']['order'].format(
                    settings['exe']['integrator']['name'][integrator])

                for sampler in target_settings['sampler']:
                    k = 3

                    scene[k] = re.sub(scene_file_settings['sampler']['regex'],
                                      scene_file_settings['sampler']['replace'].
                                      format(scene_file_settings['sampler']['name'][sampler]), scene[k - 1])
                    order[k] = order[k - 1]

                    for resolution in scene_targets['resolution']:
                        k = 4

                        # deal with different resolution format
                        scene[k] = scene[k - 1]
                        if len(scene_file_settings['resolution']) == 2:
                            for i in range(2):
                                scene[k] = re.sub(scene_file_settings['resolution'][i]['regex'],
                                                  scene_file_settings['resolution'][i]['replace'].
                                                  format(resolution[i]), scene[k])
                        elif len(scene_file_settings['resolution']) == 1:
                            scene[k] = re.sub(scene_file_settings['resolution'][0]['regex'],
                                              scene_file_settings['resolution'][0]['replace'].
                                              format(f'{resolution[0]}, {resolution[1]}'), scene[k])
                        else:
                            raise Exception('wrong resolution channels')
                        order[k] = order[k - 1]

                        for spp in target_settings['spp']:
                            k = 5

                            scene[k] = re.sub(scene_file_settings['spp']['regex'],
                                              scene_file_settings['spp']['replace'].
                                              format(spp), scene[k - 1])
                            order[k] = order[k - 1]

                            for max_depth in target_settings['max_depth']:
                                k = 6

                                scene[k] = re.sub(scene_file_settings['max_depth']['regex'],
                                                  scene_file_settings['max_depth']['replace'].
                                                  format(max_depth), scene[k - 1])
                                order[k] = order[k - 1]

                                for spectrum in target_settings['spectrum']:
                                    k = 7

                                    # deal with different spectrum format: scene/cmd
                                    scene[k] = scene[k - 1]
                                    order[k] = order[k - 1]
                                    if scene_file_settings['spectrum'] != 'undefined':
                                        scene[k] = re.sub(scene_file_settings['spectrum']['regex'],
                                                          scene_file_settings['spectrum']['replace'].
                                                          format(scene_file_settings['spectrum']['name'][spectrum]),
                                                          scene[k])
                                    else:
                                        spectrum_name = settings['exe']['spectrum']['name'][spectrum]
                                        if spectrum_name == 'undefined':
                                            continue
                                        order[k] += ' ' + settings['exe']['spectrum']['order'].format(
                                            spectrum_name)

                                    # output file
                                    output_file_name = f'{renderer}-{scene_name}-{integrator}-{sampler}-' \
                                                       f'{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                       f'{max_depth}max_depth-{spectrum}'

                                    output_file_name = os.path.dirname(__file__) + '/outputs/' + output_file_name
                                    scene[k] = re.sub(scene_file_settings['output_file']['regex'],
                                                      scene_file_settings['output_file']['replace'].format(
                                                          output_file_name), scene[k])
                                    order[k] += ' ' + settings['exe']['output'].format(output_file_name + '.exr')

                                    # device
                                    if settings['exe']['device'] != 'undefined':
                                        order[k] += ' ' + settings['exe']['device'].format(0)

                                    # new scene file
                                    scene_file_path_new = f'scene-{integrator}-{sampler}-' \
                                                          f'{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                          f'{max_depth}max_depth-{spectrum}'
                                    scene_file_path_new = os.path.join(os.path.dirname(scene_file_path),
                                                                       scene_file_path_new) + \
                                                          os.path.splitext(scene_file_settings['scene_file_name'])[-1]
                                    with open(scene_file_path_new, 'w') as f:
                                        f.write(scene[k])

                                    # real scene
                                    order[k] += ' ' + scene_file_path_new
                                    print(order[k])

                                    # render
                                    with os.popen(order[k]) as f:
                                        output_info = f.read()
                                    try:
                                        time = re.search(settings['results_regex']['time'], output_info).group(1)
                                    except:
                                        time = 'Error'
                                        error_text = f'Error {error_index}: \n{output_info}\n\n'
                                        print(error_text)
                                        with open(errors_save_file_path, 'a') as f:
                                            f.write(error_text)
                                            error_index += 1

                                    result = [
                                        renderer, scene_name, integrator,
                                        sampler, f'({resolution[0]}, {resolution[1]})',
                                        spp, max_depth, spectrum, time]

                                    results.append(result)
                                    print(result)
                                    with open(results_save_file_path, 'a', newline='') as f:
                                        f_csv = csv.writer(f)
                                        f_csv.writerow(result)

    print('==================== results ====================')
    print(results)
    with open(results_save_file_path, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(results)
    print('==================== results ====================')


if __name__ == '__main__':
    test_targets()
