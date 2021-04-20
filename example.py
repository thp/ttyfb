from ttyfb import *

from ttyfb import Demo

fill((64, 64, 64))

line((0, 0), (w, h), (255, 0, 0), (0, 255, 0))
line((0, h), (w, 0), (0, 255, 255), (255, 0, 255))
circle((w / 2, h / 2), 10, (255, 255, 255))

text_big('hello', (-1, 0), (0, 0, 0))
text_big('hello', (0, 0), (255, 255, 0))

text_big('world', (w-8*5-2+1, 8), (0, 0, 0))
text_big('world', (w-8*5-2, 8), (0, 255, 255))

text_small('ttyfb 0.1 PREVIEW', (5, 12))

render(to_stdout)

#with open('example-out.txt', 'w') as fp:
#    render(to_file(fp))

input()

for mode in Demo.MODES:
    Demo.mode = mode
    clear()
    text_small(f'Mode: {Demo.MODE_NAMES[mode]}', (0, 0))
    view_image('lena.png')
    render(to_stdout)
    input()

#with open('lena.txt', 'w') as fp:
#    render(to_file(fp))
