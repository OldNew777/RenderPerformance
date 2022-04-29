import os
import re

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
            'output': 'undefined',
            'appendix': '-b dx',
        },
        'scene_file': {
            'scene_file_name': 'scene.luisa',
            'output_file': {
                'regex': 'depth { [0-9]* }',
                'replace': 'depth {{ {} }}',
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
            'time': '\(([0-9a-zA-Z]*) | 100.0%\)',
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
                'regex': '<integer name="maxDepth" value="[0-9]*" />',
                'replace': '<integer name="maxDepth" value="{}" />',
            },
            'spp': {
                'regex': '<integer name="sampleCount" value="[0-9]*" />',
                'replace': '<integer name="sampleCount" value="{}" />',
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
            'time': 'Rendering finished. \(took ([0-9a-zA-Z]*)\)',
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
            'output': '{}',
            'appendix': '',
        },
        'scene_file': {
            'scene_file_name': 'scene-v4.pbrt',
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
            'time': 'Rendering finished. \(took ([0-9a-zA-Z]*)\)',
        },
    },
}

target_settings = {
    'renderer': [
        'LuisaRender',
        'Mitsuba2',
        'PBRT-v4',
    ],
    'scene': {
        'classroom': {
            'resolution': [
                (1920, 1080),
            ],
        },
        'coffee': {
            'resolution': [
                (800, 1000),
            ],
        },
        'dining-room': {
            'resolution': [
                (1920, 1080),
            ],
        },
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
        4096,
    ],
    'max_depth': [
        12,
        16,
    ],
}


def test_targets():
    results = []

    for renderer in target_settings['renderer']:
        render_directory = os.path.join(os.path.realpath(os.path.dirname(__file__)), renderer)
        settings = renderer_settings[renderer]
        exe_path = settings['exe']['path']
        order_exe = exe_path + ' ' + settings['exe']['appendix']

        for scene_name, scene_targets in target_settings['scene'].items():
            scene_directory = os.path.join(render_directory, scene_name)
            scene_file_settings = settings['scene_file']
            scene_file_path = os.path.join(scene_directory, scene_file_settings['scene_file_name'])
            with open(scene_file_path, 'r') as scene_file:
                scene = scene_file.read()
            order_scene = order_exe + ' ' + scene_file_path

            for integrator in target_settings['integrator']:
                integrator_name = scene_file_settings['integrator']['name'][integrator]
                if integrator_name == 'undefined':
                    continue
                scene = re.sub(scene_file_settings['integrator']['regex'],
                               scene_file_settings['integrator']['replace'].
                               format(integrator_name), scene)
                order_integrator = order_scene + ' ' + settings['exe']['integrator']['order'].format(
                    settings['exe']['integrator']['name'][integrator])

                for sampler in target_settings['sampler']:
                    scene = re.sub(scene_file_settings['sampler']['regex'],
                                   scene_file_settings['sampler']['replace'].
                                   format(scene_file_settings['sampler']['name'][sampler]), scene)

                    for resolution in scene_targets['resolution']:
                        # deal with different resolution format
                        if len(scene_file_settings['resolution']) == 2:
                            for i in range(2):
                                scene = re.sub(scene_file_settings['resolution'][i]['regex'],
                                               scene_file_settings['resolution'][i]['replace'].
                                               format(resolution[i]), scene)
                        elif len(scene_file_settings['resolution']) == 1:
                            scene = re.sub(scene_file_settings['resolution'][0]['regex'],
                                           scene_file_settings['resolution'][0]['replace'].
                                           format('{}, {}'.format(resolution[0], resolution[1])), scene)
                        else:
                            raise Exception('wrong resolution channels')

                        for spp in target_settings['spp']:
                            scene = re.sub(scene_file_settings['spp']['regex'], scene_file_settings['spp']['replace'].
                                           format(spp), scene)

                            for max_depth in target_settings['max_depth']:
                                scene = re.sub(scene_file_settings['max_depth']['regex'],
                                               scene_file_settings['max_depth']['replace'].
                                               format(max_depth), scene)

                                for spectrum in target_settings['spectrum']:
                                    # deal with different spectrum format: scene/cmd
                                    order_spectrum = order_integrator
                                    if scene_file_settings['spectrum'] != 'undefined':
                                        scene = re.sub(scene_file_settings['spectrum']['regex'],
                                                       scene_file_settings['spectrum']['replace'].
                                                       format(scene_file_settings['spectrum']['name'][spectrum]), scene)
                                    else:
                                        spectrum_name = settings['exe']['spectrum']['name'][spectrum]
                                        if spectrum_name == 'undefined':
                                            continue
                                        order_spectrum += ' ' + settings['exe']['spectrum']['order'].format(
                                            spectrum_name)

                                    order_device = order_spectrum
                                    if settings['exe']['device'] != 'undefined':
                                        order_device += ' ' + settings['exe']['device'].format(0)

                                    order_final = order_device

                                    scene_file_path_new = 'scene_{}_{}_{}*{}_{}spp_{}max_depth_{}'.format(
                                        integrator, sampler, resolution[0], resolution[1], spp, max_depth, spectrum
                                    )
                                    scene_file_path_new = os.path.join(os.path.dirname(scene_file_path),
                                                                       scene_file_path_new)
                                    with open(scene_file_path_new, 'w') as f:
                                        f.write(order_final)

                                    with os.popen(order_final) as f:
                                        output_info = f.readlines()
                                    time = re.search(settings['results_regex']['time'], output_info)

                                    result = \
                                        '{} {} {} sampler={} resolution=({}, {}) spp={} max_depth={} {} time={}'.format(
                                            renderer, scene_name, integrator,
                                            sampler, resolution[0], resolution[1],
                                            spp, max_depth, spectrum, time)

                                    results.append(result)

    with open(os.path.join(os.path.dirname(__file__), 'results.txt'), 'w') as f:
        f.writelines(results)


if __name__ == '__main__':
    test_targets()
