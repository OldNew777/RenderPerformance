LuisaRender_breakdown = False

target_settings = {
    'renderer': [
        'LuisaRender',
        # 'PBRT-v4',
        # 'Mitsuba2',
        'Mitsuba3',
    ],
    'backend': [
        # 'cpu',
        'cuda',
        'directX',
        # 'metal',
    ],
    'scene': {
        # wrong scene files with mitsuba2
        'classroom': {
            'resolution': [
                (1920, 1080),
            ],
        },
        'dining-room': {
            'resolution': [
                (1920, 1080),
            ],
        },


        # right scene files
        'living-room': {
            'resolution': [
                (1920, 1080),
                # (1280, 720),
            ],
        },
        'coffee': {
            'resolution': [
                (1200, 1800),
            ],
        },
        'glass-of-water': {
            'resolution': [
                (1920, 1080),
                # (1280, 720),
            ],
        },
        'spaceship': {
            'resolution': [
                (1920, 1080),
                # (1280, 720),
            ],
        },
        'staircase': {
            'resolution': [
                (1080, 1920),
                # (720, 1280),
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
        # 1,
        # 16,
        # 64,
        # 128,
        # 256,
        1024,
        # 4096,
        # 8192,
        # 16384,
    ],
    'max_depth': [
        # 3,
        # 8,
        16,
        # 32,
    ],
    'rr_depth': [
        # 2,
        5,
    ],
}

renderer_settings = {
    'LuisaRender': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/LuisaRender/cmake-build-release/bin/luisa-render-cli.exe',
            'spectrum': None,
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
                    'regex': 'resolution { [, \.0-9]* }',
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
                    'directX': None,
                    'metal': None,
                    'cpu': 'scalar',
                },
                'order': ' -m {}_',
            },
            'device': None,
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
            'spectrum': None,
            'integrator': {
                'name': {
                    'WavePath': 'path',
                    'MegaPath': None,
                },
                'regex': '<integrator type="[a-zA-Z]*" >',
                'replace': '<integrator type="{}" >',
            },
        },
        'results_regex': {
            'time': 'Rendering finished\. \(took ([0-9a-zA-Z\.]*)\)',
        },
    },
    'Mitsuba3': {
        'exe': {
            'path': 'C:/OldNew/Graphics-Lab/LuisaCompute/mitsuba3/cmake-build-release/Release/mitsuba.exe',
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
                    'cuda': 'cuda',
                    'directX': None,
                    'metal': None,
                    'cpu': 'scalar',
                },
                'order': ' -m {}_',
            },
            'device': None,
            'output': ' --output {}',
            'appendix': '',
        },
        'scene_file': {
            'scene_file_name': 'scene_v3.xml',
            'output_file': {
                'regex': '<string name="filename" value="output\.exr" />',
                'replace': '<string name="filename" value="{}.exr" />',
            },
            'resolution': [
                {
                    'regex': '<default name="resx" value="[0-9]*" />',
                    'replace': '<default name="resx" value="{}" />',
                },
                {
                    'regex': '<default name="resy" value="[0-9]*" />',
                    'replace': '<default name="resy" value="{}" />',
                },
            ],
            'max_depth': {
                'regex': '<default name="max_depth" value="[0-9]*" />',
                'replace': '<default name="max_depth" value="{}" />',
            },
            'rr_depth': {
                'regex': '<default name="rr_depth" value="[0-9]*" />',
                'replace': '<default name="rr_depth" value="{}" />',
            },
            'spp': {
                'regex': '<default name="spp" value="[0-9]*" />',
                'replace': '<default name="spp" value="{}" />',
            },
            'sampler': {
                'name': {
                    'Independent': 'independent',
                },
                'regex': '<sampler type="[a-zA-Z]*" >',
                'replace': '<sampler type="{}" >',
            },
            'spectrum': None,
            'integrator': {
                'name': {
                    'WavePath': None,
                    'MegaPath': 'path',
                },
                'regex': '<default name="integrator" value="[a-zA-Z]*" />',
                'replace': '<default name="integrator" value="{}" />',
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
                    'RGB': None,
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
                    'directX': None,
                    'metal': None,
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
            'rr_depth': None,
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
            'spectrum': None,
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