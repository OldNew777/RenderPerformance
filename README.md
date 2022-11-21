# RenderPerformance

`run.py` is a script implemented in Python, designed to test performance of several renders including **LuisaRender**, **Mitsuba2**, **Mitsuba3**, **PBRT-v4**.

## Usage
You may configure the script by editing `run_config.py` file. 

1. `target_settings` contains the renderers you want to test, and the corresponding rendering settings.

    Notably, **PBRT-v4** configures `rr_depth` in its source code, so the `rr_depth` in `target_settings` will not work for **PBRT-v4**.
You may modify the source code and recompile it to change `rr_depth`.

2. `renderer_settings` contains the executable path of each renderer and the regex pattern to parse scene files or commandline orders.

    The former **must be specified manually** before testing, and the later are not supposed to be modified.

Then you may run the script by
```bash
python run.py
```

The script will automatically create a folder named `outputs` to store the results.
Rendering results will be stored in `outputs/pictures`, and the statistics will be stored in `outputs/results.csv`.

Scene files of each configuration will be saved in `<renderer>/scenes` folder for checking.

