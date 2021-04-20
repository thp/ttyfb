from ttyfb import *
from ttyfb import Demo

def render_example(dithering):
    Demo.dithering = dithering

    for y in range(h):
        ya = (y+1) / h
        for x in range(w):
            putpixel((x, y), lerp_rgb((0, 0, 0), (0, 0, 255), ya))

    text_big('Dithering' if dithering else 'Palette', (0, 3), (255, 255, 255))

    render(to_stdout)

render_example(False)
input()

render_example(True)
input()

