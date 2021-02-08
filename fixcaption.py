from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import markdown
import re

class FixCaption(Preprocessor):
    """\[caption ...\]![](images/....jpg) blah.\[/caption\] --> [blah](...jpg) """
    def run(self, lines):
        out = []
        for line in lines:
            m = re.search("\\[caption.*\\]", line)
            if m:
                print("--> CAPTION DETECTED")
                caption = m.group(0)
                print(caption)
                mc = re.search("](.+)\\\\\[", caption)
                malformedlink = mc.group(1)
                mf = re.search("^\!\[\]\((.+?)\)\s+(.+)$", malformedlink)
                image = '![{desc}]({link} "{desc}")'.format(desc=mf.group(2), link=mf.group(1))
                print(image)
                out.append(line.replace(caption, image))
            else:
                out.append(line)
        return out

class FixCaptionExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(FixCaption(md), 'fixcaption', 100)

md = markdown.Markdown(extensions=[FixCaptionExtension()])
f = open('./source/post/2017-03-08-flappy-bird-running-home-build-basic-computer/index.md')
raw = f.read()
f.close()
print(md.convert(raw))