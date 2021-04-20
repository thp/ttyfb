from ttyfb import *
from ttyfb import Demo

for dstcolor in ((0, 0, 255), (255, 255, 255)):
    for mode in Demo.MODES:
        Demo.mode = mode

        clear()
        for y in range(h):
            ya = (y+1) / h
            for x in range(w):
                putpixel((x, y), lerp_rgb((0, 0, 0), dstcolor, ya))

        text_small(f'Mode: {Demo.MODE_NAMES[mode]} color: {dstcolor}', (0, 0))
        render(to_stdout)
        input()
