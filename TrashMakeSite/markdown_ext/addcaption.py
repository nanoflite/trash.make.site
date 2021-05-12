from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import markdown
import re

class AddCaption(Preprocessor):
    """![blah](*.jpg) ---> ![blah](*.jpg)"""
    def run(self, lines):
        out = []
        for line in lines:
            m = re.search("\!\[(.*?)\]\(.+?\)$", line)
            if m:
                print("--> IMAGE DETECTED")
                print(line)
                image = m.group(0)
                print(image)
                caption = m.group(1)
                new_image = '{image}\n{caption}'.format(image=image, caption=caption)
                new_line = line.replace(image, new_image)
                print(new_line)
                out.append(new_line)
            else:
                out.append(line)
        return out

class AddCaptionExtension(Extension):

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(AddCaption(md), 'addcaption', 90)
