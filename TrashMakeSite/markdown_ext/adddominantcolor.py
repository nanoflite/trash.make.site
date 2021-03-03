"""
Add a paragraph to images with a style to add the dominant color to dithered images
"""

from markdown.extensions import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

IMAGES = [u'^\s*' + IMAGE_LINK_RE, u'^\s*' + IMAGE_REFERENCE_RE]
COLOUR = r'colour="(?P<colour>.+?)"'
WANTCOLOUR = r'__adc__'

class AddDominantColorProcessor(BlockProcessor):

    IMAGES_RE = re.compile('|'.join(IMAGES))
    COLOUR_RE = re.compile(COLOUR)
    WANTCOLOUR_RE = re.compile(WANTCOLOUR)

    def test(self, parent, block):
        if bool(self.IMAGES_RE.search(block)):
            if bool(self.WANTCOLOUR_RE.search(block)):
                return True
        return False

    def run(self, parent, blocks):
        block = blocks.pop(0)
        try:
            colour = self.COLOUR_RE.search(block).group('colour')
        except:
            colour = None

        div = etree.SubElement(parent, 'div')
        div.set('class', 'dithered')
        p = etree.SubElement(div, 'p')
        p.set('class', 'dithered')
        if colour:
            block = re.sub(r'\{:\s*colour=".+?"\s*\}', '', block)
            p.set('style', 'background-color: #'+ colour)
        p.text = block

class AddDominantColorProcessorExtension(Extension):

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(AddDominantColorProcessor(md.parser), 'dominantcolor', 100)



