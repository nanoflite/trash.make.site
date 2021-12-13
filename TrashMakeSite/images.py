import re
from pathlib import Path

ATTR_RE = r'\{\:(.+?)\}'
IMG_RE = r'!\[([^\]]*)\]\(([^\)]*)\)(\{\:(.+?)\})*'

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

def get_attrs(str):
    """ Parse attribute list and return a list of attribute tuples. """
    am = re.search(ATTR_RE, str)
    if am:
        return dict(_scanner.scan(am.group(1))[0])
    else:
        return {}

def parse_images(self, m, state):
    match = m.group(0)
    title = m.group(1)
    image = m.group(2)
    tm = re.match(r'([^\]]*)', title)
    title = tm.group(1)
    options = m.group(3)
    dithered = True
    if options != None:
        attrs = get_attrs(options)
        if attrs.get('dither') == 'no':
            dithered = False
    if dithered:
        path = Path(image)
        image = str(path.parent) + '/' + str(path.stem) + '_dithered.png'
    #print('match', match)
    #print('-> title', title)
    #print('-> image', image)
    #print('-> options', options)
    return 'gimages', image, title

def render_gemini_images(image, title):
    return f'=> {image} {title}'

def render_gopher_images(image, title):
    marker = 'g' if image.endswith('.gif') else 'I'
    return marker + (title or 'image') + '\t' + image + '\n'

def plugin_images(md):
    md.inline.register_rule('gimages', IMG_RE, parse_images)
    md.inline.rules.insert(0, 'gimages')

    if md.renderer.NAME == 'GEMINI':
        md.renderer.register('gimages', render_gemini_images)

    if md.renderer.NAME == 'GOPHER':
        md.renderer.register('gimages', render_gopher_images)
