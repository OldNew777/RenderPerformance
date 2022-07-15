import matplotlib.font_manager as font_manager
from matplotlib import rcParams

fonts = font_manager.findSystemFonts()
print(f"{len(fonts)} fonts found: {[f for f in fonts if 'Lin' in f]}")

if not any(f.name == "Linux Biolinum" for f in font_manager.fontManager.ttflist):
    try:
        font_manager.fontManager.addfont("Linux-Biolinum.ttf")
    except:
        font_manager.fontManager.addfont("../Linux-Biolinum.ttf")
font_family = "Linux Biolinum"
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = font_family
rcParams["font.size"] = 15
rcParams["mathtext.fontset"] = "custom"
rcParams["mathtext.rm"] = font_family
rcParams["mathtext.it"] = font_family
rcParams["mathtext.bf"] = font_family
rcParams["mathtext.sf"] = font_family
rcParams["hatch.linewidth"] = 7.5
