from ttyfb import *

from ttyfb import Demo

import hashlib
import requests
import io
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description='Show your gravatar')
parser.add_argument('email', type=str, help='Your gravatar e-mail address')
parser.add_argument('nickname', type=str, help='Your nickname')
args = parser.parse_args()

url = ('https://www.gravatar.com/avatar/' +
       hashlib.md5(args.email.encode()).hexdigest())
img = Image.open(io.BytesIO(requests.get(url).content))

Demo.mode = Demo.MODE_256_DITHER

fill((0, 0, 0))

view_image(img.resize((40, 40)))

text_big(args.nickname, (-1, 0), (0, 0, 0))
text_big(args.nickname, (0, 0), (255, 255, 255))

render(to_stdout)
