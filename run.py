renderer_settings = {
    'LuisaRender': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/LuisaRender/cmake-build-release/bin/luisa-render-cli.exe',
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
        'exe_path': 'C:/OldNew/Graphics-Lab/LuisaCompute/mitsuba2/build/dist/mitsuba.exe',
        'scene_file': {
            'scene_file_name': 'scene.xml',
            'resolution_regular': [
                '<integer name="width" value="*"/>',
                '<integer name="height" value="*"/>',
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
        },
    },
    'PBRT-v4': {
        'exe_path': 'C:/OldNew/Graphics-Lab/LuisaCompute/pbrt-v4/build-vs/Release/pbrt.exe',
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
        },
    },
}

target_settings = {
    'renderer': [
        'LuisaRender',
        'Mitsuba2',
        'PBRT-v4',
    ],
    'scene': [
        'classroom',
        'coffee',
        'dinning-room',
        'glass-of-water',
        'living-room',
        'spaceship',
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
    pass