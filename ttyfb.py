import sys, math, time, zlib, colorsys, random, os

#
# ttyfb 0.1 PREVIEW for Python
# 2021-04-17 Thomas Perl <m@thp.io>
# Based on code from the PyUGAT XMas Puzzle (2019-12-18)
#
# Copyright 2021 Thomas Perl
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__all__ = (
    'w', 'h',
    'resize', 'clear', 'fill',
    'getpixel', 'putpixel',
    'render', 'to_stdout', 'to_file',
    'line', 'circle',
    'Vertex', 'triangle',
    'text_big', 'text_small',
    'view_image',
)

fontdat = bytearray(zlib.decompress(b'x\x9c=R\xc1\x8a\x13A\x10-6d\xe8C\xbbY5\x87\x16\x9a'
b' \x83\x07\t\x1e\x06\x0fc\\\xda\x8e' # Vincent font by Quinn Evans, public domain 2010
b'\x11\x0f\x11\xf6\xba \xe2\xa1!\xa4=\xcc\x10\x07\x84M\xc0\xa1\xfb\xdb\xf2!9\xed\x87'
b'\xc4W5q;\x93\xd4\xbc\xaa\xeaW\xf5\xaaBt9~u\xbf\xba\xff\xe6\xc9\xe7&7{O\xe5>go\x15)\xeb'
b'/v\x9e\xe7\xca\x0e\x18\x96\xac\xf7\xde\xd2\xf9\xfcx<\x1e\x1f\xcf\xc0eY\n>\x9dN\xc0\x93'
b'\xd1\xf8\xe3z]\x91B2\x07\xcc\xf4\xe6\xa6\xea\x02M^=\x7f\xf9\xe1!\x90\x9a\xdb\xbd\x9d+\n'
b'\x87\x94\xd3!\xd0h\xb2\xcc\xcb\xc9\x88\xeb \xa4(\xe2\xe0\x87\x96\xdb\xed\xa7\xf1xL\xfa'
b'\xfd\xfa\xcd\x8b\xbbJz\xcd9_\xf2\xbc\xf4c\xad%|\x87>5\xf84\xac\x01\x9fQ\xc8\xee\xba\x0e'
b'\xf94-s9%\xe4\xa3q`\xa8\xf3\xd6\xaa\xff\xf2\xc98g\x0c\x19\xaa\xeb\xa9\xe0\xba\xce\xf8'
b'\xd4\xa4f\xaf\xed\x95C\x9fQ\x9b*\x16\xe4\xa2{\xbb\x8dK2\xc6H3\x85\xc6\x9b.(T\xec\t\xb8'
b'h\xb3\xad\x11PP>\xd0W\x15\xfb\x89\xdcS\xb1\x10\xe4"\xbb]\xdc=\xc4\xe8\xc0\xb7\x00A\x02'
b'.t\x15\xc4\xda\x02~m\xdf\xdd%\xad)\x85\xbe`\xecb\xe89?E\xcd\x95\x81#?l=\xc7\x89U\x18'
b'\xba\xd8J\xcap\x7f\\\x9e\x1b@\x9fR\x98\xf9Y\xef\xe2\xeb\xcf\xef_\x1c\xf7\x11\x13\x8f'
b'\x1c\xe4\xfcp\x9d\x10\xc0\xd7\xf3"\x80S\x08}@_\x83\r\x12\xdf!\x1e/\xf70=\x1cG3\xadu'
b'\xdb.(\xb6\x87\xee\xd0FH\xe5\x93h\xb3\xcf\xcdf\xb3\xa1\xcd\x9f\xbf\xbf\x7f\xc1:\xe1'
b'\x1d\xf8{\xe1\x8bq\xe7\n\xa9\xcf\xf7\xc0\xefXO\xfa!\xc4\xf2\x7f\x80\xc4\xc1:C\xe0j\xf2'
b'\x1e|\x9b\xda\xd6\xe0\x13/\xf2\x92\xcc5\xd1L\xae\xcd\x06\xc1\x90\x7f\x10| 5-WO{\xa0L'
b'Zf#\xeb)<\xf8\xd1\xac\xe8\xe7\x89\xb0\xfe\xa2\x80\x1b~\xc6)8\xb2uU\xf5\x15V\xcf\xde'
b'\xc2]\xf2#\xe6M\xa2_\xd3\xa0\x1f\xc3kY\x87\x19\x0e\xee\xf3\x04\x1a\xd8^\xe6%\x13\xe7'
b'}\xf5\x83~rm\xeb\x9eMH\x1c\x8c\xc9\x7fvW=\xef1\r\xf7\x07\xfd\xf2\xe2\x84\xafi\x1a\xc6'
b'@.\x8a\x9b\xfb\x01\x11\x06\xe0\xe8\x1a\xcb7\xe6\x9a\xeb\xcb\xb7\xc3\xbf\xd4\x98\x0e'
b'\xf1\xdb\x96I\x14\xa6\xb6Z\xe5\x7f\xdb\x0c\xd0\xc5'))

w, h = os.get_terminal_size()
h *= 2

class Demo:
    clear = bytearray([16]*(w*h))
    buffer = bytearray(clear)
    textbuffer = [' ']*(w*h)

    hires = True
    antialias = False
    motionblur = False


def resize(nw, nh):
    global w, h
    w = nw
    h = nh
    Demo.clear = bytearray([16]*(w*h))
    Demo.buffer = bytearray(Demo.clear)
    Demo.textbuffer = [' ']*(w*h)


def clear():
    Demo.buffer[:] = (darker(c) for c in Demo.buffer) if Demo.motionblur else Demo.clear
    Demo.textbuffer = [' ']*(w*h)

def fill(rgb):
    v = make_555(rgb)
    Demo.buffer[:] = (v for _ in Demo.clear)

def pixelfont(text):
    height = 8
    width = len(text) * 8
    pixels = bytearray(height * width)
    for i, c in enumerate(text.encode('ascii')):
        char = fontdat[c*8:(c+1)*8]
        for y, row in enumerate(char):
            for x in range(8):
                if row & (1 << (8-x)) != 0:
                    pixels[(i * 8 + x) + y * width] = 0xff
    return width, height, pixels

def make_555(rgb):
    r, g, b = (int(max(0, min(5, v / 255 * 5))) for v in rgb)
    return (16 + 36 * r + 6 * g + b)

def putpixel_555(pos, value):
    x, y = pos
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    Demo.buffer[int(y)*w+int(x)] = value

def putpixel(pos, rgb):
    putpixel_555(pos, make_555(rgb))

def parse_555(value):
    assert value >= 16
    value -= 16
    b = value % 6
    value /= 6
    g = value % 6
    value /= 6
    r = value
    return (r*255/5, g*255/5, b*255/5)

def darker(c):
    return make_555((int(x*0.8) for x in parse_555(c)))

def getpixel(pos):
    x, y = pos
    if y < 0 or y >= h or x < 0 or x >= w:
        return (0, 0, 0)
    value = Demo.buffer[int(y)*w+int(x)]
    return parse_555(value)

def lerp(a, b, alpha):
    return a*(1-alpha)+b*alpha

def lerp_rgb(a, b, alpha):
    return tuple(lerp(aa, bb, alpha) for aa, bb in zip(a, b))

def line(a, b, rgb_a, rgb_b=None):
    if rgb_b is None:
        rgb_b = rgb_a

    x0, y0 = a
    x1, y1 = b
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        for x in range(abs(int(dx+1))):
            alpha = x / abs(dx)
            if dx < 0:
                x *= -1
            y = int(x*dy/dx)
            putpixel((x0+x, y0+y), lerp_rgb(rgb_a, rgb_b, alpha))
    else:
        for y in range(abs(int(dy+1))):
            alpha = y / abs(dy or 1)
            if dy < 0:
                y *= -1
            x = int(y*dx/(dy or 1))
            putpixel((x0+x, y0+y), lerp_rgb(rgb_a, rgb_b, alpha))


def circle(center, radius, color):
    # https://iq.opengenus.org/bresenhams-circle-drawing-algorithm/
    def draw(x, y):
        putpixel((center[0]+x, center[1]+y), color)
        putpixel((center[0]-x, center[1]+y), color)
        putpixel((center[0]+x, center[1]-y), color)
        putpixel((center[0]-x, center[1]-y), color)
        putpixel((center[0]+y, center[1]+x), color)
        putpixel((center[0]-y, center[1]+x), color)
        putpixel((center[0]+y, center[1]-x), color)
        putpixel((center[0]-y, center[1]-x), color)

    x = 0
    y = radius
    decision = 3 - 2 * radius
    draw(x, y)
    while y >= x:
        x += 1
        if decision > 0:
            y -= 1
            decision += 4 * (x - y) + 10
        else:
            decision += 4 * x + 6
        draw(x, y)


def triangle(v):
    v = sorted(v, key=lambda p: p.pos.y)

    height = v[2].pos.y - v[0].pos.y

    if height == 0:
        # Degenerate triangle; draw nothing
        return

    h_upper = v[1].pos.y - v[0].pos.y

    x1, x2, xs, c1, c2 = [], [], [], [], []
    for i in range(height):
        alpha = float(i) / float(height)
        x1.append(v[0].pos.x + int(float(v[2].pos.x - v[0].pos.x) * alpha))
        c1.append(v[0].color + (v[2].color - v[0].color) * alpha)
        if i < h_upper:
            alpha = float(i) / float(h_upper)
            x2.append(v[0].pos.x + int(float(v[1].pos.x - v[0].pos.x) * alpha))
            c2.append(v[0].color + (v[1].color - v[0].color) * alpha)
        else:
            alpha = float(i - h_upper) / float(height - h_upper)
            x2.append(v[1].pos.x + int(float(v[2].pos.x - v[1].pos.x) * alpha))
            c2.append(v[1].color + (v[2].color - v[1].color) * alpha)

        xs.append(abs(x2[i]-x1[i]))

    y = v[0].pos.y
    for i in range(height):
        s = 1 if x1[i] < x2[i] else 0
        xd = 1 if x1[i] < x2[i] else -1
        x = x1[i]
        colord = (c2[i] - c1[i]) / xs[i] if xs[i] != 0 else RGB(0, 0, 0)
        color = c1[i]

        for j in range(xs[i]+1):
            putpixel((x, y), (color.r, color.g, color.b))

            x += xd
            color += colord

        y += 1


class to_file(object):
    def __init__(self, fp):
        self.fp = fp

    def __call__(self, *args):
        for arg in args:
            self.fp.write(arg)


def to_stdout(*args):
    for arg in args:
        sys.stdout.write(arg)


def render(out):
    out('\033[H\033[0m')

    current_fore_color = 15
    # Fix for xterm black-on-white
    out(f'\033[38;5;15m')

    current_back_color = 0
    # Force the background color too
    out(f'\033[48;5;0m')

    for y in range(int(h/2)-(1-h%2)):
        for x in range(w):
            if Demo.hires:
                upper_color = Demo.buffer[(y*2+0)*w+x]
                lower_color = Demo.buffer[(y*2+1)*w+x]
            elif Demo.antialias:
                c0 = getpixel((x, y*2+0))
                c1 = getpixel((x, y*2+1))
                color = (int((c0[0]+c1[0])/2),
                         int((c0[1]+c1[1])/2),
                         int((c0[2]+c1[2])/2))
                upper_color = lower_color = make_555(color)
            else:
                upper_color = lower_color = Demo.buffer[(y*2)*w+x]
            ch = Demo.textbuffer[y*w+x]
            if Demo.hires and ch != ' ':
                # Fix for text_small in hires mode
                lower_color = upper_color
                if current_fore_color != 15:
                    current_fore_color = 15
                    # Fix for xterm black-on-white
                    out(f'\033[38;5;15m')
            if upper_color == lower_color == 0:
                if current_back_color != 0:
                    out('\033[48;5;0m')
                    current_back_color = 0
                out(ch)
            elif upper_color == lower_color:
                if current_back_color != upper_color:
                    out(f'\033[48;5;{upper_color}m')
                    current_back_color = upper_color
                out(ch)
            else:
                if current_back_color != upper_color:
                    out(f'\033[48;5;{upper_color}m')
                    current_back_color = upper_color
                if current_fore_color != lower_color:
                    out(f'\033[38;5;{lower_color}m')
                    current_fore_color = lower_color
                out('▄')
        if y < h-1:
            out('\r\n')
    out(f'\033[0m')
    sys.stdout.flush()


def text_big(text, pos, rgb, scale=(1, 1)):
    ww, hh, pixels = pixelfont(text)

    for y in range(hh):
        scry = pos[1] + y * scale[1]
        for x in range(ww):
            if pixels[y*ww+x]:
                scrx = pos[0] + x * scale[0]
                putpixel((scrx, scry*2), rgb)
                putpixel((scrx, scry*2+1), rgb)


def text_small(text, pos):
    x, y = pos
    for i, c in enumerate(text):
        Demo.textbuffer[y*w+x+i] = c


def dark_rectangle(x, y, w, h, darken=0.5):
    # Fake "transparent black" background rectangle
    for yy in range(y, y+h+2):
        for xx in range(x, x+w):
            c = getpixel((xx, yy))
            c = (c[0]*darken, c[1]*darken, c[2]*darken)
            putpixel((xx, yy), c)





def yields_frames(func):
    generator = func()
    def func(j):
        next(generator)
    return func

class LinesPoint:
    def __init__(self):
        self.pos = Vec2(random.randint(0, w), random.randint(0, h))
        self.vel = Vec2(random.uniform(0.1, 5), random.uniform(0.1, 5))
        self.color = (random.randint(10, 255),
                      random.randint(10, 255),
                      random.randint(10, 255))

    def update(self):
        self.pos += self.vel
        if self.pos.x > w:
            self.vel.x *= -0.9
            self.pos.x = w
        elif self.pos.x < 0:
            self.vel.x *= -0.9
            self.pos.x = 0
        if self.pos.y > h:
            self.vel.y *= -0.9
            self.pos.y = h
        elif self.pos.y < 0:
            self.vel.y *= -0.9
            self.pos.y = 0

@yields_frames
def lines_demo():
    points = [LinesPoint() for _ in range(20)]
    y = 0
    while True:
        for a, b in zip(points[1:], points):
            line((a.pos.x, a.pos.y), (b.pos.x, b.pos.y), a.color, b.color)
        for point in points:
            point.update()
        y += 1
        yield

def years_coroutine():
    frames_per_line = 10
    frames_afterglow = 105

    shaders = [
        ('Lines', 'It can draw lines.', lines_demo),
        ('Circles', 'And circles, too!', circles_demo),
        ('Triangles', 'Colored and smooth-shaded.', bouncing_triangles),
        ('Pixels', 'Render whatever you want.', rain),
    ]

    for title, description, background in shaders:
        year_text = [description]

        for year_lines in range(len(year_text)+1):
            for line_frame in range(frames_per_line + (frames_afterglow if year_lines == (len(year_text)) else 0)):
                frames_this_page = (year_lines * frames_per_line + line_frame)
                page_intro_ratio = frames_this_page / frames_per_line / 3 if year_lines <= 3 else 1
                yoff = min(0, -10*(1-easing_bounce(page_intro_ratio)))
                yoff = int(yoff)

                text_big(title, (1, yoff + 1), (0, 0, 0))
                text_big(title, (2, yoff + 1), (255, 255, 255))

                dark_rectangle(1, 20, max(len(line) for line in year_text)+4, 2*len(year_text)+2, 0.3)

                for y, line in enumerate(year_text[:year_lines+1]):
                    if y == year_lines-1:
                        exposed = int(line_frame/2)
                        line = line.split()
                        fixed = line[:exposed]
                        shuffled = line[exposed:]
                        random.shuffle(shuffled)
                        line = ' '.join(fixed + shuffled)
                    elif y == year_lines:
                        line = line.split()
                        random.shuffle(line)
                        line = ' '.join(line)
                    text_small(line, (3, 11+y))

                yield background
    yield lightning


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __iter__(self):
        return iter((self.r, self.g, self.b))

    def __mul__(self, f):
        return RGB(self.r * f, self.g * f, self.b * f)

    def __add__(self, other):
        return RGB(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, other):
        return RGB(self.r - other.r, self.g - other.g, self.b - other.b)

    def __truediv__(self, f):
        return RGB(self.r / f, self.g / f, self.b / f)

class Vertex:
    def __init__(self, x, y, color=None):
        self.pos = Pos(int(x), int(y))
        self.color = color or RGB(255, 255, 255)

    def __add__(self, other):
        return Vertex(self.pos.x + other.pos.x, self.pos.y + other.pos.y, self.color)

    def rotate(self, j):
        s = math.sin(j/180*math.pi)
        c = math.cos(j/180*math.pi)
        x = self.pos.x
        y = self.pos.y
        return Vertex(x*c-y*s, x*s+y*c)

    def recolor(self, color):
        res = Vertex(self.pos.x, self.pos.y)
        res.color = color
        return res

class Bounce:
    def __init__(self, **kwargs):
        self.x = int(w/2)
        self.y = int(h)
        self.dx = 2
        self.dy = 0.5
        self.rot = 1
        self.drot = 0
        self.rotup = 10
        self.hued = 0.05
        self.size = 20
        self.__dict__.update(kwargs)

    def update(self):
        self.x += self.dx
        if self.x > w or self.x < 0:
            self.dx *= -1
            self.drot += self.rotup
        self.y += self.dy
        if self.y > h or self.y < 0:
            self.dy *= -1
            self.drot += self.rotup
        self.rot += self.drot
        self.drot *= 0.95
        hh, l, s = colorsys.rgb_to_hls(*(self.color / 255))
        self.color = RGB(*colorsys.hls_to_rgb(hh+0.001, l, s)) * 255

    def triangle(self):
        hls = colorsys.rgb_to_hls(self.color.r/255, self.color.g/255, self.color.b/255)
        color1 = RGB(*colorsys.hls_to_rgb((hls[0]+self.hued)%1, hls[1], hls[2])) * 255
        color2 = RGB(*colorsys.hls_to_rgb((hls[0]+2*self.hued)%1, hls[1], hls[2])) * 255
        center = Vertex(int(self.x), int(self.y))
        return [center.recolor(self.color) + Vertex(self.size, 0).rotate(self.rot),
                center.recolor(color1) + Vertex(self.size, 0).rotate(self.rot+120),
                center.recolor(color2) + Vertex(self.size, 0).rotate(self.rot+240)]

@yields_frames
def bouncing_triangles():
    bounces = [
        Bounce(color=RGB(255, 0, 0)),
        Bounce(dx=-.9, dy=-1, color=RGB(0, 255, 0)),
        Bounce(dx=.9, dy=1, color=RGB(0, 0, 255)),
        Bounce(dx=-1.1, dy=-1.1, color=RGB(0, 255, 255)),
        Bounce(dx=1.1, dy=1.1, color=RGB(255, 0, 255)),
        Bounce(dx=-1.2, dy=-1.2, color=RGB(255, 255, 0)),
    ]

    bounces = []
    for i in range(1, 16):
        if i & 7 in (0, 7):
            continue
        bounces.append(Bounce(
            dx=(1.9+0.1*i)*math.sin(i*30*180/math.pi),
            dy=(1.9+0.1*i)*math.cos(i*30*180/math.pi),
            size=20-i,
            color=RGB(255 if (i & 1) else 0, 255 if (i & 2) else 0, 255 if (i & 4) else 0)))

    while True:
        for bounce in bounces:
            bounce.update()
            triangle(bounce.triangle())
        yield


class Vec2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return (self - other).length() < .0001

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l


@yields_frames
def circles_demo():
    i = 0
    while True:
        for y in range(0, h, 4):
            x = (10+i+y*8)%(w+10)-5
            circle((x, y), 8 + abs(8*math.sin(i*0.1)), (255, x*255/w, y*255/h))
        i += 1
        yield


def view_image(filename):
    from PIL import Image

    im = Image.open(filename)

    ww, hh = im.size

    ox = (w - ww) / 2
    oy = (h - hh) / 2

    px = im.load()
    for y in range(hh):
        for x in range(ww):
            putpixel((ox+x, oy+y), px[x, y][:3])
    del px


@yields_frames
def rain():
    a = [0]*(w*h)
    b = [0]*(w*h)

    def sample(dx, dy):
        xx = x + dx
        yy = y + dy
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            return a[y*w+x]
        return a[yy*w+xx]

    j = 0
    while True:
        a[random.randint(0, len(a)-1)] += 1000

        for y in range(h):
            for x in range(w):
                b[y*w+x] = (sample(0, -1) +
                            sample(0, +1) +
                            sample(0, 0) * 0.5 +
                            sample(-1, 0) +
                            sample(+1, 0)) / 2
                c = b[y*w+x]
                putpixel((x, y), (0, min(c*4, 255), min(c*3, 255)))
                b[y*w+x] *= 0.44

        a, b = b, a
        j += 1
        yield


@yields_frames
def lightning():
    class Bolt:
        def __init__(self):
            self.x0 = random.randint(0, w)
            self.x1 = max(0, min(w, self.x0 + random.randint(-20, +20)))
            self.dx0 = random.uniform(-0.5, -0.2) if self.x0 > w/2 else \
                    random.uniform(0.2, 0.5)
            self.y0 = 0
            self.y1 = h
            self.steps = 8
            self.lifetime = 0
            self.alpha_start =0

        def update(self):
            self.x0 += self.dx0
            self.lifetime += 1

        def branch(self):
            bolt = Bolt()
            where = random.uniform(0, 1)
            bolt.y0 = self.y0 * (1 - where) + self.y1 * where
            bolt.x0 = self.x0 * (1 - where) + self.x1 * where
            bolt.x1 = bolt.x0 + (self.x1 - self.x0)
            bolt.y1 = bolt.y0 + random.randint(10, 40)
            bolt.dx0 = self.dx0 * (1-where)
            bolt.alpha_start = where
            return bolt

    bolts = [Bolt()]

    def gencolor(blend):
        r = random.randint(0, 250)
        return (r*blend/5,
                random.randint(0, r)*blend/5,
                random.randint(200, 255)*blend/5)

    j = 0
    while True:
        for bolt in list(bolts):
            if (bolt.lifetime) > 30:
                bolts.remove(bolt)

        if j % 8 == 0:
            bolt = Bolt()
            bolts.append(bolt)
            bolts.append(bolt.branch())

        for bolt in bolts:
            bolt.update()
            last = Vec2(bolt.x0, bolt.y0)
            lastcolor = gencolor(bolt.lifetime)
            for step in range(bolt.steps):
                alpha = (step+1) / bolt.steps
                alpha = bolt.alpha_start + alpha * (1 - bolt.alpha_start)
                pos = Vec2(lerp(bolt.x0, bolt.x1, alpha) +
                           random.randint(-3, +3),
                           lerp(bolt.y0, bolt.y1, alpha))
                r = random.randint(0, 150)
                color = gencolor(bolt.lifetime * (1-alpha))
                line((last.x, last.y), (pos.x, pos.y), lastcolor, color)
                last = pos
                lastcolor = color

        j += 1
        yield

class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __mul__(self, f):
        if isinstance(f, Vec3):
            return Vec3(self.x * f.x, self.y * f.y, self.z * f.z)
        else:
            return Vec3(self.x * f, self.y * f, self.z * f)

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.dot(self)

    def normalized(self):
        return self / self.length()

    def __truediv__(self, f):
        return Vec3(self.x / f, self.y / f, self.z / f)


class Matrix4x4(object):
    def __init__(self, m=None):
        self.side = 4
        if m:
            self.matrix = m
        else:
            self.matrix = [1 if x == y else 0 for y in range(self.side) for x in range(self.side)]

    def __mul__(self, other):
        a = self.matrix
        b = other.matrix
        return Matrix4x4([
            a[0] * b[0] + a[1] * b[4] + a[2] * b[8] + a[3] * b[12],
            a[0] * b[1] + a[1] * b[5] + a[2] * b[9] + a[3] * b[13],
            a[0] * b[2] + a[1] * b[6] + a[2] * b[10] + a[3] * b[14],
            a[0] * b[3] + a[1] * b[7] + a[2] * b[11] + a[3] * b[15],

            a[4] * b[0] + a[5] * b[4] + a[6] * b[8] + a[7] * b[12],
            a[4] * b[1] + a[5] * b[5] + a[6] * b[9] + a[7] * b[13],
            a[4] * b[2] + a[5] * b[6] + a[6] * b[10] + a[7] * b[14],
            a[4] * b[3] + a[5] * b[7] + a[6] * b[11] + a[7] * b[15],

            a[8] * b[0] + a[9] * b[4] + a[10] * b[8] + a[11] * b[12],
            a[8] * b[1] + a[9] * b[5] + a[10] * b[9] + a[11] * b[13],
            a[8] * b[2] + a[9] * b[6] + a[10] * b[10] + a[11] * b[14],
            a[8] * b[3] + a[9] * b[7] + a[10] * b[11] + a[11] * b[15],

            a[12] * b[0] + a[13] * b[4] + a[14] * b[8] + a[15] * b[12],
            a[12] * b[1] + a[13] * b[5] + a[14] * b[9] + a[15] * b[13],
            a[12] * b[2] + a[13] * b[6] + a[14] * b[10] + a[15] * b[14],
            a[12] * b[3] + a[13] * b[7] + a[14] * b[11] + a[15] * b[15],
        ])

    __rmul__ = __mul__

    def map_vec3(self, v3):
        p = (v3.x, v3.y, v3.z, 1.)
        p = [sum(p[row] * self.matrix[i * 4 + row] for row in range(4)) for i, v in enumerate(p)]
        return Vec3(p[0] / p[3], p[1] / p[3], p[2] / p[3])

    @staticmethod
    def translation(x, y, z):
        return Matrix4x4([1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, z, 0, 0, 0, 1])

    @staticmethod
    def rotation(angle, x, y, z):
        x, y, z = Vec3(x, y, z).normalized()
        c = math.cos(angle / 180 * math.pi)
        s = math.sin(angle / 180 * math.pi)
        return Matrix4x4([
            x * x * (1 - c) + 1 * c, x * y * (1 - c) - z * s, x * z * (1 - c) + y * s, 0,
            y * x * (1 - c) + z * s, y * y * (1 - c) + 1 * c, y * z * (1 - c) - x * s, 0,
            x * z * (1 - c) - y * s, y * z * (1 - c) + x * s, z * z * (1 - c) + 1 * c, 0,
            0, 0, 0, 1,
        ])

    @classmethod
    def perspective(cls, fovy, aspect, zNear, zFar):
        f = math.cos(fovy / 2) / math.sin(fovy / 2)
        return cls([f / aspect, 0, 0, 0, 0, f, 0, 0, 0, 0, (zFar + zNear) /
            (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar), 0, 0, -1, 0])

def easing_bounce(p):
    if p < 4./11.:
        return (121 * p * p)/16.0
    elif p < 8./11.:
        return (363/40.0 * p * p) - (99/10.0 * p) + 17/5.0
    elif p < 9/10.:
        return (4356/361.0 * p * p) - (35442/1805.0 * p) + 16061/1805.0
    else:
        return (54/5.0 * p * p) - (513/25.0 * p) + 268/25.0

@yields_frames
def cube():
    front = [
        # front
        Vec3(-10, +10, +10),
        Vec3(-10, -10, +10),
        Vec3(+10, +10, +10),
        Vec3(+10, -10, +10),

        # back
        Vec3(-10, +10, -10),
        Vec3(-10, -10, -10),
        Vec3(+10, +10, -10),
        Vec3(+10, -10, -10),

        # left
        Vec3(-10, +10, -10),
        Vec3(-10, -10, -10),
        Vec3(-10, +10, +10),
        Vec3(-10, -10, +10),

        # right
        Vec3(+10, +10, -10),
        Vec3(+10, -10, -10),
        Vec3(+10, +10, +10),
        Vec3(+10, -10, +10),

        # top
        Vec3(+10, +10, -10),
        Vec3(-10, +10, -10),
        Vec3(+10, +10, +10),
        Vec3(-10, +10, +10),

        # bottom
        Vec3(+10, -10, -10),
        Vec3(-10, -10, -10),
        Vec3(+10, -10, +10),
        Vec3(-10, -10, +10),
    ]

    colors = [tuple(int(255*x) for x in colorsys.hls_to_rgb(0.05+0.6*i/6, 0.5, 0.9)) for i in range(6)]

    tris = [
        # front
        ((0, 1, 2), colors[0]),
        ((2, 1, 3), colors[0]),

        # back
        ((4, 6, 5), colors[1]),
        ((6, 7, 5), colors[1]),

        # left
        ((8, 9, 10), colors[2]),
        ((10, 9, 11), colors[2]),

        # right
        ((12, 14, 13), colors[3]),
        ((14, 15, 13), colors[3]),

        # top
        ((16, 17, 18), colors[4]),
        ((18, 17, 19), colors[4]),

        # bottom
        ((20, 22, 21), colors[5]),
        ((22, 23, 21), colors[5]),
    ]

    def clipspace2screenspace(v):
        return Vec2(v.x*fx+w/2, v.y*fy+h/2)

    def clipspace2screenspace_cube(v):
        pos = clipspace2screenspace(v)
        pos.y += 30*(easing_bounce(min(1, (j-20)/30))-1)
        return (pos.x, pos.y)

    def rnz():
        return random.uniform(0.01, 1)*random.choice([-1, 1])

    stars = [Vec3(rnz(), rnz(), rnz()).normalized() * 40 for _ in range(90)]

    j = 0
    while True:
        tm = 0.05 * j
        s = math.sin(tm)
        c = math.cos(tm)
        delayed = max(0, min(1, (j-30)/50))
        axis = Vec3(s*delayed, c*delayed, s*c*delayed if delayed != 0 else 1).normalized()

        factor = 1.5+(0.5+0.5*s)*min(1, j/60)
        fx = w*factor
        fy = h*factor

        p = Matrix4x4.perspective(90, 16/10, 0.01, 100)
        m = Matrix4x4.rotation(j*4*delayed, axis.x, axis.y, axis.z)
        t = Matrix4x4.translation(0, 0, -50)
        rotated = [p.map_vec3(t.map_vec3(m.map_vec3(v))) for v in front]

        stars_mapped = [p.map_vec3(t.map_vec3(m.map_vec3(s))) for s in stars]
        for star in stars_mapped:
            pos = clipspace2screenspace(star)
            putpixel((pos.x, pos.y), (128, 128, 128))

        idx = 0
        for (tri, color) in tris:
            a, b, c = [rotated[idx] for idx in tri]
            normal = (b - a).cross(c - a)
            if idx % 2 == 0:
                n = normal
            # https://stackoverflow.com/a/9120171/1047040
            if normal.z > 0:
                triangle([Vertex(*clipspace2screenspace_cube(v), RGB(*color)*(0.2+n.z*14))
                          for v in [a, b, c]])
            idx += 1
        j += 1
        yield


def come_from_center_coroutine(lines):
    sc = (60, 60, 60)

    sh = h/2
    th = 8
    for j in range(80):
        ts = min(1, j/10)
        ts = ts

        y0 = (sh-((th)*len(lines)*ts))/2 - 1

        for idx, line in enumerate(lines):
            tw = len(line)*8

            y = (sh-(th*ts)) / 2 * (1 - ts) + (y0+th*idx) * ts
            y += int(9 * math.sin(ts*math.pi))

            x = (w-tw*ts)/2-1

            text_big(line, (x+1-2*(idx%2), y), sc, (ts, ts))
            text_big(line, (x, y), (255, 255, 255), (ts, ts))

        yield


def fade_to_black_coroutine(frames):
    for i in range(frames):
        for y in range(h):
            for x in range(w):
                c = getpixel((x, y))
                darken = 1 - i/frames
                c = (c[0]*darken, c[1]*darken, c[2]*darken)
                putpixel((x, y), c)
        yield


def run_demo(out):
    background_shader = cube

    overlays = [
        come_from_center_coroutine(['thp.io', 'presents']),
        come_from_center_coroutine(['ttyfb 0.1', 'preview', 'for python']),
        years_coroutine(),
        come_from_center_coroutine(['create', 'something', 'awesome!']),
        fade_to_black_coroutine(60),
    ]

    overlay = overlays.pop(0)

    out('\033[2J', '\033[?25l')
    try:
        j = 0
        while True:
            started_time = time.time()

            clear()

            background_shader(j)

            try:
                background_shader = next(overlay) or background_shader
            except StopIteration:
                if not overlays:
                    break
                overlay = overlays.pop(0)

            render(out)

            j += 1
            time.sleep(max(0, 0.04-(time.time() - started_time)))
    finally:
        out('\033[2J\033[H\033[0m', '\033[?25h')


if __name__ == '__main__':
    try:
        run_demo(to_stdout)
    except KeyboardInterrupt:
        ...
