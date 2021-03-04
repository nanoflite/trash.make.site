from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re
from ..dither import dither
from ..dominantcolor import (dominant_colors, hexcolor)
from pathlib import Path
import shutil

def _handle_double_quote(s, t):
    k, v = t.split('=', 1)
    return k, v.strip('"')


def _handle_single_quote(s, t):
    k, v = t.split('=', 1)
    return k, v.strip("'")


def _handle_key_value(s, t):
    return t.split('=', 1)


def _handle_word(s, t):
    if t.startswith('.'):
        return '.', t[1:]
    if t.startswith('#'):
        return 'id', t[1:]
    return t, t


_scanner = re.Scanner([
    (r'[^ =]+=".*?"', _handle_double_quote),
    (r"[^ =]+='.*?'", _handle_single_quote),
    (r'[^ =]+=[^ =]+', _handle_key_value),
    (r'[^ =]+', _handle_word),
    (r' ', None)
])

ATTR_RE = r'\{\:(.+?)\}'
IMG_RE = r'\!\[.*?\]\((\S+)\s*.*?\)'

def get_attrs(str):
    """ Parse attribute list and return a list of attribute tuples. """
    am = re.search(ATTR_RE, str)
    if am:
        return dict(_scanner.scan(am.group(1))[0])
    else:
        return {}

class DitherImages(Preprocessor):
    """![blah](img.jpg) --> ![blah](img_dithered.png)"""


    def __init__(self, md, config):
        super().__init__(md)

        self.source = config["source"]
        self.destination = config["destination"]

        self.md.colors = {}

    def dither_image(self, image):
        src = self.source + '/' + image
        path = Path(image)
        new_image = str(path.parent) + '/' + str(path.stem) + '_dithered.png'
        dst = self.destination + '/' + new_image
        dither(src, dst, (640, 640))
        colors = dominant_colors(src)
        if colors != None:
            colour = hexcolor(colors[0])
        else:
            colour = 'ffffff'
        return colour

    def new_line(self, match, image, line, colour):
        path = Path(image)
        new_image = str(path.parent) + '/' + str(path.stem) + '_dithered.png'
        new_match = match.replace(image, new_image) + '{: colour="' + colour + '"  }'
        new_line = line.replace(match, new_match)
        return new_line

    def copy_image(self, image):
        src = self.source + '/' + image
        dst = self.destination + '/' + image
        shutil.copy(src, dst)

    def run(self, lines):
        out = []
        for line in lines:
            m = re.search(IMG_RE, line)
            if (not m):
                out.append(line)
                continue
            match = m.group(0)
            image = m.group(1)
            attrs = get_attrs(line)
            line = re.sub(ATTR_RE, '', line)
            if attrs.get('dither') == 'no':
                self.copy_image(image)
                out.append(line)
            else:
                colour = self.dither_image(image)
                out.append(self.new_line(match, image, line, colour))
        return out

class DitherImagesExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            "source": [ '', 'Source folder'],
            "destination": [ 'build', 'Destination folder']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        md.preprocessors.register(DitherImages(md, self.getConfigs()), 'ditherimages', 50)
