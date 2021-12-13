from mistune.renderers import BaseRenderer
from textwrap import wrap

class GopherRenderer(BaseRenderer):
    NAME = 'GOPHER'

    def __init__(self, tabWidth=2):
        super(GopherRenderer, self).__init__()
        self._tabWidth = tabWidth
        self.refs = []
        self.refCount = 1

    def _noTabs(self, text):
        return text.replace('\t', ' ' * self._tabWidth)

    def generateRefs(self):
        text = ''
        text += '-' * 75 + '\n'
        text += 'References:\n'
        text += '\n'.join(self.refs)
        return text

    def text(self, text):
        if text.startswith('{'): return ''
        return self._noTabs(text)

    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        text = self._noTabs(text)

        relative = False if link.startswith('http') else True
        mail = True if link.startswith('mailto:') else False

        r = str(self.refCount)
        if relative:
            line = '1[ref#' + r + '] ' + (text or title or link) + '\t' + link
        else:
            line = 'h[ref#' + r + '] ' + (text or title or link) + '\t' + 'URL:' + link

        if mail:
            line = 'h[ref#' + r + '] ' + (text or title or link) + '\t' + 'URL:' + link

        if text or title:
            out =(text or title) + ' ('
        out += 'ref#' + r
        if text or title:
            out += ')'

        self.refs.append(line)
        self.refCount += 1

        return out


    def image(self, src, alt="", title=None):
        gif = True if src.endswith('.gif') else False
        if gif:
            line = 'g' + (alt or title or 'image') + '\t' + src + '\n'
        else:
            line = 'I' + (alt or title or 'image') + '\t' + src + '\n'

        return line + '\n'

    def emphasis(self, text):
        return self._noTabs(text)

    def strong(self, text):
        return self._noTabs(text)

    def codespan(self, text):
        text = self._noTabs(text)
        lines = text.split('\n')
        formatted = []
        for line in lines:
            formatted.append('  ' + line)
        return "\n".join(formatted)

    def linebreak(self):
        return '\n'

    def inline_html(self, html):
        return self._noTabs(html)

    def paragraph(self, text):
        if (text.startswith('I') or text.startswith('g')) and text.find('\t') > -1:
            return text
        else:
            return '\n'.join(wrap(self._noTabs(text), width=67)) + '\n\n'

    def heading(self, text, level):
        text = '// ' + self._noTabs(text) + ' //'
        return text + '\n\n'

    def newline(self):
        return ''

    def thematic_break(self):
        return '-' * 75 + '\n'

    def block_text(self, text):
        return self._noTabs(text)

    def block_code(self, code, info=None):
        code = self._noTabs(code)
        if info is not None:
            info = info.strip()

        lang = None
        if info:
            lang = info.split(None, 1)[0]
        code = self.codespan(code)

        out = '\n'
        if lang:
            out += '(' + lang + ')\n'
        out += code + '\n'

        return out

    def block_quote(self, text):
        return self._noTabs(text)

    def block_html(self, html):
        return self._noTabs(html)

    def block_error(self, html):
        return 'ERROR: ' + self._noTabs(html) + '\n'

    def list(self, text, ordered, level, start=None):
        return self._noTabs(text) + '\n'

    def list_item(self, text, level):
        return '  * ' + self._noTabs(text) + '\n'

    def finalize(self, data):
        return ''.join(data)