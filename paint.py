import contextlib
import sys
import tty
import termios
import select
import os

from ttyfb import *

class UIMode():
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.pdf
    MOUSEDOWN = 32
    MOUSEUP = 35
    MOUSEMOVE = 64

    def kbhit(self):
        p = select.poll()
        p.register(0, select.POLLIN | select.POLLPRI)
        return len(p.poll(0)) > 0

    def events(self):
        while True:
            if not self.kbhit():
                break

            ch = sys.stdin.buffer.read(1)
            if ord(ch) == 27:
                n = sys.stdin.buffer.read(1)
                if n == b'[':
                    ch = sys.stdin.buffer.read(1)
                    if ch == b'M':
                        cb, cx, cy = sys.stdin.buffer.read(3)
                        cx -= 33
                        cy -= 33
                        if cb == self.MOUSEDOWN:
                            yield ('mousedown', cx, cy)
                        elif cb == self.MOUSEUP:
                            yield ('mouseup', cx, cy)
                        elif cb == self.MOUSEMOVE:
                            yield ('mousemove', cx, cy)
                        else:
                            yield ('mouse', cb, cx, cy)
            else:
                yield ('key', ch)



@contextlib.contextmanager
def ui_mode():
    try:
        tty.setraw(0, termios.TCSANOW)
        to_stdout('\033[2J', '\033[?25l')
        to_stdout('\033[?1002h')
        sys.stdout.flush()
        yield UIMode()
    finally:
        to_stdout('\033[?1002l')
        to_stdout('\033[2J\033[H\033[0m', '\033[?25h')
        sys.stdout.flush()
        tty.setcbreak(0)
        os.system('reset')


def toggle_pixel(x, y):
    putpixel((x*2, y*2), paint_color)
    putpixel((x*2, y*2+1), paint_color)
    putpixel((x*2+1, y*2), paint_color)
    putpixel((x*2+1, y*2+1), paint_color)


with ui_mode() as mode:
    paint_color = (255, 255, 255)

    lmx = 0
    lmy = 0

    text_small('Draw with the left mouse button, color with 1-5, exit with "q".', (0, 0))
    text_small('Paint color:', (0, 2))

    while True:
        rectangle(13, 3, 4, 4, (255, 255, 255))
        rectangle(14, 4, 2, 2, paint_color)

        for event, *args in mode.events():
            if event == 'key':
                key, = args
                if key == b'q':
                    raise SystemExit()
                elif key == b'1':
                    paint_color = (255, 255, 255)
                elif key == b'2':
                    paint_color = (0, 0, 0)
                elif key == b'3':
                    paint_color = (255, 0, 0)
                elif key == b'4':
                    paint_color = (0, 255, 0)
                elif key == b'5':
                    paint_color = (0, 0, 255)
            elif event == 'mousedown':
                cx, cy = args
                cx = int(cx/2)

                toggle_pixel(cx, cy)
                lmx = cx
                lmy = cy
            elif event == 'mouseup':
                ...
            elif event == 'mousemove':
                cx, cy = args
                cx = int(cx/2)

                line((lmx*2, lmy*2), (cx*2, cy*2), paint_color)

                lmx = cx
                lmy = cy

        render(to_stdout)
