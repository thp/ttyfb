from ttyfb import *

import datetime
import time
import math

scale = (1, 2)

target_rotation = 0
rotation = 2 * math.pi

alpha = 0.7

with no_cursor():
    while True:
        try:
            cur = datetime.datetime.now().strftime('%H:%M:%S')

            rotation = alpha * rotation + (1 - alpha) * target_rotation
            if rotation < 0.01 and target_rotation == 0:
                rotation = 0
            elif target_rotation != 0 and rotation > target_rotation * 0.8:
                break

            bright = (1 - rotation / (2 * math.pi))
            scale = (1*bright, 2*bright)

            x = (w - 8 * len(cur) * scale[0]) / 2
            y = ((h - 8 * scale[1]) / 2)

            clear()
            for dx, c in ((1, int(64 * bright)), (0, int(255 * bright))):
                text_big(cur, (x+dx, y), (c,)*3, scale, rotation if target_rotation else 0)
            render(to_stdout)

            time.sleep(.01 if rotation is not None else 1)
        except KeyboardInterrupt:
            if target_rotation == 0:
                target_rotation = 2 * math.pi
                alpha = 0.95
            else:
                break
