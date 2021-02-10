from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re
from dither import dither
from pathlib import Path
import os

class DitherImages(Preprocessor):
    """![blah](img.jpg) --> ![blah](img_dithered.png)"""

    def __init__(self, md, config):
        super().__init__(md)

        self.source = config["source"]
        self.destination = config["destination"]

    def run(self, lines):
        out = []
        for line in lines:
            m = re.search("\!\[.*\]\((.*?)\s.*.*\)", line)
            if m:
                image = m.group(1)
                src = self.source + '/' + image
                path = Path(image)
                new_image = str(path.parent) + '/' + str(path.stem) + '_dithered.png'
                dst = self.destination + '/' + new_image
                if os.path.isfile(src):
                    dither(src, dst, (640, 640))
                    new_line = line.replace(image, new_image)
                    out.append(new_line)
                else:
                    out.append(line)
            else:
                out.append(line)
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
        # If not work --> change priority! fixcaption must be run first
        md.preprocessors.register(DitherImages(md, self.getConfigs()), 'ditherimages', 50)
