import os
import re

from mylogger import *
from result_recorder import Recorder
from wash_breakdown import *

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
                'order': ' {}',
            },
            'backend': {
                'name': {
                    'cuda': 'cuda',
                    'directX': 'dx',
                    'metal': 'metal',
                    'cpu': 'ispc',
                },
                'order': ' -b {}',
            },
            'device': ' -d {}',
            'output': '',
            'appendix': '',
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
                'regex': ' depth { [0-9]* }',
                'replace': ' depth {{ {} }}',
            },
            'rr_depth': {
                'regex': 'rr_depth { [0-9]* }',
                'replace': 'rr_depth {{ {} }}',
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
                    'RGB': 'rgb',
                    'Spectral': 'spectral',
                },
                'order': '{}',
            },
            'integrator': {
                'name': {
                    'WavePath': '',
                    'MegaPath': '',
                },
                'order': ' {}',
            },
            'backend': {
                'name': {
                    'cuda': 'gpu',
                    'directX': 'undefined',
                    'metal': 'undefined',
                    'cpu': 'scalar',
                },
                'order': ' -m {}_',
            },
            'device': 'undefined',
            'output': ' --output {}',
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
            'rr_depth': {
                'regex': '<integer name="rr_depth" value="[0-9]*" />',
                'replace': '<integer name="rr_depth" value="{}" />',
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
            # 'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/pbrt-v4/build-vs/Release_2rr_depth/pbrt.exe',
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/pbrt-v4/build-vs/Release_5rr_depth/pbrt.exe',
            'spectrum': {
                'name': {
                    'RGB': 'undefined',
                    'Spectral': '',
                },
                'order': ' {}',
            },
            'integrator': {
                'name': {
                    'WavePath': '--wavefront',
                    'MegaPath': ' ',
                },
                'order': ' {}',
            },
            'backend': {
                'name': {
                    'cuda': '--gpu',
                    'directX': 'undefined',
                    'metal': 'undefined',
                    'cpu': '',
                },
                'order': ' {}',
            },
            'device': ' --gpu-device {}',
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
            'rr_depth': 'undefined',
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
                    'MegaPath': 'path',
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
        'LuisaRender',
        # 'Mitsuba2',
        # 'PBRT-v4',
    ],
    'backend': [
        # 'cuda',
        # 'directX',
        'cpu',
        # 'metal',
    ],
    'scene': {
        # # wrong cases with mitsuba2
        # 'classroom': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        # 'dining-room': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        #
        # # right cases
        # 'living-room': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },

        'coffee': {
            'resolution': [
                (1200, 1800),
            ],
        },
        # 'glass-of-water': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        # 'spaceship': {
        #     'resolution': [
        #         (1920, 1080),
        #     ],
        # },
        # 'staircase': {
        #     'resolution': [
        #         (1080, 1920),
        #     ],
        # },
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
        1,
        # 16,
        # 64,
        # 128,
        # 256,
        # 1024,
        # 4096,
    ],
    'max_depth': [
        # 8,
        16,
    ],
    'rr_depth': [
        # 2,
        5,
    ],
}

LuisaRender_breakdown = True


def test_targets():
    results = []
    results_save_file_path = os.path.join(os.path.dirname(__file__), 'outputs', 'results.csv')
    scene = ['' for i in range(100)]
    order = ['' for i in range(100)]
    error_index = 0

    output_dir = os.path.dirname(__file__).replace('\\', '/') + '/outputs'
    output_picture_dir = output_dir + '/pictures'
    if not os.path.exists(output_picture_dir):
        os.makedirs(output_picture_dir)

    recorder = Recorder(results_save_file_path)
    with open('results.txt', 'w') as _:
        pass
    headers = ['render', 'scene', 'backend', 'integrator', 'sampler', 'resolution',
               'spp', 'max depth', 'rr depth', 'spectrum', 'time consumption']
    while not recorder.init(headers):
        pass

    # clear_log_file()
    logger.info('')
    logger.info('===================== start =====================')

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
                order[k] = order[k - 1] + settings['exe']['integrator']['order'].format(
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

                                if scene_file_settings['rr_depth'] == 'undefined':
                                    rr_depth_unknown = True
                                else:
                                    rr_depth_unknown = False

                                for rr_depth in target_settings['rr_depth']:
                                    k = 7

                                    scene[k] = scene[k - 1]
                                    order[k] = order[k - 1]

                                    if rr_depth_unknown:
                                        rr_depth = 'unknown'
                                    else:
                                        scene[k] = re.sub(scene_file_settings['rr_depth']['regex'],
                                                          scene_file_settings['rr_depth']['replace'].
                                                          format(rr_depth), scene[k])

                                    for backend in target_settings['backend']:
                                        k = 8

                                        scene[k] = scene[k - 1]
                                        order[k] = order[k - 1]

                                        backend_name = settings['exe']['backend']['name'][backend]
                                        if backend_name == 'undefined':
                                            continue
                                        order[k] += settings['exe']['backend']['order'].format(backend_name)

                                        for spectrum in target_settings['spectrum']:
                                            k = 9

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
                                                order[k] += settings['exe']['spectrum']['order'].format(spectrum_name)

                                            # output file
                                            output_file_name = f'{renderer}-{scene_name}-{backend}-{integrator}-' \
                                                               f'{sampler}-{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                               f'{max_depth}max_depth-{rr_depth}rr_depth-{spectrum}'

                                            output_file_name = output_picture_dir + '/' + output_file_name
                                            scene[k] = re.sub(scene_file_settings['output_file']['regex'],
                                                              scene_file_settings['output_file']['replace'].format(
                                                                  output_file_name), scene[k])
                                            order[k] += settings['exe']['output'].format(output_file_name + '.exr')

                                            # new scene file confirmed
                                            scene_file_path_new = f'scene-{integrator}-{sampler}-' \
                                                                  f'{resolution[0]}_{resolution[1]}-{spp}spp-' \
                                                                  f'{max_depth}max_depth-{rr_depth}rr_depth-{spectrum}'
                                            scene_file_path_new = os.path.join(os.path.dirname(scene_file_path),
                                                                               scene_file_path_new) + \
                                                                  os.path.splitext(scene_file_settings['scene_file_name'])[
                                                                      -1]
                                            with open(scene_file_path_new, 'w') as f:
                                                f.write(scene[k])

                                            # device
                                            if settings['exe']['device'] != 'undefined':
                                                order[k] += settings['exe']['device'].format(0)

                                            # target scene file
                                            order[k] += ' ' + scene_file_path_new

                                            # order confirmed
                                            logger.info(order[k])

                                            render_times = 1
                                            # LuisaRender breakdown
                                            if renderer == 'LuisaRender' and LuisaRender_breakdown:
                                                render_times = 2

                                                cache_dir = os.path.join(os.path.dirname(settings['exe']['path']), '.cache')
                                                cache_files = os.listdir(cache_dir)
                                                for file in  cache_files:
                                                    os.remove(os.path.join(cache_dir, file))

                                            for _ in range(render_times):

                                                # render
                                                with os.popen(order[k]) as f:
                                                    output_info = f.read()
                                                try:
                                                    time = re.search(settings['results_regex']['time'], output_info).group(1)
                                                except:
                                                    time = 'Error'
                                                    error_text = f'Error {error_index}: \n{output_info}\n'
                                                    error_index += 1
                                                    logger.warning(error_text)

                                                result = [
                                                    renderer, scene_name, backend, integrator,
                                                    sampler, f'({resolution[0]}, {resolution[1]})',
                                                    spp, max_depth, rr_depth, spectrum, time]

                                                results.append(result)
                                                logger.info(result)
                                                recorder.write_row(result)

                                    if rr_depth_unknown:
                                        break

    while not recorder.flush():
        pass

    logger.info('#################### results ####################')
    logger.info(results)
    logger.info('#################### results ####################')

    gather_breakdown()

    logger.info('====================== end ======================')
    logger.info('')


if __name__ == '__main__':
    test_targets()
