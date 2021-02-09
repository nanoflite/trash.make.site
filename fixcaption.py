from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import markdown
import re

class FixCaption(Preprocessor):
    """\[caption ...\]![](images/....jpg) blah.\[/caption\] --> [blah](...jpg) """
    def run(self, lines):
        out = []
        for line in lines:
            m = re.search("\\\\\\[caption.*\\]", line)
            if m:
                print("--> CAPTION DETECTED")
                print(line)
                caption = m.group(0)
                print(caption)
                mc = re.search("](.+)\\\\\[", caption)
                malformedlink = mc.group(1)
                mf = re.search("^\!\[.*\]\((.+?)\)\s+(.+)$", malformedlink)
                print(mf)
                image = '![{desc}]({link} "{desc}")'.format(desc=mf.group(2), link=mf.group(1))
                new_line = line.replace(caption, image)
                print(new_line)
                out.append(new_line)
            else:
                out.append(line)
        return out

class FixCaptionExtension(Extension):

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(FixCaption(md), 'fixcaption', 100)
