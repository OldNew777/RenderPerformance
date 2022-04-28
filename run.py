import os
import re

renderer_settings = {
    'LuisaRender': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/LuisaRender/cmake-build-release/bin/luisa-render-cli.exe',
            'spectrum': 'undefined',
            'appendix': '-b dx -d 0',
        },
        'scene_file': {
            'scene_file_name': 'scene.luisa',
            'resolution': [
                {
                    'regular': 'resolution { [, 0-9]* }',
                    'replace': 'resolution {{ {} }}'
                },
            ],
            'max_depth': {
                'regular': 'depth { [0-9]* }',
                'replace': 'depth {{ {} }}',
            },
            'spp': {
                'regular': 'spp { [0-9]* }',
                'replace': 'spp {{ {} }}',
            },
            'sampler': {
                'name': {
                    'Independent': 'Independent',
                },
                'regular': 'sampler : [a-zA-Z]* \{\}',
                'replace': 'sampler : {} {{}}',
            },
            'spectrum': {
                'name': {
                    'RGB': 'sRGB',
                    'Spectral': 'Hero',
                },
                'regular': 'spectrum : [a-zA-Z]* \{\}',
                'replace': 'spectrum : {} {{}}',
            },
            'integrator': {
                'name': {
                    'WavePath': 'WavePath',
                    'MegaPath': 'MegaPath',
                },
                'regular': 'integrator : [a-zA-Z]* {',
                'replace': 'integrator : {} {{',
            },
        },
    },
    'Mitsuba2': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/Mitsuba2/build/dist/mitsuba.exe',
            'spectrum': {
                'name': {
                    'RGB': 'sRGB',
                    'Spectral': 'Hero',
                },
            },
        },
        'scene_file': {
            'scene_file_name': 'scene.xml',
            'resolution': [
                {
                    'regular': '<integer name="width" value="[0-9]*" />',
                    'replace': '<integer name="width" value="{}" />',
                },
                {
                    'regular': '<integer name="height" value="[0-9]*" />',
                    'replace': '<integer name="height" value="{}" />',
                },
            ],
            'max_depth': {
                'regular': '<integer name="maxDepth" value="[0-9]*" />',
                'replace': '<integer name="maxDepth" value="{}" />',
            },
            'spp': {
                'regular': '<integer name="sampleCount" value="[0-9]*" />',
                'replace': '<integer name="sampleCount" value="{}" />',
            },
            'sampler': {
                'name': {
                    'Independent': 'independent',
                },
                'regular': '<sampler type="[a-zA-Z]*" >',
                'replace': '<sampler type="{}" >',
            },
            'spectrum': 'undefined',
            'integrator': {
                'name': {
                    'WavePath': 'path',
                    'MegaPath': 'undefined',
                },
                'regular': '<integrator type="[a-zA-Z]*" >',
                'replace': '<integrator type="{}" >',
            },
        },
    },
    'PBRT-v4': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/pbrt-v4/build-vs/Release/pbrt.exe',
        },
        'scene_file': {
            'scene_file_name': 'scene-v4.pbrt',
            'resolution': [
                {
                    'regular': '"integer xresolution" \[ [0-9]* \]',
                    'replace': '"integer xresolution" [ {} ]',
                },
                {
                    'regular': '"integer yresolution" \[ [0-9]* \]',
                    'replace': '"integer yresolution" [ {} ]',
                },
            ],
            'max_depth': {
                'regular': '"integer maxdepth" \[ [0-9]* \]',
                'replace': '"integer maxdepth" [ {} ]',
            },
            'spp': {
                'regular': '"integer pixelsamples" \[ [0-9]* \]',
                'replace': '"integer pixelsamples" [ {} ]',
            },
            'sampler': {
                'name': {
                    'Independent': 'independent',
                },
                'regular': 'Sampler "[a-zA-Z]*"',
                'replace': 'Sampler "{}"',
            },
            'spectrum': 'undefined',
            'integrator': {
                'name': {
                    'WavePath': 'path',
                    'MegaPath': 'undefined',
                },
                'regular': 'Integrator "[a-zA-Z]*"',
                'replace': 'Integrator "{}"',
            },
        },
    },
}

target_settings = {
    'renderer': [
        # 'LuisaRender',
        'Mitsuba2',
        'PBRT-v4',
    ],
    'scene': [
        'classroom',
        'coffee',
        'dining-room',
        'glass-of-water',
        'living-room',
        'spaceship',
    ],
    'integrator': [
        'WavePath',
        'MegaPath',
    ],
    'spp': [
        4096,
    ],
    'sampler': [
        'Independent',
    ],
    'resolution': [
        (1920, 1080),
    ],
    'spectrum': [
        'RGB',
        'Spectral',
    ],
    'max_depth': [
        12,
        16,
    ],
}

if __name__ == '__main__':
    for renderer in target_settings['renderer']:
        render_directory = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(__file__))), renderer)
        settings = renderer_settings[renderer]
        exe_path = settings['exe']['path']
        working_directory = os.path.dirname(exe_path)
        for scene_name in target_settings['scene']:
            scene_directory = os.path.join(render_directory, scene_name)
            scene_file_settings = settings['scene_file']
            scene_file_path = os.path.join(scene_directory, scene_file_settings['scene_file_name'])
            with open(scene_file_path, 'r') as scene_file:
                scene = scene_file.read()
            for integrator in target_settings['integrator']:
                integrator_name = scene_file_settings['integrator']['name'][integrator]
                if integrator_name == 'undefined':
                    continue
                scene = re.sub(scene_file_settings['integrator']['regular'],
                               scene_file_settings['integrator']['replace'].
                               format(integrator_name), scene)
                for spp in target_settings['spp']:
                    scene = re.sub(scene_file_settings['spp']['regular'], scene_file_settings['spp']['replace'].
                                   format(spp), scene)
                    for sampler in target_settings['sampler']:
                        scene = re.sub(scene_file_settings['sampler']['regular'],
                                       scene_file_settings['sampler']['replace'].
                                       format(scene_file_settings['sampler']['name'][sampler]), scene)
                        for resolution in target_settings['resolution']:
                            # deal with different resolution format
                            if len(scene_file_settings['resolution']) == 2:
                                for i in range(2):
                                    scene = re.sub(scene_file_settings['resolution'][i]['regular'],
                                                   scene_file_settings['resolution'][i]['replace'].
                                                   format(resolution[i]), scene)
                            elif len(scene_file_settings['resolution']) == 1:
                                scene = re.sub(scene_file_settings['resolution'][0]['regular'],
                                               scene_file_settings['resolution'][0]['replace'].
                                               format('{}, {}'.format(resolution[0], resolution[1])), scene)
                            else:
                                raise Exception('wrong resolution channels')
                            for max_depth in target_settings['max_depth']:
                                scene = re.sub(scene_file_settings['max_depth']['regular'],
                                               scene_file_settings['max_depth']['replace'].
                                               format(max_depth), scene)
                                # TODO: deal with different spectrum format: scene/cmd
                                for spectrum in target_settings['spectrum']:
                                    if scene_file_settings['spectrum'] != 'undefined':
                                        scene = re.sub(scene_file_settings['spectrum']['regular'],
                                                       scene_file_settings['spectrum']['replace'].
                                                       format(scene_file_settings['spectrum']['name'][spectrum]), scene)
                                    print(scene)
                                    exit(0)
