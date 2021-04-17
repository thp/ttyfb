from ttyfb import *

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

with open('example-out.txt', 'w') as fp:
    render(to_file(fp))

input()

clear()
view_image('lena.png')
render(to_stdout)

with open('lena.txt', 'w') as fp:
    render(to_file(fp))

input()

