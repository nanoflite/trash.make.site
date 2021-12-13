from mistune.renderers import BaseRenderer
from textwrap import wrap

class GeminiRenderer(BaseRenderer):
    NAME = 'GEMINI'

    def __init__(self, tabWidth=2):
        super(GeminiRenderer, self).__init__()
        self._tabWidth = tabWidth
        self.refs = []
        self.refCount = 1

    def _noTabs(self, text):
        return text.replace('\t', ' ' * self._tabWidth)

    def generateRefs(self):
        text = '\n'
        text += '# References:\n'
        text += '\n'.join(list(map(lambda r: '=> ' + r, self.refs)))
        return text

    def text(self, text):
        if text.startswith('{'):
            return ''
        return self._noTabs(text)

    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        text = self._noTabs(text)

        r = str(self.refCount)
        line = link + ' [ref#' + r + '] ' + (text or title or link)

        if text or title:
            out = (text or title) + ' ('
        out += 'ref#' + r
        if text or title:
            out += ')'

        self.refs.append(line)
        self.refCount += 1

        return out

    def image(self, src, alt="", title=None):
        line = '\n=>' + src + ' ' + (alt or title or '') + '\n'
        return line

    def emphasis(self, text):
        return self._noTabs(text)

    def strong(self, text):
        return self._noTabs(text)

    def codespan(self, text):
        return '```\n' + text + '```\n'

    def linebreak(self):
        return '\n'

    def inline_html(self, html):
        return self._noTabs(html)

    def paragraph(self, text):
        return text + '\n'

    def heading(self, text, level):
        level = level if level <= 3 else 3
        text = '#' * level + ' ' + self._noTabs(text) + '\n'
        return text

    def newline(self):
        return '\n'

    def thematic_break(self):
        return '\n'

    def block_text(self, text):
        return text + '\n'

    def block_code(self, code, info=None):
        if info is not None:
            info = info.strip()

        lang = None
        if info:
            lang = info.split(None, 1)[0]

        out = '```'
        if lang:
            out += ' (lang:' + lang + ')'
        out += '\n' + code + '\n```\n'
        return out

    def block_quote(self, text):
        return '> ' + self._noTabs(text)

    def block_html(self, html):
        return self._noTabs(html)

    def block_error(self, html):
        return 'ERROR: ' + self._noTabs(html) + '\n'

    def list(self, text, ordered, level, start=None):
        return text

    def list_item(self, text, level):
        return '* ' + text

    def finalize(self, data):
        return ''.join(data)