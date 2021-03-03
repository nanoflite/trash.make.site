from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

class ExtractFirstParagraph(Treeprocessor):

    def run(self, doc):
        for el in doc.iter():
            if el.tag == 'p':
                self.md.FirstParagraph = el.text
                break

class ExtractFirstParagraphExtension(Extension):
    """Get the first paragraph from the MD file."""

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        md.treeprocessors.register(ExtractFirstParagraph(md), 'firstparagraph', 100)

    def reset(self):
        self.md.FirstParagraph = None